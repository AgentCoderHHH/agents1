from dataclasses import dataclass
from typing import List, Optional
import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import spacy
from loguru import logger
from github import Github
import os
from dotenv import load_dotenv
from .utils import rate_limit
from openai import OpenAI

load_dotenv()

@dataclass
class WebResearchConfig:
    search_engines: List[str]
    content_filters: List[str]
    credibility_threshold: float
    browser_type: str = "chrome"
    headless: bool = True

class InternetDocumentationAgent:
    def __init__(self, config: WebResearchConfig):
        self.config = config
        self.nlp = spacy.load("en_core_web_sm")
        self.github = Github(os.getenv("GITHUB_TOKEN"))
        self.client = OpenAI()
        self.browser = None
        self.context = None
        
    async def initialize(self):
        """Initialize the agent's resources"""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=self.config.headless
        )
        self.context = await self.browser.new_context()
        
    @rate_limit(calls_per_minute=60)
    async def search_web(self, query: str) -> List[str]:
        """Search the web for relevant information"""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a web search expert."},
                {"role": "user", "content": f"Generate search queries for: {query}"}
            ]
        )
        return [query.strip() for query in response.choices[0].message.content.split('\n')]
    
    def _extract_links(self, content: str) -> List[str]:
        """Extract relevant links from search results"""
        soup = BeautifulSoup(content, 'lxml')
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and self._is_relevant(href):
                links.append(href)
        return links
    
    def _is_relevant(self, url: str) -> bool:
        """Check if a URL is relevant based on filters"""
        return any(filter in url.lower() for filter in self.config.content_filters)
    
    @rate_limit(calls_per_minute=60)
    async def extract_content(self, url: str) -> str:
        """Extract content from a webpage"""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a content extraction expert."},
                {"role": "user", "content": f"Extract the main content from this URL: {url}"}
            ]
        )
        return response.choices[0].message.content
    
    @rate_limit(calls_per_minute=60)
    async def assess_credibility(self, content: str) -> float:
        """Assess the credibility of content using NLP"""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a content credibility assessor."},
                {"role": "user", "content": f"Assess the credibility of this content (0-1 scale):\n\n{content}"}
            ]
        )
        return float(response.choices[0].message.content)
    
    async def store_documentation(self, content: str, path: str):
        """Store documentation in GitHub"""
        try:
            repo = self.github.get_repo(os.getenv("GITHUB_REPO"))
            repo.create_file(
                path=path,
                message=f"Add documentation: {path}",
                content=content,
                branch="main"
            )
        except Exception as e:
            logger.error(f"Error storing documentation: {str(e)}")
    
    async def cleanup(self):
        """Clean up resources"""
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop() 