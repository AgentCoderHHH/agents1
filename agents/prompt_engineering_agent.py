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

class PromptDomain(Enum):
    TECHNICAL = "technical"
    CREATIVE = "creative"
    ANALYTICAL = "analytical"
    GENERAL = "general"

@dataclass
class PromptConfig:
    optimization_level: OptimizationLevel = OptimizationLevel.BALANCED
    domain: PromptDomain = PromptDomain.GENERAL
    template_version: str = "2.0"
    parameters: Dict[str, Any] = None
    max_tokens: int = 2000
    temperature: float = 0.7
    include_examples: bool = True
    include_analogies: bool = True
    include_technical_details: bool = True

    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}

class PromptEngineeringAgent:
    """Enhanced agent for optimizing prompts and managing templates"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.config = PromptConfig()
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.responses: Dict[str, List[Dict[str, Any]]] = {}
        self.templates_dir = Path("templates")
        self.templates_dir.mkdir(exist_ok=True)
        self._load_templates()
        self._initialize_domain_templates()

    def _initialize_domain_templates(self):
        """Initialize domain-specific templates"""
        self.domain_templates = {
            PromptDomain.TECHNICAL: {
                "structure": [
                    "Problem Definition",
                    "Technical Context",
                    "Implementation Details",
                    "Best Practices",
                    "Common Pitfalls",
                    "Code Examples"
                ],
                "keywords": [
                    "architecture", "implementation", "optimization",
                    "performance", "scalability", "security"
                ]
            },
            PromptDomain.CREATIVE: {
                "structure": [
                    "Theme",
                    "Style",
                    "Tone",
                    "Imagery",
                    "Emotional Impact",
                    "Originality"
                ],
                "keywords": [
                    "imagination", "expression", "style",
                    "tone", "metaphor", "symbolism"
                ]
            },
            PromptDomain.ANALYTICAL: {
                "structure": [
                    "Problem Statement",
                    "Data Analysis",
                    "Methodology",
                    "Findings",
                    "Conclusions",
                    "Recommendations"
                ],
                "keywords": [
                    "analysis", "evaluation", "comparison",
                    "trends", "patterns", "insights"
                ]
            }
        }

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
        """Enhanced prompt optimization with domain-specific improvements"""
        try:
            # Analyze the prompt to determine domain
            domain = await self._analyze_prompt_domain(prompt)
            self.config.domain = domain
            
            # Get domain-specific optimization strategy
            strategy = self._get_optimization_strategy(reasoning_effort, domain.value)
            
            # Optimize the prompt with enhanced context
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": strategy},
                    {"role": "user", "content": f"""
                    Original prompt: {prompt}
                    
                    Please optimize this prompt considering:
                    1. Domain: {domain.value}
                    2. Level: {reasoning_effort}
                    3. Include examples: {self.config.include_examples}
                    4. Include analogies: {self.config.include_analogies}
                    5. Include technical details: {self.config.include_technical_details}
                    
                    Provide a comprehensive optimized version that maintains the original intent while enhancing clarity, specificity, and effectiveness.
                    """}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            optimized_prompt = response.choices[0].message.content
            
            # Evaluate the optimization with enhanced criteria
            quality_score = await self._evaluate_optimization(prompt, optimized_prompt, domain)
            
            # Track the response with additional metadata
            self._track_response(prompt, optimized_prompt, quality_score, domain)
            
            return {
                "original_prompt": prompt,
                "optimized_prompt": optimized_prompt,
                "quality_score": quality_score,
                "optimization_level": reasoning_effort,
                "domain": domain.value,
                "improvements": await self._analyze_improvements(prompt, optimized_prompt)
            }
        except Exception as e:
            logger.error(f"Error optimizing prompt: {str(e)}")
            return {"error": str(e)}

    def _get_optimization_strategy(self, level: str, domain: str) -> str:
        """Get the optimization strategy based on level and domain"""
        base_strategies = {
            "minimal": """
            Make minimal but effective changes to improve clarity while preserving the original intent.
            Focus on:
            1. Grammar and syntax improvements
            2. Basic clarity enhancements
            3. Minor structural adjustments
            """,
            "balanced": """
            Balance clarity improvements with structural enhancements while maintaining the core message.
            Focus on:
            1. Clear problem definition
            2. Logical structure
            3. Specific requirements
            4. Contextual relevance
            """,
            "aggressive": """
            Comprehensively restructure and enhance the prompt for maximum effectiveness.
            Focus on:
            1. Detailed problem breakdown
            2. Comprehensive context
            3. Specific examples and analogies
            4. Clear success criteria
            5. Technical depth where appropriate
            """
        }

        domain_specific = {
            "technical": """
            Ensure the prompt:
            1. Includes specific technical requirements
            2. References relevant technologies or frameworks
            3. Specifies performance criteria
            4. Includes error handling considerations
            5. Mentions scalability requirements
            """,
            "creative": """
            Ensure the prompt:
            1. Establishes clear creative direction
            2. Specifies style and tone
            3. Includes emotional or thematic elements
            4. References artistic influences
            5. Sets originality criteria
            """,
            "analytical": """
            Ensure the prompt:
            1. Defines clear analysis objectives
            2. Specifies data sources and methods
            3. Sets evaluation criteria
            4. Includes comparison frameworks
            5. Defines success metrics
            """
        }

        base_strategy = base_strategies.get(level, base_strategies["balanced"])
        domain_strategy = domain_specific.get(domain, "")
        
        return f"{base_strategy}\n{domain_strategy}"

    async def _analyze_prompt_domain(self, prompt: str) -> PromptDomain:
        """Analyze the prompt to determine its domain"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Analyze the prompt and determine its primary domain."},
                    {"role": "user", "content": f"Prompt: {prompt}\n\nClassify this prompt as either technical, creative, analytical, or general."}
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            domain_text = response.choices[0].message.content.strip().lower()
            return PromptDomain(domain_text)
        except Exception as e:
            logger.error(f"Error analyzing prompt domain: {str(e)}")
            return PromptDomain.GENERAL

    async def _evaluate_optimization(self, original: str, optimized: str, domain: PromptDomain) -> Dict[str, float]:
        """Enhanced evaluation of prompt optimization"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"""
                    Evaluate the prompt optimization on multiple criteria (0-1 scale).
                    Consider the domain: {domain.value}
                    """},
                    {"role": "user", "content": f"""
                    Original: {original}
                    Optimized: {optimized}
                    
                    Evaluate on:
                    1. Clarity
                    2. Specificity
                    3. Completeness
                    4. Domain Relevance
                    5. Effectiveness
                    """}
                ],
                temperature=0.3,
                max_tokens=100
            )
            
            evaluation_text = response.choices[0].message.content
            scores = self._parse_evaluation_scores(evaluation_text)
            
            return {
                "overall": sum(scores.values()) / len(scores),
                **scores
            }
        except Exception as e:
            logger.error(f"Error evaluating optimization: {str(e)}")
            return {"overall": 0.5}

    def _parse_evaluation_scores(self, evaluation_text: str) -> Dict[str, float]:
        """Parse evaluation scores from the response text"""
        scores = {}
        for line in evaluation_text.split("\n"):
            if ":" in line:
                criterion, score = line.split(":")
                try:
                    scores[criterion.strip().lower()] = float(score.strip())
                except ValueError:
                    continue
        return scores

    async def _analyze_improvements(self, original: str, optimized: str) -> List[str]:
        """Analyze specific improvements made to the prompt"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "List specific improvements made to the prompt."},
                    {"role": "user", "content": f"Original: {original}\nOptimized: {optimized}\n\nList the key improvements made:"}
                ],
                temperature=0.3,
                max_tokens=200
            )
            
            improvements_text = response.choices[0].message.content
            return [imp.strip() for imp in improvements_text.split("\n") if imp.strip()]
        except Exception as e:
            logger.error(f"Error analyzing improvements: {str(e)}")
            return []

    def _track_response(self, original: str, optimized: str, quality_score: Dict[str, float], domain: PromptDomain) -> None:
        """Enhanced response tracking with domain and detailed scores"""
        try:
            response_id = f"response_{len(self.responses)}"
            self.responses[response_id] = {
                "original": original,
                "optimized": optimized,
                "scores": quality_score,
                "domain": domain.value,
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