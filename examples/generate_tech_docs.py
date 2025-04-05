#!/usr/bin/env python3
import asyncio
import os
from dotenv import load_dotenv
from agents.agent_orchestrator import AgentOrchestrator, OrchestratorConfig, ExecutionMode, ErrorHandling
from agents.documentation_maker_agent import DocumentationConfig, TechnicalLevel
from agents.prompt_engineering_agent import PromptConfig, OptimizationLevel
from agents.web_research_agent import WebResearchConfig

async def main():
    # Load environment variables
    load_dotenv()
    
    # Configure agents
    web_config = WebResearchConfig(
        search_engines=["google", "bing"],
        content_filters=["documentation", "reference", "guide"],
        credibility_threshold=0.8
    )
    
    doc_config = DocumentationConfig(
        target_audience="developers",
        technical_level=TechnicalLevel.ADVANCED,
        format="markdown"
    )
    
    prompt_config = PromptConfig(
        optimization_level=OptimizationLevel.AGGRESSIVE,
        template_version="1.0",
        parameters={
            "style": "technical",
            "include_api_reference": True,
            "include_best_practices": True,
            "include_performance_considerations": True
        }
    )
    
    # Configure orchestrator
    orchestrator_config = OrchestratorConfig(
        execution_mode=ExecutionMode.PARALLEL,
        context_sharing=True,
        error_handling=ErrorHandling.STRICT
    )
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(orchestrator_config)
    
    try:
        # Get topic from user input
        topic = input("Enter the technology to document (e.g., 'FastAPI', 'React', 'TensorFlow'): ")
        
        print(f"\nGenerating technical documentation for: {topic}")
        print("This may take a few minutes...\n")
        
        # Execute workflow
        result = await orchestrator.execute_workflow(
            topic=topic,
            web_config=web_config,
            doc_config=doc_config,
            prompt_config=prompt_config
        )
        
        # Print results
        print("\n=== Generated Technical Documentation ===")
        print(result["documentation"])
        
        # Print metrics
        print("\n=== Performance Metrics ===")
        print(f"Research time: {result['metrics']['research_time']:.2f}s")
        print(f"Documentation time: {result['metrics']['documentation_time']:.2f}s")
        print(f"Total time: {result['metrics']['total_time']:.2f}s")
        
    except Exception as e:
        print(f"\nError: {str(e)}")
    finally:
        await orchestrator.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 