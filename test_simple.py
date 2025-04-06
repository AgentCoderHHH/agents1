import asyncio
from agents import (
    InternetDocumentationAgent,
    DocumentationMakerAgent,
    PromptEngineeringAgent
)
from loguru import logger

async def main():
    # Test InternetDocumentationAgent
    logger.info("Testing InternetDocumentationAgent...")
    research_agent = InternetDocumentationAgent()
    results = await research_agent.research_topic("Python async programming")
    logger.info("Research Results:")
    logger.info(results)

    # Test DocumentationMakerAgent
    logger.info("\nTesting DocumentationMakerAgent...")
    doc_agent = DocumentationMakerAgent()
    docs = await doc_agent.generate_documentation("Python async programming")
    logger.info("Documentation:")
    logger.info(docs)

    # Test PromptEngineeringAgent
    logger.info("\nTesting PromptEngineeringAgent...")
    prompt_agent = PromptEngineeringAgent()
    optimized = await prompt_agent.optimize_prompt("Explain Python async programming")
    logger.info("Optimized Prompt:")
    logger.info(optimized)

if __name__ == "__main__":
    asyncio.run(main()) 