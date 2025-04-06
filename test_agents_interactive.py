from agents import (
    InternetDocumentationAgent,
    DocumentationMakerAgent,
    PromptEngineeringAgent,
    AgentOrchestrator
)
from loguru import logger
import asyncio
import json

async def test_internet_documentation_agent():
    """Test the InternetDocumentationAgent with user input"""
    logger.info("\n=== Testing InternetDocumentationAgent ===")
    agent = InternetDocumentationAgent()
    
    topic = input("\nEnter a topic to research: ")
    logger.info(f"Researching topic: {topic}")
    
    try:
        results = await agent.research_topic(topic)
        logger.info("\nResearch Results:")
        for idx, result in enumerate(results, 1):
            logger.info(f"\nResult {idx}:")
            logger.info(f"Title: {result['title']}")
            logger.info(f"URL: {result['url']}")
            logger.info(f"Credibility: {result['credibility']}")
            logger.info(f"Relevance: {result['relevance']}")
            logger.info(f"Summary: {result['summary']}")
    except Exception as e:
        logger.error(f"Error during research: {str(e)}")

async def test_documentation_maker_agent():
    """Test the DocumentationMakerAgent with user input"""
    logger.info("\n=== Testing DocumentationMakerAgent ===")
    agent = DocumentationMakerAgent()
    
    topic = input("\nEnter a topic for documentation: ")
    logger.info(f"Generating documentation for: {topic}")
    
    try:
        docs = await agent.generate_documentation(topic)
        logger.info("\nGenerated Documentation:")
        logger.info(f"Title: {docs['title']}")
        logger.info(f"Content: {docs['content']}")
        logger.info(f"Quality Score: {docs['quality_score']}")
    except Exception as e:
        logger.error(f"Error generating documentation: {str(e)}")

async def test_prompt_engineering_agent():
    """Test the PromptEngineeringAgent with user input"""
    logger.info("\n=== Testing PromptEngineeringAgent ===")
    agent = PromptEngineeringAgent()
    
    prompt = input("\nEnter a prompt to optimize: ")
    logger.info(f"Optimizing prompt: {prompt}")
    
    try:
        optimized = await agent.optimize_prompt(prompt)
        logger.info("\nOptimized Prompt:")
        logger.info(f"Original: {prompt}")
        logger.info(f"Optimized: {optimized['prompt']}")
        logger.info(f"Optimization Score: {optimized['score']}")
    except Exception as e:
        logger.error(f"Error optimizing prompt: {str(e)}")

async def test_agent_orchestrator():
    """Test the AgentOrchestrator with user input"""
    logger.info("\n=== Testing AgentOrchestrator ===")
    orchestrator = AgentOrchestrator()
    
    topic = input("\nEnter a topic for orchestrated research: ")
    logger.info(f"Orchestrating research for: {topic}")
    
    try:
        result = await orchestrator.orchestrate_research(topic)
        logger.info("\nOrchestrated Research Results:")
        logger.info(f"Research Quality: {result['research_quality']}")
        logger.info(f"Documentation Quality: {result['documentation_quality']}")
        logger.info(f"Prompt Optimization Score: {result['prompt_optimization_score']}")
        logger.info("\nFinal Documentation:")
        logger.info(json.dumps(result['final_documentation'], indent=2))
    except Exception as e:
        logger.error(f"Error during orchestration: {str(e)}")

async def main():
    """Run interactive agent tests"""
    while True:
        print("\n=== Agent Testing Menu ===")
        print("1. Test InternetDocumentationAgent")
        print("2. Test DocumentationMakerAgent")
        print("3. Test PromptEngineeringAgent")
        print("4. Test AgentOrchestrator")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            await test_internet_documentation_agent()
        elif choice == "2":
            await test_documentation_maker_agent()
        elif choice == "3":
            await test_prompt_engineering_agent()
        elif choice == "4":
            await test_agent_orchestrator()
        elif choice == "5":
            logger.info("Exiting...")
            break
        else:
            logger.warning("Invalid choice. Please try again.")

if __name__ == "__main__":
    asyncio.run(main()) 