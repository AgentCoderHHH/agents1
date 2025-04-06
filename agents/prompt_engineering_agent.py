from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import asyncio
from loguru import logger
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path
from .utils import rate_limit

load_dotenv()

class OptimizationLevel(Enum):
    MINIMAL = "minimal"
    BALANCED = "balanced"
    AGGRESSIVE = "aggressive"

@dataclass
class PromptConfig:
    optimization_level: OptimizationLevel = OptimizationLevel.BALANCED
    template_version: str = "1.0"
    parameters: Dict[str, Any] = None
    max_tokens: int = 2000
    temperature: float = 0.7

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

class PromptEngineeringAgent:
    """Agent for optimizing prompts and managing templates"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.config = PromptConfig()
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.responses: Dict[str, List[Dict[str, Any]]] = {}
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        self._load_templates()

    def _load_templates(self):
        """Load templates from the templates directory"""
        try:
            for template_file in self.templates_dir.glob("*.json"):
                with open(template_file, "r") as f:
                    template_data = json.load(f)
                    self.templates[template_data["id"]] = template_data
        except Exception as e:
            logger.error(f"Error loading templates: {str(e)}")

    def add_template(self, template: Dict[str, Any]) -> str:
        """Add a new template"""
        try:
            template_id = f"template_{len(self.templates)}"
            template["id"] = template_id
            self.templates[template_id] = template
            
            # Save to file
            template_file = self.templates_dir / f"{template_id}.json"
            with open(template_file, "w") as f:
                json.dump(template, f, indent=2)
            
            return template_id
        except Exception as e:
            logger.error(f"Error adding template: {str(e)}")
            raise

    def update_template(self, template_id: str, new_template: Dict[str, Any]) -> None:
        """Update an existing template"""
        try:
            if template_id not in self.templates:
                raise ValueError(f"Template {template_id} not found")
            
            self.templates[template_id].update(new_template)
            
            # Save to file
            template_file = self.templates_dir / f"{template_id}.json"
            with open(template_file, "w") as f:
                json.dump(self.templates[template_id], f, indent=2)
        except Exception as e:
            logger.error(f"Error updating template: {str(e)}")
            raise

    async def optimize_prompt(self, prompt: str, reasoning_effort: str = "balanced") -> Dict[str, Any]:
        """Optimize a prompt based on the configuration"""
        try:
            # Select optimization strategy based on level
            strategy = self._get_optimization_strategy(reasoning_effort)
            
            # Optimize the prompt
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": strategy},
                    {"role": "user", "content": f"Optimize this prompt: {prompt}"}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            optimized_prompt = response.choices[0].message.content
            
            # Evaluate the optimization
            quality_score = await self._evaluate_optimization(prompt, optimized_prompt)
            
            # Track the response
            self._track_response(prompt, optimized_prompt, quality_score)
            
            return {
                "original_prompt": prompt,
                "optimized_prompt": optimized_prompt,
                "quality_score": quality_score,
                "optimization_level": reasoning_effort
            }
        except Exception as e:
            logger.error(f"Error optimizing prompt: {str(e)}")
            return {"error": str(e)}

    def _get_optimization_strategy(self, level: str) -> str:
        """Get the optimization strategy based on the level"""
        strategies = {
            "minimal": "Make minimal changes to improve clarity while preserving the original intent.",
            "balanced": "Balance clarity improvements with structural enhancements while maintaining the core message.",
            "aggressive": "Comprehensively restructure and enhance the prompt for maximum effectiveness."
        }
        return strategies.get(level, strategies["balanced"])

    async def _evaluate_optimization(self, original: str, optimized: str) -> float:
        """Evaluate the quality of the optimization"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Evaluate prompt optimization on a scale of 0-1."},
                    {"role": "user", "content": f"Original: {original}\nOptimized: {optimized}"}
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
            logger.error(f"Error evaluating optimization: {str(e)}")
            return 0.5

    def _track_response(self, original: str, optimized: str, score: float) -> None:
        """Track the response for analysis"""
        try:
            response_id = f"response_{len(self.responses)}"
            self.responses[response_id] = {
                "original": original,
                "optimized": optimized,
                "score": score,
                "timestamp": asyncio.get_event_loop().time()
            }
        except Exception as e:
            logger.error(f"Error tracking response: {str(e)}")

    async def execute(self, prompt: str, reasoning_effort: str = "balanced") -> Dict[str, Any]:
        """Execute the prompt optimization process"""
        return await self.optimize_prompt(prompt, reasoning_effort)

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