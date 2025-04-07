from typing import Dict, Any, List, Optional
from strawberry import Schema, Query, Mutation, type
from strawberry.fastapi import GraphQLRouter
from datetime import datetime
from loguru import logger

from ..security.auth import AuthManager, User
from ..agent_orchestrator import AgentOrchestrator
from ..data_sources.mongodb_source import MongoDBDataSource
from ..data_sources.postgresql_source import PostgreSQLDataSource

# Initialize components
auth_manager = AuthManager()
orchestrator = AgentOrchestrator()
mongodb = MongoDBDataSource()
postgresql = PostgreSQLDataSource()

# Types
@type
class Goal:
    id: str
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]
    priority: str

@type
class Task:
    id: str
    title: str
    description: Optional[str]
    status: str
    goal_id: str
    assignee: Optional[str]
    created_at: datetime
    updated_at: datetime
    due_date: Optional[datetime]
    dependencies: Optional[List[str]]

@type
class Progress:
    id: str
    goal_id: str
    status: str
    progress: float
    timestamp: datetime
    notes: Optional[str]

@type
class WorkflowResult:
    topic: str
    research: Dict[str, Any]
    documentation: Dict[str, Any]
    optimized_prompts: Dict[str, Any]
    analytics: Dict[str, Any]
    progress: Dict[str, Any]
    alignment: Dict[str, Any]
    tasks: Dict[str, Any]

@type
class SystemStatus:
    total_executions: int
    latest_execution: Optional[WorkflowResult]
    agent_status: Dict[str, str]
    data_hub_status: str

# Query type
class Query:
    @staticmethod
    async def goals() -> List[Goal]:
        try:
            goals_data = await mongodb.query("goals", {})
            return [Goal(**goal) for goal in goals_data]
        except Exception as e:
            logger.error(f"Error getting goals: {str(e)}")
            raise

    @staticmethod
    async def tasks() -> List[Task]:
        try:
            tasks_data = await postgresql.query("tasks", {})
            return [Task(**task) for task in tasks_data]
        except Exception as e:
            logger.error(f"Error getting tasks: {str(e)}")
            raise

    @staticmethod
    async def progress(goal_id: str) -> List[Progress]:
        try:
            progress_data = await postgresql.query("progress", {"goal_id": goal_id})
            return [Progress(**progress) for progress in progress_data]
        except Exception as e:
            logger.error(f"Error getting progress: {str(e)}")
            raise

    @staticmethod
    async def system_status() -> SystemStatus:
        try:
            status = await orchestrator.get_execution_status()
            return SystemStatus(**status)
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            raise

# Mutation type
class Mutation:
    @staticmethod
    async def create_goal(
        title: str,
        description: Optional[str] = None,
        status: str = "pending",
        due_date: Optional[datetime] = None,
        priority: str = "medium"
    ) -> Goal:
        try:
            goal_data = {
                "id": str(datetime.utcnow().timestamp()),
                "title": title,
                "description": description,
                "status": status,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "due_date": due_date,
                "priority": priority
            }
            result = await mongodb.insert("goals", goal_data)
            return Goal(**goal_data)
        except Exception as e:
            logger.error(f"Error creating goal: {str(e)}")
            raise

    @staticmethod
    async def create_task(
        title: str,
        goal_id: str,
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        due_date: Optional[datetime] = None,
        dependencies: Optional[List[str]] = None
    ) -> Task:
        try:
            task_data = {
                "id": str(datetime.utcnow().timestamp()),
                "title": title,
                "description": description,
                "status": "pending",
                "goal_id": goal_id,
                "assignee": assignee,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "due_date": due_date,
                "dependencies": dependencies
            }
            result = await postgresql.insert("tasks", task_data)
            return Task(**task_data)
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            raise

    @staticmethod
    async def create_progress(
        goal_id: str,
        status: str,
        progress: float,
        notes: Optional[str] = None
    ) -> Progress:
        try:
            progress_data = {
                "id": str(datetime.utcnow().timestamp()),
                "goal_id": goal_id,
                "status": status,
                "progress": progress,
                "timestamp": datetime.utcnow(),
                "notes": notes
            }
            result = await postgresql.insert("progress", progress_data)
            return Progress(**progress_data)
        except Exception as e:
            logger.error(f"Error creating progress: {str(e)}")
            raise

    @staticmethod
    async def execute_workflow(
        topic: str,
        reasoning_effort: str = "balanced"
    ) -> WorkflowResult:
        try:
            results = await orchestrator.execute_workflow(topic, reasoning_effort)
            return WorkflowResult(**results)
        except Exception as e:
            logger.error(f"Error executing workflow: {str(e)}")
            raise

# Create schema
schema = Schema(query=Query, mutation=Mutation)

# Create GraphQL router
graphql_app = GraphQLRouter(schema)

# Startup and shutdown events
@graphql_app.on_startup
async def startup():
    await orchestrator.initialize()
    await mongodb.connect()
    await postgresql.connect()

@graphql_app.on_shutdown
async def shutdown():
    await orchestrator.cleanup()
    await mongodb.close()
    await postgresql.close() 