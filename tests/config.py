"""
Test configuration and mock data for the AgentOpenApi system.
"""

import os
from pathlib import Path

# Test directory paths
TEST_DIR = Path(__file__).parent
TEST_DATA_DIR = TEST_DIR / "test_data"
TEST_CONFIG_DIR = TEST_DIR / "test_config"

# Create test directories if they don't exist
TEST_DATA_DIR.mkdir(exist_ok=True)
TEST_CONFIG_DIR.mkdir(exist_ok=True)

# Mock data for testing
MOCK_WEBSITE_DATA = {
    'Date': ['2024-01-01', '2024-01-02'],
    'Visitors': [1000, 1200],
    'Pageviews': [2000, 2400],
    'BounceRate': [0.45, 0.42],
    'SessionDuration': [180, 190]
}

MOCK_TWITTER_DATA = {
    'created_at': ['2024-01-01', '2024-01-02'],
    'text': ['Sample tweet 1', 'Sample tweet 2'],
    'retweet_count': [100, 150],
    'favorite_count': [200, 250],
    'reply_count': [50, 60]
}

MOCK_ANALYTICS_DATA = {
    'Date': ['2024-01-01', '2024-01-02'],
    'Users': [950, 1150],
    'Sessions': [1800, 2200],
    'BounceRate': [0.45, 0.42],
    'PagesPerSession': [2.1, 2.2]
}

# Mock alert configurations
MOCK_ALERT_CONFIGS = {
    'website': {
        'visitors': {
            'max_threshold': 10000,
            'min_threshold': 1000
        },
        'bounce_rate': {
            'max_threshold': 0.7,
            'min_threshold': 0.1
        }
    },
    'twitter': {
        'engagement_rate': {
            'max_threshold': 0.1,
            'min_threshold': 0.01
        },
        'reach': {
            'max_threshold': 100000,
            'min_threshold': 1000
        }
    }
}

# Test environment variables
TEST_ENV_VARS = {
    'TELEGRAM_BOT_TOKEN': 'test_bot_token',
    'TELEGRAM_CHAT_ID': 'test_chat_id',
    'SLACK_WEBHOOK_URL': 'https://test.slack.com/webhook',
    'GOOGLE_SHEETS_CREDENTIALS': 'test_credentials.json'
}

# Test file paths
TEST_ALERT_CONFIGS_PATH = TEST_CONFIG_DIR / "alert_configs.json"
TEST_CREDENTIALS_PATH = TEST_CONFIG_DIR / "credentials.json"

# Create test files
def setup_test_files():
    """Create test files with mock data."""
    import json
    
    # Create alert configs file
    with open(TEST_ALERT_CONFIGS_PATH, 'w') as f:
        json.dump(MOCK_ALERT_CONFIGS, f, indent=2)
    
    # Create credentials file
    with open(TEST_CREDENTIALS_PATH, 'w') as f:
        json.dump({'test': 'credentials'}, f, indent=2)

# Set up test environment
def setup_test_environment():
    """Set up the test environment."""
    # Create test directories
    TEST_DATA_DIR.mkdir(exist_ok=True)
    TEST_CONFIG_DIR.mkdir(exist_ok=True)
    
    # Create test files
    setup_test_files()
    
    # Set environment variables
    for key, value in TEST_ENV_VARS.items():
        os.environ[key] = value

# Clean up test environment
def cleanup_test_environment():
    """Clean up the test environment."""
    # Remove test files
    if TEST_ALERT_CONFIGS_PATH.exists():
        TEST_ALERT_CONFIGS_PATH.unlink()
    if TEST_CREDENTIALS_PATH.exists():
        TEST_CREDENTIALS_PATH.unlink()
    
    # Remove test directories if empty
    if TEST_CONFIG_DIR.exists() and not any(TEST_CONFIG_DIR.iterdir()):
        TEST_CONFIG_DIR.rmdir()
    if TEST_DATA_DIR.exists() and not any(TEST_DATA_DIR.iterdir()):
        TEST_DATA_DIR.rmdir()
    
    # Unset environment variables
    for key in TEST_ENV_VARS:
        if key in os.environ:
            del os.environ[key] 