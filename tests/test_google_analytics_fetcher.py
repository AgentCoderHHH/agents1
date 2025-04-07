"""
Tests for the GoogleAnalyticsFetcherAgent.
"""

import pytest
import pandas as pd
from unittest.mock import Mock, patch
from agents.data.google_analytics_fetcher import GoogleAnalyticsFetcherAgent

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
    """Create a GoogleAnalyticsFetcherAgent instance with mocked dependencies."""
    with patch('google.oauth2.service_account.Credentials.from_service_account_file'), \
         patch('googleapiclient.discovery.build'):
        agent = GoogleAnalyticsFetcherAgent(mock_credentials, mock_spreadsheet_id)
        return agent

def test_initialization(fetcher_agent, mock_credentials, mock_spreadsheet_id):
    """Test agent initialization."""
    assert fetcher_agent.credentials_path == mock_credentials
    assert fetcher_agent.spreadsheet_id == mock_spreadsheet_id
    assert hasattr(fetcher_agent, 'error_handler')
    assert hasattr(fetcher_agent, 'monitoring')

def test_fetch_website_data(fetcher_agent):
    """Test fetching website data."""
    mock_values = {
        'values': [
            ['Date', 'Visitors', 'Pageviews'],
            ['2023-01-01', '100', '200'],
            ['2023-01-02', '150', '300']
        ]
    }
    
    fetcher_agent.service.spreadsheets().values().get().execute.return_value = mock_values
    
    df = fetcher_agent.fetch_website_data('Sheet1!A1:C3')
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['Date', 'Visitors', 'Pageviews']

def test_fetch_analytics_data(fetcher_agent):
    """Test fetching Google Analytics data."""
    mock_values = {
        'values': [
            ['Date', 'Sessions', 'Bounce Rate'],
            ['2023-01-01', '100', '50%'],
            ['2023-01-02', '150', '45%']
        ]
    }
    
    fetcher_agent.service.spreadsheets().values().get().execute.return_value = mock_values
    
    df = fetcher_agent.fetch_analytics_data('Analytics!A1:C3')
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ['Date', 'Sessions', 'Bounce Rate']

def test_validate_data(fetcher_agent):
    """Test data validation."""
    df = pd.DataFrame({
        'Date': ['2023-01-01', '2023-01-02'],
        'Visitors': [100, 150],
        'Pageviews': [200, 300]
    })
    
    # Test with valid data
    assert fetcher_agent.validate_data(df, ['Date', 'Visitors', 'Pageviews']) is True
    
    # Test with missing columns
    assert fetcher_agent.validate_data(df, ['Date', 'Visitors', 'Pageviews', 'Missing']) is False
    
    # Test with empty DataFrame
    assert fetcher_agent.validate_data(pd.DataFrame(), ['Date']) is False

def test_error_handling(fetcher_agent):
    """Test error handling during data fetching."""
    fetcher_agent.service.spreadsheets().values().get().execute.side_effect = Exception("API Error")
    
    df = fetcher_agent.fetch_website_data('Sheet1!A1:C3')
    assert df.empty 