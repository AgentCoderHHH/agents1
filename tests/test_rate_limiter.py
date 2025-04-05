import pytest
import asyncio
import time
from agents.utils import rate_limit, RateLimiter

@pytest.fixture
def rate_limiter():
    return RateLimiter(calls_per_minute=60)

async def test_rate_limiter_initialization(rate_limiter):
    """Test that RateLimiter initializes correctly"""
    assert rate_limiter.calls_per_minute == 60
    assert rate_limiter.interval == 1.0  # 60 seconds / 60 calls
    assert rate_limiter.last_call_time == 0
    assert isinstance(rate_limiter.lock, asyncio.Lock)

@pytest.mark.asyncio
async def test_rate_limiter_single_call(rate_limiter):
    """Test single call with rate limiter"""
    async def test_func():
        return "test_result"
    
    result = await rate_limiter(test_func)
    assert result == "test_result"
    assert rate_limiter.last_call_time > 0

@pytest.mark.asyncio
async def test_rate_limiter_multiple_calls(rate_limiter):
    """Test multiple calls with rate limiter"""
    async def test_func():
        return "test_result"
    
    start_time = time.time()
    results = []
    
    for _ in range(3):
        result = await rate_limiter(test_func)
        results.append(result)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    assert all(r == "test_result" for r in results)
    assert elapsed_time >= 2.0  # Should take at least 2 seconds for 3 calls

@pytest.mark.asyncio
async def test_rate_limiter_concurrent_calls(rate_limiter):
    """Test concurrent calls with rate limiter"""
    async def test_func():
        return "test_result"
    
    start_time = time.time()
    tasks = [rate_limiter(test_func) for _ in range(3)]
    results = await asyncio.gather(*tasks)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    assert all(r == "test_result" for r in results)
    assert elapsed_time >= 2.0  # Should take at least 2 seconds for 3 calls

@pytest.mark.asyncio
async def test_rate_limit_decorator():
    """Test the rate_limit decorator"""
    @rate_limit(calls_per_minute=60)
    async def test_func():
        return "test_result"
    
    result = await test_func()
    assert result == "test_result"

@pytest.mark.asyncio
async def test_rate_limiter_with_exception(rate_limiter):
    """Test rate limiter with function that raises exception"""
    async def test_func():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        await rate_limiter(test_func)

@pytest.mark.asyncio
async def test_rate_limiter_with_different_rates():
    """Test rate limiter with different rates per minute"""
    rates = [30, 60, 120]
    
    for rate in rates:
        limiter = RateLimiter(calls_per_minute=rate)
        assert limiter.interval == 60 / rate
        
        start_time = time.time()
        for _ in range(3):
            await limiter(lambda: "test")
        elapsed_time = time.time() - start_time
        
        # Should take at least (2 * interval) seconds for 3 calls
        assert elapsed_time >= (2 * (60 / rate)) 