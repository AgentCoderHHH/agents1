from enum import Enum
from typing import Optional, Dict, Any
from loguru import logger
import traceback
from dataclasses import dataclass
from datetime import datetime

class ErrorSeverity(Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

@dataclass
class ErrorContext:
    timestamp: datetime
    agent_name: str
    operation: str
    severity: ErrorSeverity
    error_type: str
    error_message: str
    stack_trace: Optional[str] = None
    additional_data: Optional[Dict[str, Any]] = None

class ErrorHandler:
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.error_log: Dict[str, ErrorContext] = {}
        
    def handle_error(
        self,
        error: Exception,
        operation: str,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        additional_data: Optional[Dict[str, Any]] = None
    ) -> ErrorContext:
        """Handle and log an error with context"""
        error_id = f"{self.agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        error_context = ErrorContext(
            timestamp=datetime.now(),
            agent_name=self.agent_name,
            operation=operation,
            severity=severity,
            error_type=type(error).__name__,
            error_message=str(error),
            stack_trace=traceback.format_exc(),
            additional_data=additional_data
        )
        
        self.error_log[error_id] = error_context
        self._log_error(error_context)
        
        return error_context
    
    def _log_error(self, error_context: ErrorContext):
        """Log error based on severity"""
        log_message = (
            f"Error in {error_context.agent_name} during {error_context.operation}\n"
            f"Type: {error_context.error_type}\n"
            f"Message: {error_context.error_message}\n"
            f"Additional Data: {error_context.additional_data}"
        )
        
        if error_context.severity == ErrorSeverity.DEBUG:
            logger.debug(log_message)
        elif error_context.severity == ErrorSeverity.INFO:
            logger.info(log_message)
        elif error_context.severity == ErrorSeverity.WARNING:
            logger.warning(log_message)
        elif error_context.severity == ErrorSeverity.ERROR:
            logger.error(log_message)
        else:
            logger.critical(log_message)
            
        if error_context.stack_trace:
            logger.debug(f"Stack trace:\n{error_context.stack_trace}")
    
    def get_error_history(self) -> Dict[str, ErrorContext]:
        """Get the complete error history for this agent"""
        return self.error_log
    
    def clear_error_history(self):
        """Clear the error history"""
        self.error_log.clear() 