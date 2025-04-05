import pytest
from agents import DocumentationMakerAgent, DocumentationConfig, TechnicalLevel
from unittest.mock import Mock, patch

@pytest.fixture
def doc_config():
    return DocumentationConfig(
        target_audience="developers",
        technical_level=TechnicalLevel.INTERMEDIATE,
        format="markdown"
    )

@pytest.fixture
def agent(doc_config):
    return DocumentationMakerAgent(doc_config)

@pytest.mark.asyncio
async def test_generate_documentation(agent):
    with patch.object(agent, 'openai') as mock_openai:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "# Test Documentation\n\nContent"
        mock_openai.chat.completions.create.return_value = mock_response
        
        result = await agent.generate_documentation("test topic", "test content")
        assert result.startswith("# Test Documentation")
        mock_openai.chat.completions.create.assert_called_once()

def test_organize_content(agent):
    content = """
    # Overview
    Test overview
    
    # Usage
    Test usage
    """
    sections = agent.organize_content(content)
    assert "Overview" in sections
    assert "Usage" in sections
    assert "Test overview" in sections["Overview"]
    assert "Test usage" in sections["Usage"]

def test_validate_documentation(agent):
    valid_doc = """
    # Overview
    Test
    
    # Prerequisites
    Test
    
    # Usage
    Test
    
    ```python
    print("test")
    ```
    """
    assert agent.validate_documentation(valid_doc) is True
    
    invalid_doc = "# Test"
    assert agent.validate_documentation(invalid_doc) is False

def test_format_documentation(agent):
    content = "# Test"
    assert agent.format_documentation(content) == content 