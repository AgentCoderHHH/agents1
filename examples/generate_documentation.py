import asyncio
import os
from dotenv import load_dotenv
from agents import (
    AgentOrchestrator,
    OrchestratorConfig,
    ExecutionMode,
    ErrorHandling,
    WebResearchConfig,
    DocumentationConfig,
    TechnicalLevel,
    PromptConfig,
    OptimizationLevel
)

load_dotenv()

async def main():
    # Configure the orchestrator
    orchestrator_config = OrchestratorConfig(
        execution_mode=ExecutionMode.PARALLEL,
        context_sharing=True,
        error_handling=ErrorHandling.LENIENT
    )
    
    # Create the orchestrator
    orchestrator = AgentOrchestrator(orchestrator_config)
    
    try:
        # Example topic
        topic = "Python Async Programming"
        
        # Execute the workflow
        result = await orchestrator.execute_workflow(topic)
        
        # Print results
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print("Documentation generated successfully!")
            print(f"Research content length: {len(result.get('research', ''))} characters")
            print(f"Documentation length: {len(result.get('documentation', ''))} characters")
            
    finally:
        # Clean up resources
        await orchestrator.cleanup()

if __name__ == "__main__":
    asyncio.run(main()) 