"""
Configuration module for handling environment variables and settings.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for handling environment variables."""
    
    # Base paths
    BASE_DIR = Path(__file__).resolve().parent.parent
    CREDENTIALS_DIR = BASE_DIR / 'config' / 'credentials'
    
    # Google Sheets Configuration
    GOOGLE_SHEETS_CREDENTIALS_PATH = CREDENTIALS_DIR / 'credentials.json'
    GOOGLE_SHEETS_SPREADSHEET_ID = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
    GOOGLE_SHEETS_WEBSITE_RANGE = os.getenv('GOOGLE_SHEETS_WEBSITE_RANGE')
    GOOGLE_SHEETS_ANALYTICS_RANGE = os.getenv('GOOGLE_SHEETS_ANALYTICS_RANGE')
    GOOGLE_SHEETS_TWITTER_RANGE = os.getenv('GOOGLE_SHEETS_TWITTER_RANGE')
    
    # Twitter Configuration
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
    TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    # Notification Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
    SLACK_WEBHOOK_URL = os.getenv('SLACK_WEBHOOK_URL')
    EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
    EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', 587))
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    
    # Data Processing Configuration
    DATA_VALIDATION_THRESHOLD = float(os.getenv('DATA_VALIDATION_THRESHOLD', 0.95))
    ANOMALY_DETECTION_THRESHOLD = float(os.getenv('ANOMALY_DETECTION_THRESHOLD', 2.0))
    ALERT_THRESHOLD = int(os.getenv('ALERT_THRESHOLD', 1000))
    
    # Monitoring Configuration
    MONITORING_INTERVAL = int(os.getenv('MONITORING_INTERVAL', 300))
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate_config(cls) -> bool:
        """
        Validate that all required configuration values are present.
        
        Returns:
            bool: True if all required configurations are present, False otherwise
        """
        # Validate credentials file
        if not cls.GOOGLE_SHEETS_CREDENTIALS_PATH.exists():
            print(f"Credentials file not found at {cls.GOOGLE_SHEETS_CREDENTIALS_PATH}")
            return False
            
        # Validate credentials content
        try:
            with open(cls.GOOGLE_SHEETS_CREDENTIALS_PATH) as f:
                credentials = json.load(f)
                required_fields = [
                    'type', 'project_id', 'private_key_id', 'private_key',
                    'client_email', 'client_id', 'auth_uri', 'token_uri',
                    'auth_provider_x509_cert_url', 'client_x509_cert_url'
                ]
                missing_fields = [field for field in required_fields if field not in credentials]
                if missing_fields:
                    print(f"Missing required fields in credentials: {', '.join(missing_fields)}")
                    return False
        except json.JSONDecodeError:
            print("Invalid JSON in credentials file")
            return False
        except Exception as e:
            print(f"Error reading credentials file: {str(e)}")
            return False
        
        # Validate environment variables
        required_configs = [
            'GOOGLE_SHEETS_SPREADSHEET_ID',
            'GOOGLE_SHEETS_WEBSITE_RANGE',
            'GOOGLE_SHEETS_ANALYTICS_RANGE',
            'GOOGLE_SHEETS_TWITTER_RANGE',
            'TWITTER_API_KEY',
            'TWITTER_API_SECRET',
            'TWITTER_ACCESS_TOKEN',
            'TWITTER_ACCESS_TOKEN_SECRET',
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHAT_ID'
        ]
        
        missing_configs = []
        for config in required_configs:
            if not getattr(cls, config):
                missing_configs.append(config)
        
        if missing_configs:
            print(f"Missing required configurations: {', '.join(missing_configs)}")
            return False
        
        return True
    
    @classmethod
    def get_google_credentials(cls) -> Dict[str, Any]:
        """
        Get Google Sheets credentials from the credentials file.
        
        Returns:
            Dict[str, Any]: Google Sheets credentials
        """
        try:
            with open(cls.GOOGLE_SHEETS_CREDENTIALS_PATH) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading Google credentials: {str(e)}")
            return {} 