"""
Google Analytics Fetcher Agent for retrieving website and Google Analytics data from Google Sheets.
"""

import os
from typing import Dict, List, Optional
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config

class GoogleAnalyticsFetcherAgent:
    """Agent responsible for fetching website and Google Analytics data from Google Sheets."""
    
    def __init__(self):
        """
        Initialize the Google Analytics Fetcher Agent.
        """
        if not Config.validate_config():
            raise ValueError("Missing required configurations")
            
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
        
        # Initialize Google Sheets API
        self._initialize_sheets_api()
    
    def _initialize_sheets_api(self) -> None:
        """Initialize the Google Sheets API client."""
        try:
            credentials = service_account.Credentials.from_service_account_info(
                Config.get_google_credentials(),
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            self.error_handler.handle_error(
                "GoogleSheetsAPIError",
                f"Failed to initialize Google Sheets API: {str(e)}"
            )
    
    def fetch_website_data(self) -> pd.DataFrame:
        """
        Fetch website data from Google Sheets.
        
        Returns:
            pd.DataFrame: DataFrame containing the website data
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=Config.GOOGLE_SHEETS_SPREADSHEET_ID,
                range=Config.GOOGLE_SHEETS_WEBSITE_RANGE
            ).execute()
            
            values = result.get('values', [])
            if not values:
                self.error_handler.handle_error(
                    "DataFetchError",
                    "No data found in the specified range"
                )
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(values[1:], columns=values[0])
            
            # Log successful fetch
            self.monitoring.log_metric(
                "website_data_fetch_success",
                1,
                {"range": Config.GOOGLE_SHEETS_WEBSITE_RANGE}
            )
            
            return df
            
        except HttpError as e:
            self.error_handler.handle_error(
                "GoogleSheetsAPIError",
                f"Failed to fetch website data: {str(e)}"
            )
            return pd.DataFrame()
    
    def fetch_analytics_data(self) -> pd.DataFrame:
        """
        Fetch Google Analytics data from Google Sheets.
        
        Returns:
            pd.DataFrame: DataFrame containing the Google Analytics data
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=Config.GOOGLE_SHEETS_SPREADSHEET_ID,
                range=Config.GOOGLE_SHEETS_ANALYTICS_RANGE
            ).execute()
            
            values = result.get('values', [])
            if not values:
                self.error_handler.handle_error(
                    "DataFetchError",
                    "No data found in the specified range"
                )
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(values[1:], columns=values[0])
            
            # Log successful fetch
            self.monitoring.log_metric(
                "analytics_data_fetch_success",
                1,
                {"range": Config.GOOGLE_SHEETS_ANALYTICS_RANGE}
            )
            
            return df
            
        except HttpError as e:
            self.error_handler.handle_error(
                "GoogleSheetsAPIError",
                f"Failed to fetch analytics data: {str(e)}"
            )
            return pd.DataFrame()
    
    def validate_data(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        Validate the fetched data.
        
        Args:
            df (pd.DataFrame): The DataFrame to validate
            required_columns (List[str]): List of required column names
            
        Returns:
            bool: True if data is valid, False otherwise
        """
        if df.empty:
            return False
            
        # Check for required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.error_handler.handle_error(
                "DataValidationError",
                f"Missing required columns: {', '.join(missing_columns)}"
            )
            return False
            
        return True 