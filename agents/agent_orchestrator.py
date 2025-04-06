from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from loguru import logger
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json
from pathlib import Path

from .internet_documentation_agent import InternetDocumentationAgent
from .documentation_maker_agent import DocumentationMakerAgent
from .prompt_engineering_agent import PromptEngineeringAgent

# Load environment variables
load_dotenv()

class OrchestratorMode(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    ADAPTIVE = "adaptive"

@dataclass
class OrchestratorConfig:
    mode: OrchestratorMode = OrchestratorMode.SEQUENTIAL
    max_retries: int = 3
    timeout_seconds: int = 300
    max_concurrent_tasks: int = 3

@dataclass
class RunContext:
    topic: str
    start_time: float
    parent_context: Optional['RunContext'] = None
    metadata: Dict[str, Any] = None

class AgentOrchestrator:
    def __init__(self, config: Optional[OrchestratorConfig] = None):
        self.config = config or OrchestratorConfig()
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.agents = {}
        self.execution_history = []
        self.context_store: Dict[str, RunContext] = {}
        self.execution_queue: List[Dict[str, Any]] = []

    async def initialize(self):
        """Initialize all agents."""
        try:
            # Initialize research agent
            self.agents["research"] = InternetDocumentationAgent()
            
            # Initialize documentation agent
            self.agents["documentation"] = DocumentationMakerAgent()
            
            # Initialize prompt engineering agent
            self.agents["prompt"] = PromptEngineeringAgent()
            
            logger.info("All agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing agents: {str(e)}")
            raise

    async def execute_workflow(self, topic: str, reasoning_effort: str = "balanced") -> Dict[str, Any]:
        """Execute the complete research and documentation workflow."""
        try:
            # Initialize agents if not already done
            if not self.agents:
                await self.initialize()
            
            # Step 1: Research the topic
            logger.info(f"Starting research on topic: {topic}")
            research_results = await self.agents["research"].research_topic(topic)
            
            # Step 2: Generate documentation
            logger.info("Generating documentation")
            documentation = await self.agents["documentation"].generate_documentation(topic)
            
            # Step 3: Optimize prompts
            logger.info("Optimizing prompts")
            optimized_prompts = await self.agents["prompt"].optimize_prompt(
                f"Explain {topic} in detail",
                reasoning_effort=reasoning_effort
            )
            
            # Combine results
            workflow_results = {
                "topic": topic,
                "research": research_results,
                "documentation": documentation,
                "optimized_prompts": optimized_prompts
            }
            
            # Store execution history
            self.execution_history.append(workflow_results)
            
            return workflow_results
            
        except Exception as e:
            logger.error(f"Error in workflow execution: {str(e)}")
            return {
                "error": str(e),
                "topic": topic,
                "research": None,
                "documentation": None,
                "optimized_prompts": None
            }

    async def get_execution_status(self) -> Dict[str, Any]:
        """Get the status of all executions."""
        return {
            "total_executions": len(self.execution_history),
            "latest_execution": self.execution_history[-1] if self.execution_history else None,
            "agent_status": {
                name: "initialized" if agent else "not_initialized"
                for name, agent in self.agents.items()
            }
        }

    async def cleanup(self):
        """Clean up resources."""
        try:
            for agent in self.agents.values():
                if hasattr(agent, 'cleanup'):
                    await agent.cleanup()
            logger.info("Cleanup completed successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")
            raise

    def create_context(self, topic: str, parent_context: Optional[RunContext] = None) -> RunContext:
        """Create a new execution context."""
        import time
        context = RunContext(
            topic=topic,
            start_time=time.time(),
            parent_context=parent_context,
            metadata={}
        )
        self.context_store[topic] = context
        return context

    async def execute_parallel(self, context: RunContext, plans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Execute multiple agents in parallel"""
        tasks = []
        for plan in plans:
            agent_type = plan.get("agent_type")
            if agent_type not in self.agents:
                logger.error(f"Unknown agent type: {agent_type}")
                continue

            agent = self.agents[agent_type]
            task = agent.execute(
                context.topic,
                plan.get("reasoning_effort", "balanced")
            )
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        execution_results = {}
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Error in parallel execution: {str(result)}")
                execution_results[f"task_{i}"] = {"error": str(result)}
            else:
                execution_results[f"task_{i}"] = {"result": result}

        return execution_results

    async def orchestrate_llm(self, context: RunContext) -> Dict[str, Any]:
        """Orchestrate LLM-based execution flow"""
        # First, research the topic
        research_results = await self.agents["research"].execute(
            context.topic,
            "balanced"
        )
        
        # Then, generate documentation
        documentation = await self.agents["documentation"].execute(
            context.topic,
            "balanced"
        )
        
        # Finally, optimize the documentation
        optimized = await self.agents["prompt"].execute(
            documentation,
            "balanced"
        )

        return {
            "research": research_results,
            "documentation": documentation,
            "optimized": optimized
        }

    async def evaluate_execution(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the success of an execution"""
        success = all(
            not isinstance(result.get("error"), str)
            for result in results.values()
        )
        
        return {
            "success": success,
            "results": results
        } 