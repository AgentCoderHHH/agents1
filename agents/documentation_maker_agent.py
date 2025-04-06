from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Any
from loguru import logger
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from pathlib import Path
from .utils import rate_limit

load_dotenv()

class TechnicalLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class DocumentationConfig:
    target_audience: TechnicalLevel = TechnicalLevel.INTERMEDIATE
    format: str = "markdown"
    include_examples: bool = True
    max_tokens: int = 4000
    temperature: float = 0.7

class DocumentationMakerAgent:
    """Agent for generating comprehensive documentation"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.config = DocumentationConfig()
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        
    async def generate_documentation(self, topic: str, reasoning_effort: str = "balanced") -> Dict[str, Any]:
        """Generate comprehensive documentation for a topic"""
        try:
            # Generate documentation using GPT-4
            system_prompt = self._create_system_prompt()
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate documentation about: {topic}"}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            documentation = response.choices[0].message.content
            
            # Assess documentation quality
            quality_score = await self._assess_quality(documentation, topic)
            
            return {
                "documentation": documentation,
                "quality_score": quality_score,
                "format": self.config.format,
                "target_audience": self.config.target_audience.value
            }
        except Exception as e:
            logger.error(f"Error generating documentation: {str(e)}")
            return {"error": str(e)}

    def _create_system_prompt(self) -> str:
        """Create system prompt based on configuration"""
        prompt = f"""You are a technical documentation expert. Generate comprehensive documentation with the following characteristics:
- Target audience: {self.config.target_audience.value}
- Format: {self.config.format}
- Include examples: {self.config.include_examples}
- Focus on clarity and accuracy
- Structure the content logically
- Include code examples where relevant
- Use proper formatting and markdown
"""
        return prompt

    async def _assess_quality(self, documentation: str, topic: str) -> float:
        """Assess the quality of generated documentation"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Assess documentation quality on a scale of 0-1."},
                    {"role": "user", "content": f"Assess this documentation about {topic}:\n\n{documentation}"}
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            score_text = response.choices[0].message.content.strip()
            try:
                return float(score_text)
            except ValueError:
                return 0.5
        except Exception as e:
            logger.error(f"Error assessing documentation quality: {str(e)}")
            return 0.5

    async def execute(self, topic: str, reasoning_effort: str = "balanced") -> Dict[str, Any]:
        """Execute the documentation generation process"""
        return await self.generate_documentation(topic, reasoning_effort)
    
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
        if self.config.target_audience != TechnicalLevel.BEGINNER:
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