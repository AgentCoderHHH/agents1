from prometheus_client import Counter, Histogram, Gauge, make_wsgi_app
from functools import wraps
import time
import threading
from typing import Callable, Any
from loguru import logger

# Use a consistent port for both Prometheus and Flask
METRICS_PORT = 8000

# Prometheus metrics
API_CALLS = Counter(
    'api_calls_total',
    'Total number of API calls',
    ['agent', 'operation']
)

API_ERRORS = Counter(
    'api_errors_total',
    'Total number of API errors',
    ['agent', 'operation', 'error_type']
)

OPERATION_DURATION = Histogram(
    'operation_duration_seconds',
    'Time spent in operations',
    ['agent', 'operation'],
    buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0, float('inf'))
)

ACTIVE_OPERATIONS = Gauge(
    'active_operations',
    'Number of currently active operations',
    ['agent']
)

def monitor(agent: str, operation: str) -> Callable:
    """Decorator to monitor agent operations"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            ACTIVE_OPERATIONS.labels(agent=agent).inc()
            API_CALLS.labels(agent=agent, operation=operation).inc()
            
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                OPERATION_DURATION.labels(
                    agent=agent,
                    operation=operation
                ).observe(duration)
                return result
            except Exception as e:
                API_ERRORS.labels(
                    agent=agent,
                    operation=operation,
                    error_type=type(e).__name__
                ).inc()
                logger.error(f"Operation {operation} in agent {agent} failed: {str(e)}")
                raise
            finally:
                ACTIVE_OPERATIONS.labels(agent=agent).dec()
                
        return wrapper
    return decorator

# Create a WSGI app that serves metrics
metrics_app = make_wsgi_app() 