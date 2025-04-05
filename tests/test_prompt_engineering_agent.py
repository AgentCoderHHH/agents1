import pytest
from agents import PromptEngineeringAgent, PromptConfig, OptimizationLevel
from unittest.mock import Mock, patch
import json
from pathlib import Path

@pytest.fixture
def prompt_config():
    return PromptConfig(
        optimization_level=OptimizationLevel.BALANCED,
        template_version="1.0",
        parameters={"test": "value"}
    )

@pytest.fixture
def agent(prompt_config):
    return PromptEngineeringAgent(prompt_config)

@pytest.mark.asyncio
async def test_optimize_prompt_minimal(agent):
    prompt = "  test  prompt  "
    result = agent._minimal_optimization(prompt)
    assert result == "test prompt"

@pytest.mark.asyncio
async def test_optimize_prompt_balanced(agent):
    with patch.object(agent, 'openai') as mock_openai:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Optimized prompt"
        mock_openai.chat.completions.create.return_value = mock_response
        
        result = await agent._balanced_optimization("test prompt")
        assert result == "Optimized prompt"
        mock_openai.chat.completions.create.assert_called_once()

@pytest.mark.asyncio
async def test_optimize_prompt_aggressive(agent):
    with patch.object(agent, 'openai') as mock_openai:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Highly optimized prompt"
        mock_openai.chat.completions.create.return_value = mock_response
        
        result = await agent._aggressive_optimization("test prompt")
        assert result == "Highly optimized prompt"
        mock_openai.chat.completions.create.assert_called_once()

def test_save_template(agent, tmp_path):
    agent.templates_dir = tmp_path
    template = "Test template"
    agent.save_template("test", template)
    
    template_path = tmp_path / "test_1.0.json"
    assert template_path.exists()
    
    with open(template_path) as f:
        data = json.load(f)
        assert data["name"] == "test"
        assert data["version"] == "1.0"
        assert data["template"] == template

def test_load_template(agent, tmp_path):
    agent.templates_dir = tmp_path
    template_data = {
        "name": "test",
        "version": "1.0",
        "template": "Test template",
        "parameters": {"test": "value"}
    }
    
    template_path = tmp_path / "test_1.0.json"
    with open(template_path, 'w') as f:
        json.dump(template_data, f)
        
    result = agent.load_template("test")
    assert result == template_data

def test_insert_parameters(agent):
    template = "Test {test} template"
    result = agent.insert_parameters(template)
    assert result == "Test value template"

@pytest.mark.asyncio
async def test_track_performance(agent):
    with patch.object(agent, 'openai') as mock_openai:
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = """
        clarity: 0.8
        completeness: 0.9
        relevance: 0.7
        technical_accuracy: 0.85
        """
        mock_openai.chat.completions.create.return_value = mock_response
        
        metrics = await agent.track_performance("test prompt", "test response")
        assert "clarity" in metrics
        assert "completeness" in metrics
        assert "relevance" in metrics
        assert "technical_accuracy" in metrics
        assert all(0 <= v <= 1 for v in metrics.values()) 