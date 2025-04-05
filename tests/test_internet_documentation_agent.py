import pytest
from agents import InternetDocumentationAgent, WebResearchConfig
from unittest.mock import Mock, patch

@pytest.fixture
def web_config():
    return WebResearchConfig(
        search_engines=["test.com"],
        content_filters=["test"],
        credibility_threshold=0.7
    )

@pytest.fixture
def agent(web_config):
    return InternetDocumentationAgent(web_config)

@pytest.mark.asyncio
async def test_initialize(agent):
    with patch('playwright.async_api.async_playwright') as mock_playwright:
        mock_browser = Mock()
        mock_context = Mock()
        mock_playwright.return_value.start.return_value.chromium.launch.return_value = mock_browser
        mock_browser.new_context.return_value = mock_context
        
        await agent.initialize()
        
        assert hasattr(agent, 'playwright')
        assert hasattr(agent, 'browser')
        assert hasattr(agent, 'context')

@pytest.mark.asyncio
async def test_search_web(agent):
    with patch.object(agent, 'context') as mock_context:
        mock_page = Mock()
        mock_context.new_page.return_value = mock_page
        mock_page.content.return_value = '<a href="https://test.com">Test</a>'
        
        links = await agent.search_web("test query")
        assert len(links) > 0
        assert "test.com" in links[0]

@pytest.mark.asyncio
async def test_extract_content(agent):
    with patch.object(agent, 'context') as mock_context:
        mock_page = Mock()
        mock_context.new_page.return_value = mock_page
        mock_page.content.return_value = '<html><body>Test content</body></html>'
        
        content = await agent.extract_content("https://test.com")
        assert content is not None
        assert "Test content" in content

def test_assess_credibility(agent):
    content = "This is a research study with data and statistics"
    score = agent.assess_credibility(content)
    assert 0 <= score <= 1
    assert score > 0.5  # Should be high due to research-related terms

@pytest.mark.asyncio
async def test_store_documentation(agent):
    with patch.object(agent, 'github') as mock_github:
        mock_repo = Mock()
        mock_github.get_repo.return_value = mock_repo
        
        await agent.store_documentation("Test content", "test.md")
        mock_repo.create_file.assert_called_once() 