"""
Test script to verify Google Sheets setup.
"""

import unittest
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

class TestGoogleSheets(unittest.TestCase):
    """Test cases for Google Sheets setup."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment."""
        load_dotenv()
        
        # Get credentials path from environment
        credentials_path = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
        spreadsheet_id = os.getenv('GOOGLE_SHEETS_SPREADSHEET_ID')
        
        # Verify credentials file exists
        cls.assertTrue(os.path.exists(credentials_path), 
                      f"Credentials file not found at {credentials_path}")
        
        # Create credentials
        cls.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        # Build service
        cls.service = build('sheets', 'v4', credentials=cls.credentials)
        cls.spreadsheet_id = spreadsheet_id
    
    def test_sheet_access(self):
        """Test access to the spreadsheet."""
        try:
            # Try to get spreadsheet metadata
            spreadsheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            self.assertIsNotNone(spreadsheet)
            self.assertIn('sheets', spreadsheet)
            
        except Exception as e:
            self.fail(f"Failed to access spreadsheet: {str(e)}")
    
    def test_sheet_ranges(self):
        """Test access to specific ranges."""
        ranges = [
            os.getenv('GOOGLE_SHEETS_WEBSITE_RANGE'),
            os.getenv('GOOGLE_SHEETS_ANALYTICS_RANGE'),
            os.getenv('GOOGLE_SHEETS_TWITTER_RANGE')
        ]
        
        for range_name in ranges:
            try:
                result = self.service.spreadsheets().values().get(
                    spreadsheetId=self.spreadsheet_id,
                    range=range_name
                ).execute()
                
                self.assertIsNotNone(result)
                self.assertIn('values', result)
                
            except Exception as e:
                self.fail(f"Failed to access range {range_name}: {str(e)}")

if __name__ == '__main__':
    unittest.main() 