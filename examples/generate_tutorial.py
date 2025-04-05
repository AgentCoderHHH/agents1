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
        content_filters=["tutorial", "guide", "how-to"],
        credibility_threshold=0.7
    )
    
    doc_config = DocumentationConfig(
        target_audience="developers",
        technical_level=TechnicalLevel.BEGINNER,
        format="markdown"
    )
    
    prompt_config = PromptConfig(
        optimization_level=OptimizationLevel.BALANCED,
        template_version="1.0",
        parameters={
            "style": "tutorial",
            "include_step_by_step": True,
            "include_practical_examples": True
        }
    )
    
    # Configure orchestrator
    orchestrator_config = OrchestratorConfig(
        execution_mode=ExecutionMode.SEQUENTIAL,
        context_sharing=True,
        error_handling=ErrorHandling.LENIENT
    )
    
    # Initialize orchestrator
    orchestrator = AgentOrchestrator(orchestrator_config)
    
    try:
        # Get topic from user input
        topic = input("Enter the tutorial topic (e.g., 'Python Async Programming'): ")
        
        print(f"\nGenerating tutorial for: {topic}")
        print("This may take a few minutes...\n")
        
        # Execute workflow
        result = await orchestrator.execute_workflow(
            topic=topic,
            web_config=web_config,
            doc_config=doc_config,
            prompt_config=prompt_config
        )
        
        # Print results
        print("\n=== Generated Tutorial ===")
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