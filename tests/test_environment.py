"""
Test script to verify environment setup.
"""

import unittest
import sys
import os
from pathlib import Path

class TestEnvironment(unittest.TestCase):
    """Test cases for environment setup."""
    
    def test_python_version(self):
        """Test Python version."""
        self.assertTrue(sys.version_info >= (3, 8), "Python 3.8 or higher is required")
    
    def test_required_packages(self):
        """Test required packages are installed."""
        try:
            import pandas
            import numpy
            import google.auth
            import google.oauth2
            import googleapiclient
            import tweepy
            import telegram
        except ImportError as e:
            self.fail(f"Missing required package: {str(e)}")
    
    def test_directory_structure(self):
        """Test directory structure."""
        required_dirs = [
            'config',
            'logs',
            'tests'
        ]
        
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            self.assertTrue(dir_path.exists(), f"Directory {dir_name} does not exist")
            self.assertTrue(dir_path.is_dir(), f"{dir_name} is not a directory")
    
    def test_env_file(self):
        """Test .env file exists."""
        env_file = Path('.env')
        self.assertTrue(env_file.exists(), ".env file does not exist")
        self.assertTrue(env_file.is_file(), ".env is not a file")
        
        # Check for required environment variables
        required_vars = [
            'GOOGLE_SHEETS_CREDENTIALS_PATH',
            'GOOGLE_SHEETS_SPREADSHEET_ID',
            'TWITTER_API_KEY',
            'TWITTER_API_SECRET',
            'TWITTER_ACCESS_TOKEN',
            'TWITTER_ACCESS_TOKEN_SECRET',
            'TELEGRAM_BOT_TOKEN',
            'TELEGRAM_CHAT_ID'
        ]
        
        with open('.env') as f:
            env_content = f.read()
            
        for var in required_vars:
            self.assertIn(var, env_content, f"Missing environment variable: {var}")

if __name__ == '__main__':
    unittest.main() 