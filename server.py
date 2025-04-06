from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
from loguru import logger
import asyncio
from agents.agent_orchestrator import AgentOrchestrator, OrchestratorConfig, OrchestratorMode
import os
from dotenv import load_dotenv
import json
import uvicorn

# Load environment variables
load_dotenv()

app = FastAPI(
    title="AgentOpenAPI",
    description="API for AI-powered documentation and research agents",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = AgentOrchestrator(
    config=OrchestratorConfig(
        mode=OrchestratorMode.SEQUENTIAL,
        max_retries=3,
        timeout_seconds=300,
        max_concurrent_tasks=3
    )
)

class ExecuteRequest(BaseModel):
    topic: str
    reasoning_effort: Optional[str] = "balanced"

class TestResponse(BaseModel):
    message: str

class HealthResponse(BaseModel):
    status: str

@app.on_event("startup")
async def startup_event():
    """Initialize agents on startup"""
    try:
        await orchestrator.initialize()
        logger.info("Agents initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing agents: {str(e)}")
        raise

def format_response_for_terminal(result: Dict[str, Any]) -> str:
    """Format the response for terminal display"""
    output = []
    
    # Research Agent Response
    if "research" in result:
        output.append("\n=== Research Agent Response ===")
        research = result["research"]
        if isinstance(research, dict):
            for key, value in research.items():
                if key == "overview":
                    output.append(f"\nOverview:\n{value}")
                elif key == "sections":
                    output.append("\nSections:")
                    for section in value:
                        output.append(f"- {section}")
                elif key == "examples":
                    output.append("\nExamples:")
                    for example in value:
                        output.append(f"- {example}")
                elif key == "references":
                    output.append("\nReferences:")
                    for ref in value:
                        output.append(f"- {ref}")
    
    # Documentation Agent Response
    if "documentation" in result:
        output.append("\n=== Documentation Agent Response ===")
        doc = result["documentation"]
        if isinstance(doc, dict):
            output.append(f"\nDocumentation (Quality Score: {doc.get('quality_score', 'N/A')}):")
            output.append(doc.get("documentation", ""))
    
    # Prompt Engineering Agent Response
    if "optimized_prompts" in result:
        output.append("\n=== Prompt Engineering Agent Response ===")
        prompts = result["optimized_prompts"]
        if isinstance(prompts, dict):
            output.append(f"\nOriginal Prompt: {prompts.get('original_prompt', 'N/A')}")
            output.append(f"Optimized Prompt: {prompts.get('optimized_prompt', 'N/A')}")
            output.append(f"Quality Score: {prompts.get('quality_score', 'N/A')}")
            output.append(f"Optimization Level: {prompts.get('optimization_level', 'N/A')}")
    
    return "\n".join(output)

@app.post("/execute")
async def execute(request: ExecuteRequest) -> Dict[str, Any]:
    """Execute the multi-agent workflow"""
    try:
        # Execute workflow
        result = await orchestrator.execute_workflow(
            request.topic,
            reasoning_effort=request.reasoning_effort
        )
        
        # Format and print the response
        formatted_response = format_response_for_terminal(result)
        print(formatted_response)
        
        return {
            "success": True,
            "result": result,
            "error": None
        }
    except Exception as e:
        logger.error(f"Error executing workflow: {str(e)}")
        return {
            "success": False,
            "result": None,
            "error": str(e)
        }

@app.get("/test")
async def test() -> TestResponse:
    """Test endpoint"""
    return TestResponse(message="API is working")

@app.get("/health")
async def health() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse(status="healthy")

if __name__ == "__main__":
    # Get port from environment variable, default to 3001 if not set
    port = int(os.getenv("PORT", 3001))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 