from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any, Optional
import asyncio
from loguru import logger
import os
from dotenv import load_dotenv
from .internet_documentation_agent import InternetDocumentationAgent, WebResearchConfig
from .documentation_maker_agent import DocumentationMakerAgent, DocumentationConfig, TechnicalLevel
from .prompt_engineering_agent import PromptEngineeringAgent, PromptConfig, OptimizationLevel
from .error_handler import ErrorHandler, ErrorSeverity

load_dotenv()

class ExecutionMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"

class ErrorHandling(Enum):
    STRICT = "strict"
    LENIENT = "lenient"

@dataclass
class OrchestratorConfig:
    execution_mode: ExecutionMode
    context_sharing: bool
    error_handling: ErrorHandling
    max_retries: int = 3
    timeout: int = 300  # seconds

class AgentOrchestrator:
    def __init__(self, config: OrchestratorConfig):
        self.config = config
        self.agents = {}
        self.error_handler = ErrorHandler("AgentOrchestrator")
        self.initialize_agents()
        
    def initialize_agents(self):
        """Initialize all agents"""
        try:
            self.agents["internet"] = InternetDocumentationAgent(WebResearchConfig(
                search_engines=["google.com", "bing.com"],
                content_filters=["docs", "tutorial", "guide"],
                credibility_threshold=0.7
            ))
            
            self.agents["documentation"] = DocumentationMakerAgent(DocumentationConfig(
                target_audience="developers",
                technical_level=TechnicalLevel.INTERMEDIATE,
                format="markdown"
            ))
            
            self.agents["prompt"] = PromptEngineeringAgent(PromptConfig(
                optimization_level=OptimizationLevel.BALANCED,
                template_version="1.0",
                parameters={}
            ))
            
            for agent_name, agent in self.agents.items():
                try:
                    await agent.initialize()
                except Exception as e:
                    self.error_handler.handle_error(
                        e,
                        f"initialize_{agent_name}",
                        ErrorSeverity.ERROR,
                        {"agent_name": agent_name}
                    )
                    raise
                    
        except Exception as e:
            self.error_handler.handle_error(
                e,
                "initialize_agents",
                ErrorSeverity.CRITICAL
            )
            raise
            
    async def execute_workflow(self, topic: str) -> Dict[str, Any]:
        """Execute the documentation workflow"""
        result = {}
        
        try:
            if self.config.execution_mode == ExecutionMode.SEQUENTIAL:
                result = await self._execute_sequential(topic)
            else:
                result = await self._execute_parallel(topic)
                
        except Exception as e:
            error_context = self.error_handler.handle_error(
                e,
                "execute_workflow",
                ErrorSeverity.ERROR,
                {"topic": topic, "execution_mode": self.config.execution_mode}
            )
            
            if self.config.error_handling == ErrorHandling.STRICT:
                raise
            else:
                result["error"] = error_context
                
        return result
        
    async def _execute_sequential(self, topic: str) -> Dict[str, Any]:
        """Execute workflow in sequential mode"""
        result = {}
        
        try:
            # Research phase
            research = await self.agents["internet"].search_web(topic)
            result["research"] = research
            
            # Documentation generation
            documentation = await self.agents["documentation"].generate_documentation(topic, research)
            result["documentation"] = documentation
            
            # Prompt optimization
            optimized = await self.agents["prompt"].optimize_prompt(documentation)
            result["optimized"] = optimized
            
        except Exception as e:
            self.error_handler.handle_error(
                e,
                "execute_sequential",
                ErrorSeverity.ERROR,
                {"topic": topic}
            )
            raise
            
        return result
        
    async def _execute_parallel(self, topic: str) -> Dict[str, Any]:
        """Execute workflow in parallel mode"""
        result = {}
        
        try:
            tasks = [
                self.agents["internet"].search_web(topic),
                self.agents["documentation"].generate_documentation(topic, ""),
                self.agents["prompt"].optimize_prompt("")
            ]
            
            research, documentation, optimized = await asyncio.gather(*tasks)
            
            result["research"] = research
            result["documentation"] = documentation
            result["optimized"] = optimized
            
        except Exception as e:
            self.error_handler.handle_error(
                e,
                "execute_parallel",
                ErrorSeverity.ERROR,
                {"topic": topic}
            )
            raise
            
        return result
        
    async def cleanup(self):
        """Clean up resources"""
        try:
            for agent in self.agents.values():
                await agent.cleanup()
        except Exception as e:
            self.error_handler.handle_error(
                e,
                "cleanup",
                ErrorSeverity.WARNING
            ) 