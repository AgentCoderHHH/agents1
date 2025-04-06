import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from loguru import logger
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path

# Load environment variables
load_dotenv()

class ResearchDepth(Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"

@dataclass
class ResearchConfig:
    depth: ResearchDepth = ResearchDepth.STANDARD
    max_results: int = 5
    max_tokens: int = 2000
    temperature: float = 0.7

class InternetDocumentationAgent:
    def __init__(self, config: Optional[ResearchConfig] = None):
        self.config = config or ResearchConfig()
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.research_history = []

    async def research_topic(self, topic: str) -> Dict[str, Any]:
        """
        Research a topic using GPT-4 and return structured results.
        """
        try:
            # Create system prompt based on research depth
            system_prompt = self._create_system_prompt(topic)
            
            # Generate research content
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Research the topic: {topic}"}
                ],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature
            )
            
            # Parse and structure the response
            research_content = response.choices[0].message.content
            structured_results = self._structure_research_results(research_content)
            
            # Assess quality and relevance
            quality_score = await self._assess_quality(structured_results)
            
            # Store in history
            self.research_history.append({
                "topic": topic,
                "results": structured_results,
                "quality_score": quality_score
            })
            
            return structured_results
            
        except Exception as e:
            logger.error(f"Error researching topic {topic}: {str(e)}")
            raise

    def _create_system_prompt(self, topic: str) -> str:
        """Create a system prompt based on research depth."""
        depth_instructions = {
            ResearchDepth.QUICK: "Provide a concise overview with key points.",
            ResearchDepth.STANDARD: "Provide a comprehensive analysis with examples.",
            ResearchDepth.DEEP: "Provide an in-depth analysis with detailed examples and technical details."
        }
        
        return f"""You are a research assistant specializing in {topic}.
        {depth_instructions[self.config.depth]}
        Structure your response with clear sections and bullet points.
        Include relevant examples and code snippets where appropriate.
        Focus on accuracy and clarity."""

    def _structure_research_results(self, content: str) -> Dict[str, Any]:
        """Structure the research content into a standardized format."""
        return {
            "overview": content,
            "sections": self._extract_sections(content),
            "examples": self._extract_examples(content),
            "references": self._extract_references(content)
        }

    def _extract_sections(self, content: str) -> List[Dict[str, str]]:
        """Extract main sections from the content."""
        # Simple section extraction based on headers
        sections = []
        current_section = {"title": "", "content": ""}
        
        for line in content.split("\n"):
            if line.startswith("#"):
                if current_section["title"]:
                    sections.append(current_section)
                    current_section = {"title": "", "content": ""}
                current_section["title"] = line.strip("#").strip()
            else:
                current_section["content"] += line + "\n"
        
        if current_section["title"]:
            sections.append(current_section)
            
        return sections

    def _extract_examples(self, content: str) -> List[Dict[str, str]]:
        """Extract code examples from the content."""
        examples = []
        current_example = {"description": "", "code": ""}
        in_code_block = False
        
        for line in content.split("\n"):
            if line.startswith("```"):
                in_code_block = not in_code_block
                if not in_code_block and current_example["code"]:
                    examples.append(current_example)
                    current_example = {"description": "", "code": ""}
            elif in_code_block:
                current_example["code"] += line + "\n"
            elif line.strip() and not line.startswith("#"):
                current_example["description"] += line + "\n"
        
        return examples

    def _extract_references(self, content: str) -> List[str]:
        """Extract references from the content."""
        references = []
        for line in content.split("\n"):
            if line.startswith("- ") or line.startswith("* "):
                references.append(line[2:].strip())
        return references

    async def _assess_quality(self, results: Dict[str, Any]) -> float:
        """Assess the quality of research results."""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a quality assessment assistant."},
                    {"role": "user", "content": f"Rate the quality of this research (0-1): {json.dumps(results)}"}
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            quality_text = response.choices[0].message.content
            try:
                return float(quality_text)
            except ValueError:
                return 0.5  # Default score if parsing fails
                
        except Exception as e:
            logger.error(f"Error assessing quality: {str(e)}")
            return 0.5  # Default score on error 