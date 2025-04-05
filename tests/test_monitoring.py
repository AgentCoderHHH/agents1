import pytest
import asyncio
import time
from prometheus_client import REGISTRY
from agents.monitoring import (
    monitor,
    MonitoringServer,
    API_CALLS,
    API_ERRORS,
    OPERATION_DURATION,
    ACTIVE_OPERATIONS
)

@pytest.fixture
def reset_metrics():
    """Reset Prometheus metrics between tests"""
    for metric in [API_CALLS, API_ERRORS, OPERATION_DURATION, ACTIVE_OPERATIONS]:
        if metric._name in REGISTRY._names_to_collectors:
            REGISTRY.unregister(metric)
    yield
    for metric in [API_CALLS, API_ERRORS, OPERATION_DURATION, ACTIVE_OPERATIONS]:
        if metric._name in REGISTRY._names_to_collectors:
            REGISTRY.unregister(metric)

def test_monitoring_server_singleton():
    """Test that MonitoringServer is a singleton"""
    server1 = MonitoringServer()
    server2 = MonitoringServer()
    assert server1 is server2

def test_monitoring_server_initialization():
    """Test monitoring server initialization"""
    server = MonitoringServer()
    assert server.port == 8000  # Default port
    assert hasattr(server, 'started')
    assert hasattr(server, 'initialized')

@pytest.mark.asyncio
async def test_monitor_successful_operation(reset_metrics):
    """Test monitoring of successful operation"""
    @monitor("test_agent", "test_operation")
    async def test_func():
        return "success"
    
    result = await test_func()
    
    assert result == "success"
    assert API_CALLS._metrics["test_agent"]["test_operation"]._value == 1
    assert ACTIVE_OPERATIONS._metrics["test_agent"]._value == 0
    assert len(OPERATION_DURATION._metrics["test_agent"]["test_operation"]._buckets) > 0

@pytest.mark.asyncio
async def test_monitor_failed_operation(reset_metrics):
    """Test monitoring of failed operation"""
    @monitor("test_agent", "test_operation")
    async def test_func():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        await test_func()
    
    assert API_CALLS._metrics["test_agent"]["test_operation"]._value == 1
    assert API_ERRORS._metrics["test_agent"]["test_operation"]["ValueError"]._value == 1
    assert ACTIVE_OPERATIONS._metrics["test_agent"]._value == 0

@pytest.mark.asyncio
async def test_monitor_concurrent_operations(reset_metrics):
    """Test monitoring of concurrent operations"""
    @monitor("test_agent", "test_operation")
    async def test_func():
        await asyncio.sleep(0.1)
        return "success"
    
    tasks = [test_func() for _ in range(3)]
    results = await asyncio.gather(*tasks)
    
    assert all(r == "success" for r in results)
    assert API_CALLS._metrics["test_agent"]["test_operation"]._value == 3
    assert ACTIVE_OPERATIONS._metrics["test_agent"]._value == 0

@pytest.mark.asyncio
async def test_monitor_timing_accuracy(reset_metrics):
    """Test accuracy of operation timing"""
    @monitor("test_agent", "test_operation")
    async def test_func():
        await asyncio.sleep(0.1)
        return "success"
    
    await test_func()
    
    histogram = OPERATION_DURATION._metrics["test_agent"]["test_operation"]
    assert any(0.1 <= bucket <= 0.5 for bucket in histogram._buckets)

@pytest.mark.asyncio
async def test_monitor_nested_operations(reset_metrics):
    """Test monitoring of nested operations"""
    @monitor("test_agent", "outer_operation")
    async def outer_func():
        return await inner_func()
    
    @monitor("test_agent", "inner_operation")
    async def inner_func():
        return "success"
    
    result = await outer_func()
    
    assert result == "success"
    assert API_CALLS._metrics["test_agent"]["outer_operation"]._value == 1
    assert API_CALLS._metrics["test_agent"]["inner_operation"]._value == 1
    assert ACTIVE_OPERATIONS._metrics["test_agent"]._value == 0

def test_monitoring_server_start(monkeypatch, caplog):
    """Test monitoring server start"""
    def mock_start_server(port):
        return True
    
    monkeypatch.setattr("prometheus_client.start_http_server", mock_start_server)
    server = MonitoringServer()
    server.start()
    
    assert "Prometheus metrics server started on port" in caplog.text
    assert server.started is True

def test_monitoring_server_start_failure(monkeypatch, caplog):
    """Test monitoring server start failure"""
    def mock_start_server(port):
        raise OSError("Port in use")
    
    monkeypatch.setattr("prometheus_client.start_http_server", mock_start_server)
    server = MonitoringServer()
    server.start()
    
    assert "Failed to start Prometheus server" in caplog.text 