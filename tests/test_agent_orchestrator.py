import pytest
from agents import AgentOrchestrator, OrchestratorConfig, ExecutionMode, ErrorHandling
from unittest.mock import Mock, patch, AsyncMock
from agents.error_handler import ErrorSeverity

@pytest.fixture
def config():
    return OrchestratorConfig(
        execution_mode=ExecutionMode.SEQUENTIAL,
        context_sharing=True,
        error_handling=ErrorHandling.STRICT,
        max_retries=3,
        timeout=300
    )

@pytest.fixture
def mock_internet_agent():
    agent = AsyncMock()
    agent.search_web = AsyncMock(return_value=["result1", "result2"])
    agent.initialize = AsyncMock()
    agent.cleanup = AsyncMock()
    return agent

@pytest.fixture
def mock_documentation_agent():
    agent = AsyncMock()
    agent.generate_documentation = AsyncMock(return_value="test documentation")
    agent.initialize = AsyncMock()
    agent.cleanup = AsyncMock()
    return agent

@pytest.fixture
def mock_prompt_agent():
    agent = AsyncMock()
    agent.optimize_prompt = AsyncMock(return_value="optimized prompt")
    agent.initialize = AsyncMock()
    agent.cleanup = AsyncMock()
    return agent

@pytest.fixture
def orchestrator(config, mock_internet_agent, mock_documentation_agent, mock_prompt_agent, monkeypatch):
    """Create an orchestrator with mocked agents"""
    orchestrator = AgentOrchestrator(config)
    orchestrator.agents = {
        "internet": mock_internet_agent,
        "documentation": mock_documentation_agent,
        "prompt": mock_prompt_agent
    }
    return orchestrator

@pytest.mark.asyncio
async def test_orchestrator_initialization(config):
    """Test orchestrator initialization"""
    orchestrator = AgentOrchestrator(config)
    assert orchestrator.config == config
    assert isinstance(orchestrator.agents, dict)
    assert orchestrator.error_handler is not None

@pytest.mark.asyncio
async def test_sequential_execution(orchestrator):
    """Test sequential workflow execution"""
    result = await orchestrator.execute_workflow("test topic")
    
    assert "research" in result
    assert "documentation" in result
    assert "optimized" in result
    assert orchestrator.agents["internet"].search_web.called
    assert orchestrator.agents["documentation"].generate_documentation.called
    assert orchestrator.agents["prompt"].optimize_prompt.called

@pytest.mark.asyncio
async def test_parallel_execution(config, orchestrator):
    """Test parallel workflow execution"""
    config.execution_mode = ExecutionMode.PARALLEL
    orchestrator.config = config
    
    result = await orchestrator.execute_workflow("test topic")
    
    assert "research" in result
    assert "documentation" in result
    assert "optimized" in result
    assert orchestrator.agents["internet"].search_web.called
    assert orchestrator.agents["documentation"].generate_documentation.called
    assert orchestrator.agents["prompt"].optimize_prompt.called

@pytest.mark.asyncio
async def test_error_handling_strict(orchestrator):
    """Test error handling in strict mode"""
    orchestrator.agents["internet"].search_web.side_effect = ValueError("Test error")
    
    with pytest.raises(ValueError):
        await orchestrator.execute_workflow("test topic")

@pytest.mark.asyncio
async def test_error_handling_lenient(config, orchestrator):
    """Test error handling in lenient mode"""
    config.error_handling = ErrorHandling.LENIENT
    orchestrator.config = config
    orchestrator.agents["internet"].search_web.side_effect = ValueError("Test error")
    
    result = await orchestrator.execute_workflow("test topic")
    assert "error" in result
    assert isinstance(result["error"].error_message, str)

@pytest.mark.asyncio
async def test_cleanup(orchestrator):
    """Test cleanup of all agents"""
    await orchestrator.cleanup()
    
    for agent in orchestrator.agents.values():
        assert agent.cleanup.called

@pytest.mark.asyncio
async def test_agent_initialization_error(config, mock_internet_agent):
    """Test handling of agent initialization errors"""
    mock_internet_agent.initialize.side_effect = ValueError("Init error")
    orchestrator = AgentOrchestrator(config)
    orchestrator.agents["internet"] = mock_internet_agent
    
    with pytest.raises(ValueError):
        await orchestrator.initialize_agents()

@pytest.mark.asyncio
async def test_context_sharing(config, orchestrator):
    """Test context sharing between agents"""
    config.context_sharing = True
    orchestrator.config = config
    
    await orchestrator.execute_workflow("test topic")
    
    # Verify that documentation agent received research results
    orchestrator.agents["documentation"].generate_documentation.assert_called_with(
        "test topic",
        ["result1", "result2"]
    ) 