from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from loguru import logger

from ..security.auth import AuthManager, User, Token
from ..agent_orchestrator import AgentOrchestrator
from ..data_sources.mongodb_source import MongoDBDataSource
from ..data_sources.postgresql_source import PostgreSQLDataSource

app = FastAPI(title="Agent System API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
auth_manager = AuthManager()
orchestrator = AgentOrchestrator()
mongodb = MongoDBDataSource()
postgresql = PostgreSQLDataSource()

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Models
class GoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"
    due_date: Optional[datetime] = None
    priority: str = "medium"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    goal_id: str
    assignee: Optional[str] = None
    due_date: Optional[datetime] = None
    dependencies: Optional[List[str]] = None

class ProgressCreate(BaseModel):
    goal_id: str
    status: str
    progress: float
    notes: Optional[str] = None

# Dependency to get current user
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = auth_manager.verify_token(token)
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    user = auth_manager.get_user(username)
    if user is None:
        raise credentials_exception
    
    return user

# Authentication endpoints
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth_manager.create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Goal endpoints
@app.post("/goals", response_model=Dict[str, Any])
async def create_goal(
    goal: GoalCreate,
    current_user: User = Depends(get_current_user)
):
    if not auth_manager.has_permission(current_user, "write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        goal_data = goal.dict()
        goal_data["id"] = str(datetime.utcnow().timestamp())
        result = await mongodb.insert("goals", goal_data)
        return {"id": result, "message": "Goal created successfully"}
    except Exception as e:
        logger.error(f"Error creating goal: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating goal"
        )

@app.get("/goals", response_model=List[Dict[str, Any]])
async def get_goals(
    current_user: User = Depends(get_current_user)
):
    if not auth_manager.has_permission(current_user, "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        goals = await mongodb.query("goals", {})
        return goals
    except Exception as e:
        logger.error(f"Error getting goals: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting goals"
        )

# Task endpoints
@app.post("/tasks", response_model=Dict[str, Any])
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    if not auth_manager.has_permission(current_user, "write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        task_data = task.dict()
        task_data["id"] = str(datetime.utcnow().timestamp())
        task_data["status"] = "pending"
        result = await postgresql.insert("tasks", task_data)
        return {"id": result, "message": "Task created successfully"}
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating task"
        )

@app.get("/tasks", response_model=List[Dict[str, Any]])
async def get_tasks(
    current_user: User = Depends(get_current_user)
):
    if not auth_manager.has_permission(current_user, "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        tasks = await postgresql.query("tasks", {})
        return tasks
    except Exception as e:
        logger.error(f"Error getting tasks: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting tasks"
        )

# Progress endpoints
@app.post("/progress", response_model=Dict[str, Any])
async def create_progress(
    progress: ProgressCreate,
    current_user: User = Depends(get_current_user)
):
    if not auth_manager.has_permission(current_user, "write"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        progress_data = progress.dict()
        progress_data["id"] = str(datetime.utcnow().timestamp())
        progress_data["timestamp"] = datetime.utcnow()
        result = await postgresql.insert("progress", progress_data)
        return {"id": result, "message": "Progress recorded successfully"}
    except Exception as e:
        logger.error(f"Error recording progress: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error recording progress"
        )

@app.get("/progress/{goal_id}", response_model=List[Dict[str, Any]])
async def get_progress(
    goal_id: str,
    current_user: User = Depends(get_current_user)
):
    if not auth_manager.has_permission(current_user, "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        progress = await postgresql.query("progress", {"goal_id": goal_id})
        return progress
    except Exception as e:
        logger.error(f"Error getting progress: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting progress"
        )

# Agent endpoints
@app.post("/execute", response_model=Dict[str, Any])
async def execute_workflow(
    topic: str,
    reasoning_effort: str = "balanced",
    current_user: User = Depends(get_current_user)
):
    if not auth_manager.has_permission(current_user, "execute"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        results = await orchestrator.execute_workflow(topic, reasoning_effort)
        return results
    except Exception as e:
        logger.error(f"Error executing workflow: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error executing workflow"
        )

@app.get("/status", response_model=Dict[str, Any])
async def get_system_status(
    current_user: User = Depends(get_current_user)
):
    if not auth_manager.has_permission(current_user, "read"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    try:
        status = await orchestrator.get_execution_status()
        return status
    except Exception as e:
        logger.error(f"Error getting system status: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error getting system status"
        )

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    await orchestrator.initialize()
    await mongodb.connect()
    await postgresql.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await orchestrator.cleanup()
    await mongodb.close()
    await postgresql.close() 