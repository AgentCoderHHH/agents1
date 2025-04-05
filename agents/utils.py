import time
import asyncio
from functools import wraps
from typing import Callable, Any
from loguru import logger

class RateLimiter:
    def __init__(self, calls_per_minute: int):
        self.calls_per_minute = calls_per_minute
        self.interval = 60 / calls_per_minute
        self.last_call_time = 0
        self.lock = asyncio.Lock()

    async def __call__(self, func: Callable) -> Any:
        async with self.lock:
            current_time = time.time()
            time_since_last_call = current_time - self.last_call_time
            
            if time_since_last_call < self.interval:
                sleep_time = self.interval - time_since_last_call
                logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
                await asyncio.sleep(sleep_time)
            
            self.last_call_time = time.time()
            return await func

def rate_limit(calls_per_minute: int):
    """Decorator to rate limit async functions"""
    limiter = RateLimiter(calls_per_minute)
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await limiter(lambda: func(*args, **kwargs))
        return wrapper
    
    return decorator 