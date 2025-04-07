"""
Tests for the TwitterDataFetcherAgent.
"""

import pytest
import pandas as pd
import json
from unittest.mock import Mock, patch
from agents.data.twitter_data_fetcher import TwitterDataFetcherAgent

@pytest.fixture
def mock_credentials():
    """Mock Google Sheets API credentials."""
    return "path/to/credentials.json"

@pytest.fixture
def mock_spreadsheet_id():
    """Mock Google Sheets spreadsheet ID."""
    return "test_spreadsheet_id"

@pytest.fixture
def fetcher_agent(mock_credentials, mock_spreadsheet_id):
    """Create a TwitterDataFetcherAgent instance with mocked dependencies."""
    with patch('google.oauth2.service_account.Credentials.from_service_account_file'), \
         patch('googleapiclient.discovery.build'):
        agent = TwitterDataFetcherAgent(mock_credentials, mock_spreadsheet_id)
        return agent

def test_initialization(fetcher_agent, mock_credentials, mock_spreadsheet_id):
    """Test agent initialization."""
    assert fetcher_agent.credentials_path == mock_credentials
    assert fetcher_agent.spreadsheet_id == mock_spreadsheet_id
    assert hasattr(fetcher_agent, 'error_handler')
    assert hasattr(fetcher_agent, 'monitoring')

def test_fetch_twitter_data(fetcher_agent):
    """Test fetching and processing Twitter data."""
    # Sample Twitter data in JSON format
    tweet1 = {
        'engagement_count': 100,
        'reach': 1000,
        'likes': 50,
        'retweets': 30,
        'replies': 20
    }
    
    tweet2 = {
        'engagement_count': 200,
        'reach': 2000,
        'likes': 100,
        'retweets': 60,
        'replies': 40
    }
    
    mock_values = {
        'values': [
            ['Tweet ID', 'JSON Data'],
            ['123', json.dumps(tweet1)],
            ['456', json.dumps(tweet2)]
        ]
    }
    
    fetcher_agent.service.spreadsheets().values().get().execute.return_value = mock_values
    
    df = fetcher_agent.fetch_twitter_data('Twitter!A1:B3')
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert 'tweet_id' in df.columns
    assert 'engagement_count' in df.columns
    assert 'reach' in df.columns
    assert df['engagement_count'].sum() == 300
    assert df['reach'].sum() == 3000

def test_extract_metrics(fetcher_agent):
    """Test extracting metrics from Twitter data."""
    df = pd.DataFrame({
        'tweet_id': ['123', '456'],
        'engagement_count': [100, 200],
        'reach': [1000, 2000],
        'likes': [50, 100],
        'retweets': [30, 60],
        'replies': [20, 40]
    })
    
    metrics = fetcher_agent.extract_metrics(df)
    
    assert isinstance(metrics, dict)
    assert metrics['total_tweets'] == 2
    assert metrics['total_engagement'] == 300
    assert metrics['average_engagement'] == 150
    assert metrics['total_reach'] == 3000
    assert metrics['average_reach'] == 1500
    assert len(metrics['top_performing_tweets']) == 2

def test_validate_data(fetcher_agent):
    """Test data validation."""
    df = pd.DataFrame({
        'tweet_id': ['123', '456'],
        'engagement_count': [100, 200],
        'reach': [1000, 2000]
    })
    
    # Test with valid data
    assert fetcher_agent.validate_data(df, ['tweet_id', 'engagement_count', 'reach']) is True
    
    # Test with missing columns
    assert fetcher_agent.validate_data(df, ['tweet_id', 'engagement_count', 'reach', 'missing']) is False
    
    # Test with empty DataFrame
    assert fetcher_agent.validate_data(pd.DataFrame(), ['tweet_id']) is False

def test_error_handling(fetcher_agent):
    """Test error handling during data fetching."""
    # Test API error
    fetcher_agent.service.spreadsheets().values().get().execute.side_effect = Exception("API Error")
    df = fetcher_agent.fetch_twitter_data('Twitter!A1:B3')
    assert df.empty
    
    # Test JSON decode error
    mock_values = {
        'values': [
            ['Tweet ID', 'JSON Data'],
            ['123', 'invalid json']
        ]
    }
    fetcher_agent.service.spreadsheets().values().get().execute.return_value = mock_values
    df = fetcher_agent.fetch_twitter_data('Twitter!A1:B2')
    assert df.empty 