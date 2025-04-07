from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import uvicorn
import os
from dotenv import load_dotenv

from .api.rest_api import app as rest_app
from .api.graphql_api import graphql_app

# Load environment variables
load_dotenv()

# Create main FastAPI app
app = FastAPI(title="Agent System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount REST API
app.mount("/api", rest_app)

# Mount GraphQL API
app.mount("/graphql", graphql_app)

@app.get("/")
async def root():
    return {
        "message": "Agent System API",
        "docs": {
            "rest": "/api/docs",
            "graphql": "/graphql"
        }
    }

if __name__ == "__main__":
    # Configure logging
    logger.add("logs/agent_system.log", rotation="1 day", retention="7 days")
    
    # Get port from environment variable or use default
    port = int(os.getenv("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        "agents.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    ) 