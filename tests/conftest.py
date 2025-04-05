import pytest
import os
from unittest.mock import AsyncMock
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing"""
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setenv("GITHUB_TOKEN", "test-github-token")
    monkeypatch.setenv("GITHUB_REPO", "test/repo")

@pytest.fixture
def mock_openai():
    """Mock OpenAI client"""
    mock_client = AsyncMock(spec=OpenAI)
    mock_completion = AsyncMock()
    mock_completion.choices = [AsyncMock(message=AsyncMock(content="test response"))]
    mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)
    return mock_client

@pytest.fixture
def mock_github():
    """Mock GitHub client"""
    mock_client = AsyncMock()
    mock_repo = AsyncMock()
    mock_repo.create_file = AsyncMock()
    mock_repo.update_file = AsyncMock()
    mock_client.get_repo = AsyncMock(return_value=mock_repo)
    return mock_client

@pytest.fixture
def mock_browser():
    """Mock Playwright browser"""
    mock_browser = AsyncMock()
    mock_context = AsyncMock()
    mock_page = AsyncMock()
    
    mock_page.content = AsyncMock(return_value="<html>Test content</html>")
    mock_page.goto = AsyncMock()
    mock_page.close = AsyncMock()
    
    mock_context.new_page = AsyncMock(return_value=mock_page)
    mock_browser.new_context = AsyncMock(return_value=mock_context)
    
    return mock_browser

@pytest.fixture
def mock_nlp():
    """Mock spaCy NLP"""
    class MockToken:
        def __init__(self, text):
            self.text = text
            
    class MockDoc:
        def __init__(self, tokens):
            self._tokens = [MockToken(t) for t in tokens]
            
        def __iter__(self):
            return iter(self._tokens)
            
    class MockNLP:
        def __call__(self, text):
            return MockDoc(["test", "token"])
            
    return MockNLP()

@pytest.fixture
def base_test_config():
    """Base configuration for tests"""
    return {
        "test_topic": "Python Async Programming",
        "test_content": "This is test content for documentation",
        "test_prompt": "Generate documentation about {topic}",
        "test_documentation": "# Test Documentation\n\nThis is a test."
    }

@pytest.fixture
def async_test_timeout():
    """Default timeout for async tests"""
    return 5  # seconds

@pytest.fixture(autouse=True)
def mock_logger(monkeypatch):
    """Mock logger to prevent actual logging during tests"""
    mock_log = AsyncMock()
    for level in ["debug", "info", "warning", "error", "critical"]:
        setattr(mock_log, level, AsyncMock())
    monkeypatch.setattr("agents.error_handler.logger", mock_log)
    return mock_log 