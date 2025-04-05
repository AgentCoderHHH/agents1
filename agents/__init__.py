"""
AgentOpenApi - A collection of AI agents for documentation and technical analysis
"""

from loguru import logger
import os
from pathlib import Path

# Configure Loguru logger
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"

# Ensure logs directory exists
Path("logs").mkdir(exist_ok=True)

logger.remove()  # Remove default handler
logger.add(
    "logs/agent_system.log",
    rotation="500 MB",
    retention="10 days",
    compression="zip",
    format=LOG_FORMAT,
    level=LOG_LEVEL,
    backtrace=True,
    diagnose=True
)
logger.add(
    "logs/errors.log",
    rotation="100 MB",
    retention="7 days",
    compression="zip",
    format=LOG_FORMAT,
    level="ERROR",
    backtrace=True,
    diagnose=True,
    filter=lambda record: record["level"].name == "ERROR"
)

# Add console output for non-production environments
if os.getenv("ENVIRONMENT", "development") != "production":
    logger.add(
        lambda msg: print(msg, end=""),
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        colorize=True
    )

# Import monitoring components
from .monitoring import monitor, API_CALLS, API_ERRORS, OPERATION_DURATION, ACTIVE_OPERATIONS
from .monitoring_ui import start_monitoring

__all__ = [
    'start_monitoring',
    'monitor',
    'API_CALLS',
    'API_ERRORS',
    'OPERATION_DURATION',
    'ACTIVE_OPERATIONS'
] 