from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from loguru import logger
from datetime import datetime

class AgentStatus(Enum):
    INITIALIZING = "initializing"
    READY = "ready"
    BUSY = "busy"
    ERROR = "error"
    SHUTDOWN = "shutdown"

class AgentCapability(Enum):
    DATA_ANALYSIS = "data_analysis"
    REPORT_GENERATION = "report_generation"
    MONITORING = "monitoring"
    ALERTING = "alerting"
    TASK_MANAGEMENT = "task_management"

@dataclass
class AgentConfig:
    agent_id: str
    capabilities: List[AgentCapability]
    max_concurrent_tasks: int = 3
    timeout_seconds: int = 300

class DomainAgent:
    def __init__(self, config: AgentConfig):
        self.config = config
        self.status = AgentStatus.INITIALIZING
        self.current_tasks: List[str] = []
        self.metrics_client = None
        self.logger = logger
        self.data_hub = None

    async def initialize(self):
        """Initialize agent resources"""
        try:
            self.metrics_client = MetricsClient()
            self.status = AgentStatus.READY
            logger.info(f"Agent {self.config.agent_id} initialized successfully")
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"Error initializing agent {self.config.agent_id}: {str(e)}")
            raise

    async def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a task"""
        if self.status != AgentStatus.READY:
            raise RuntimeError(f"Agent {self.config.agent_id} is not ready")

        if len(self.current_tasks) >= self.config.max_concurrent_tasks:
            raise RuntimeError(f"Agent {self.config.agent_id} is at maximum capacity")

        try:
            self.status = AgentStatus.BUSY
            self.current_tasks.append(task["task_id"])
            
            # Execute the task
            result = await self._execute_task_impl(task)
            
            self.current_tasks.remove(task["task_id"])
            if not self.current_tasks:
                self.status = AgentStatus.READY
                
            return result
        except Exception as e:
            self.status = AgentStatus.ERROR
            logger.error(f"Error executing task {task['task_id']}: {str(e)}")
            raise

    async def _execute_task_impl(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Implementation of task execution - to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement _execute_task_impl")

    async def report_status(self) -> Dict[str, Any]:
        """Report current agent status"""
        return {
            "agent_id": self.config.agent_id,
            "status": self.status.value,
            "current_tasks": self.current_tasks,
            "capabilities": [cap.value for cap in self.config.capabilities],
            "timestamp": datetime.now().isoformat()
        }

    async def shutdown(self):
        """Clean shutdown of agent"""
        try:
            if self.metrics_client:
                await self.metrics_client.close()
            self.status = AgentStatus.SHUTDOWN
            logger.info(f"Agent {self.config.agent_id} shutdown completed")
        except Exception as e:
            logger.error(f"Error during agent shutdown: {str(e)}")
            raise

    def has_capability(self, capability: AgentCapability) -> bool:
        """Check if agent has a specific capability"""
        return capability in self.config.capabilities 