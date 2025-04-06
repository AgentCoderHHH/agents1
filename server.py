from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uvicorn
from loguru import logger
from agents.agent_orchestrator import AgentOrchestrator
import asyncio
import os
from dotenv import load_dotenv

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
orchestrator = AgentOrchestrator()

class ExecuteRequest(BaseModel):
    topic: str
    agent_type: Optional[str] = None
    reasoning_effort: Optional[str] = "balanced"
    parameters: Optional[Dict[str, Any]] = None
    parallel_tasks: Optional[List[Dict[str, Any]]] = None

class ExecuteResponse(BaseModel):
    success: bool
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize agents on startup"""
    try:
        await orchestrator.initialize()
        logger.info("Agents initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing agents: {str(e)}")
        raise

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {"message": "API is working"}

@app.post("/execute", response_model=ExecuteResponse)
async def execute_agent(request: ExecuteRequest):
    """Execute an agent or multiple agents with the given topic and parameters"""
    try:
        context = orchestrator.create_context(request.topic)
        
        if request.parallel_tasks:
            # Execute multiple agents in parallel
            results = await orchestrator.execute_parallel(context, request.parallel_tasks)
        elif request.agent_type:
            # Execute a single agent
            if request.agent_type not in orchestrator.agents:
                raise HTTPException(status_code=400, detail="Invalid agent type")
            
            agent = orchestrator.agents[request.agent_type]
            if request.agent_type == "research":
                results = await agent.research_topic(request.topic)
            elif request.agent_type == "documentation":
                results = await agent.generate_documentation(request.topic)
            elif request.agent_type == "prompt":
                results = await agent.optimize_prompt(request.topic)
            else:
                raise HTTPException(status_code=400, detail="Invalid agent type")
        else:
            # Execute the full workflow
            results = await orchestrator.execute_workflow(request.topic)
        
        return ExecuteResponse(
            success=True,
            result=results
        )
    except Exception as e:
        logger.error(f"Error executing agent: {str(e)}")
        return ExecuteResponse(
            success=False,
            error=str(e)
        )

if __name__ == "__main__":
    # Get port from environment variable, default to 3001 if not set
    port = int(os.getenv("PORT", 3001))
    logger.info(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 