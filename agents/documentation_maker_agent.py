from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional
import openai
from loguru import logger
import os
from dotenv import load_dotenv
from .utils import rate_limit
from pathlib import Path

load_dotenv()

class TechnicalLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class DocumentationConfig:
    target_audience: str
    technical_level: TechnicalLevel
    format: str
    language: str = "en"
    style_guide: str = "default"

class DocumentationMakerAgent:
    def __init__(self, config: DocumentationConfig):
        self.config = config
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        
    @rate_limit(calls_per_minute=60)
    async def generate_documentation(self, topic: str, content: str) -> str:
        """Generate documentation based on the given topic and content"""
        try:
            prompt = self._create_prompt(topic, content)
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}")
            return ""
    
    def _create_prompt(self, topic: str, content: str) -> str:
        """Create a prompt for the AI model"""
        return f"""
        Create documentation for the following topic: {topic}
        
        Technical Level: {self.config.technical_level.value}
        Target Audience: {self.config.target_audience}
        Format: {self.config.format}
        
        Content to document:
        {content}
        
        Please structure the documentation appropriately for the specified technical level
        and target audience. Include examples where relevant.
        """
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt based on configuration"""
        return f"""
        You are a technical documentation writer specializing in {self.config.technical_level.value} level content.
        Your task is to create clear, concise, and accurate documentation that is appropriate for {self.config.target_audience}.
        Follow the {self.config.style_guide} style guide and ensure the documentation is well-structured and easy to follow.
        """
    
    def organize_content(self, content: str) -> Dict[str, str]:
        """Organize content into sections"""
        sections = {
            "Overview": "",
            "Prerequisites": "",
            "Installation": "",
            "Usage": "",
            "Examples": "",
            "API Reference": "",
            "Troubleshooting": ""
        }
        
        # Simple content organization based on headers
        current_section = "Overview"
        for line in content.split('\n'):
            if line.startswith('#'):
                section_name = line.strip('#').strip()
                if section_name in sections:
                    current_section = section_name
            else:
                sections[current_section] += line + '\n'
                
        return sections
    
    @rate_limit(calls_per_minute=60)
    async def validate_documentation(self, documentation: str) -> bool:
        """Validate the generated documentation"""
        # Check for required sections
        required_sections = ["Overview", "Prerequisites", "Usage"]
        for section in required_sections:
            if f"# {section}" not in documentation:
                logger.warning(f"Missing required section: {section}")
                return False
                
        # Check for code examples if technical level is not beginner
        if self.config.technical_level != TechnicalLevel.BEGINNER:
            if "```" not in documentation:
                logger.warning("Missing code examples")
                return False
                
        return True
    
    @rate_limit(calls_per_minute=60)
    async def format_documentation(self, documentation: str) -> str:
        """Format the documentation according to the specified format"""
        if self.config.format == "markdown":
            return documentation
        elif self.config.format == "html":
            # Convert markdown to HTML (would need a markdown parser)
            return documentation
        else:
            logger.warning(f"Unsupported format: {self.config.format}")
            return documentation 