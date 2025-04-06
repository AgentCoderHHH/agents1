"""
AgentOpenApi - A system for automated documentation and research
"""

from loguru import logger
import os
from pathlib import Path

# Configure logger
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logger.add(
    log_dir / "agent_system.log",
    rotation="500 MB",
    retention="10 days",
    compression="zip",
    level="INFO"
)

logger.add(
    log_dir / "errors.log",
    rotation="100 MB",
    retention="7 days",
    compression="zip",
    level="ERROR"
)

# Import and expose agent classes
from .internet_documentation_agent import InternetDocumentationAgent
from .documentation_maker_agent import DocumentationMakerAgent
from .prompt_engineering_agent import PromptEngineeringAgent
from .agent_orchestrator import AgentOrchestrator

# Import monitoring components
from .monitoring import (
    monitor,
    API_CALLS,
    API_ERRORS,
    OPERATION_DURATION,
    ACTIVE_OPERATIONS
)

from .monitoring_ui import start_monitoring

__all__ = [
    'InternetDocumentationAgent',
    'DocumentationMakerAgent',
    'PromptEngineeringAgent',
    'AgentOrchestrator',
    'monitor',
    'API_CALLS',
    'API_ERRORS',
    'OPERATION_DURATION',
    'ACTIVE_OPERATIONS',
    'start_monitoring'
] 