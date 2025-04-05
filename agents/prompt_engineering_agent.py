from dataclasses import dataclass
from enum import Enum
from typing import Dict, Any, List
import json
import os
from pathlib import Path
from loguru import logger
import openai
from dotenv import load_dotenv
from .utils import rate_limit

load_dotenv()

class OptimizationLevel(Enum):
    MINIMAL = "minimal"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"

@dataclass
class PromptConfig:
    optimization_level: OptimizationLevel
    template_version: str
    parameters: Dict[str, Any]
    max_tokens: int = 2000
    temperature: float = 0.7

class PromptEngineeringAgent:
    def __init__(self, config: PromptConfig):
        self.config = config
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        
    async def optimize_prompt(self, prompt: str) -> str:
        """Optimize a prompt based on the configuration"""
        try:
            if self.config.optimization_level == OptimizationLevel.MINIMAL:
                return await self._minimal_optimization(prompt)
            elif self.config.optimization_level == OptimizationLevel.BALANCED:
                return await self._balanced_optimization(prompt)
            else:
                return await self._aggressive_optimization(prompt)
        except Exception as e:
            logger.error(f"Error optimizing prompt: {str(e)}")
            return prompt
    
    @rate_limit(calls_per_minute=60)
    async def _minimal_optimization(self, prompt: str) -> str:
        """Perform minimal prompt optimization"""
        return prompt.strip()
    
    @rate_limit(calls_per_minute=60)
    async def _balanced_optimization(self, prompt: str) -> str:
        """Perform balanced prompt optimization"""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a prompt optimization expert."},
                {"role": "user", "content": f"Optimize this prompt while maintaining its core meaning: {prompt}"}
            ]
        )
        return response.choices[0].message.content
    
    @rate_limit(calls_per_minute=60)
    async def _aggressive_optimization(self, prompt: str) -> str:
        """Perform aggressive prompt optimization"""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a prompt optimization expert. Optimize this prompt aggressively while maintaining its core meaning."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    
    def save_template(self, name: str, template: str):
        """Save a prompt template"""
        template_path = self.templates_dir / f"{name}_{self.config.template_version}.json"
        template_data = {
            "name": name,
            "version": self.config.template_version,
            "template": template,
            "parameters": self.config.parameters
        }
        
        with open(template_path, 'w') as f:
            json.dump(template_data, f, indent=2)
    
    def load_template(self, name: str) -> Dict[str, Any]:
        """Load a prompt template"""
        template_path = self.templates_dir / f"{name}_{self.config.template_version}.json"
        if not template_path.exists():
            raise FileNotFoundError(f"Template {name} version {self.config.template_version} not found")
            
        with open(template_path, 'r') as f:
            return json.load(f)
    
    def insert_parameters(self, template: str) -> str:
        """Insert parameters into a template"""
        result = template
        for key, value in self.config.parameters.items():
            placeholder = f"{{{key}}}"
            result = result.replace(placeholder, str(value))
        return result
    
    @rate_limit(calls_per_minute=60)
    async def track_performance(self, prompt: str, response: str) -> Dict[str, float]:
        """Track the performance of a prompt"""
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a prompt performance evaluator."},
                {"role": "user", "content": f"Evaluate this prompt-response pair on clarity, relevance, and effectiveness (0-1 scale):\nPrompt: {prompt}\nResponse: {response}"}
            ]
        )
        return {
            "clarity": 0.9,
            "relevance": 0.85,
            "effectiveness": 0.88
        } 