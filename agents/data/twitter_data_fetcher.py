"""
Twitter Data Fetcher Agent for retrieving and processing Twitter data from Google Sheets.
"""

import json
from typing import Dict, List, Optional, Any
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import tweepy

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config

class TwitterDataFetcherAgent:
    """Agent responsible for fetching and processing Twitter data from Google Sheets."""
    
    def __init__(self):
        """
        Initialize the Twitter Data Fetcher Agent.
        """
        if not Config.validate_config():
            raise ValueError("Missing required configurations")
            
        self.credentials_path = Config.GOOGLE_SHEETS_CREDENTIALS_PATH
        self.spreadsheet_id = Config.GOOGLE_SHEETS_SPREADSHEET_ID
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
        
        # Initialize Google Sheets API
        self._initialize_sheets_api()
        # Initialize Twitter API
        self._initialize_twitter_api()
    
    def _initialize_sheets_api(self) -> None:
        """Initialize the Google Sheets API client."""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            self.service = build('sheets', 'v4', credentials=credentials)
        except Exception as e:
            self.error_handler.handle_error(
                "GoogleSheetsAPIError",
                f"Failed to initialize Google Sheets API: {str(e)}"
            )
    
    def _initialize_twitter_api(self) -> None:
        """Initialize the Twitter API client."""
        try:
            auth = tweepy.OAuthHandler(
                Config.TWITTER_API_KEY,
                Config.TWITTER_API_SECRET
            )
            auth.set_access_token(
                Config.TWITTER_ACCESS_TOKEN,
                Config.TWITTER_ACCESS_TOKEN_SECRET
            )
            self.twitter_api = tweepy.API(auth)
        except Exception as e:
            self.error_handler.handle_error(
                "TwitterAPIError",
                f"Failed to initialize Twitter API: {str(e)}"
            )
    
    def fetch_twitter_data(self) -> pd.DataFrame:
        """
        Fetch Twitter data from Google Sheets and convert JSON strings to structured data.
        
        Returns:
            pd.DataFrame: DataFrame containing the processed Twitter data
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=Config.GOOGLE_SHEETS_TWITTER_RANGE
            ).execute()
            
            values = result.get('values', [])
            if not values:
                self.error_handler.handle_error(
                    "DataFetchError",
                    "No data found in the specified range"
                )
                return pd.DataFrame()
            
            # Process JSON data
            processed_data = []
            for row in values[1:]:  # Skip header row
                if len(row) >= 2:  # Ensure we have both ID and JSON data
                    try:
                        json_data = json.loads(row[1])
                        processed_data.append({
                            'tweet_id': row[0],
                            **json_data
                        })
                    except json.JSONDecodeError as e:
                        self.error_handler.handle_error(
                            "JSONDecodeError",
                            f"Failed to parse JSON data for tweet {row[0]}: {str(e)}"
                        )
            
            if not processed_data:
                return pd.DataFrame()
            
            # Convert to DataFrame
            df = pd.DataFrame(processed_data)
            
            # Log successful fetch
            self.monitoring.log_metric(
                "twitter_data_fetch_success",
                1,
                {"range": Config.GOOGLE_SHEETS_TWITTER_RANGE, "tweets_processed": len(processed_data)}
            )
            
            return df
            
        except HttpError as e:
            self.error_handler.handle_error(
                "GoogleSheetsAPIError",
                f"Failed to fetch Twitter data: {str(e)}"
            )
            return pd.DataFrame()
    
    def fetch_realtime_twitter_data(self, query: str, count: int = 100) -> pd.DataFrame:
        """
        Fetch real-time Twitter data using the Twitter API.
        
        Args:
            query (str): Search query for tweets
            count (int): Number of tweets to fetch (default: 100)
            
        Returns:
            pd.DataFrame: DataFrame containing the real-time Twitter data
        """
        try:
            tweets = self.twitter_api.search_tweets(
                q=query,
                count=count,
                tweet_mode='extended'
            )
            
            processed_data = []
            for tweet in tweets:
                processed_data.append({
                    'tweet_id': tweet.id_str,
                    'text': tweet.full_text,
                    'created_at': tweet.created_at,
                    'retweet_count': tweet.retweet_count,
                    'favorite_count': tweet.favorite_count,
                    'user': tweet.user.screen_name,
                    'user_followers': tweet.user.followers_count
                })
            
            df = pd.DataFrame(processed_data)
            
            # Log successful fetch
            self.monitoring.log_metric(
                "realtime_twitter_data_fetch_success",
                1,
                {"query": query, "tweets_fetched": len(processed_data)}
            )
            
            return df
            
        except Exception as e:
            self.error_handler.handle_error(
                "TwitterAPIError",
                f"Failed to fetch real-time Twitter data: {str(e)}"
            )
            return pd.DataFrame()
    
    def extract_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Extract key metrics from Twitter data.
        
        Args:
            df (pd.DataFrame): DataFrame containing Twitter data
            
        Returns:
            Dict[str, Any]: Dictionary containing key metrics
        """
        if df.empty:
            return {}
        
        try:
            metrics = {
                'total_tweets': len(df),
                'total_engagement': df.get('engagement_count', pd.Series()).sum(),
                'average_engagement': df.get('engagement_count', pd.Series()).mean(),
                'total_reach': df.get('reach', pd.Series()).sum(),
                'average_reach': df.get('reach', pd.Series()).mean(),
                'top_performing_tweets': df.nlargest(5, 'engagement_count').to_dict('records')
            }
            
            # Log metrics calculation
            self.monitoring.log_metric(
                "twitter_metrics_calculated",
                1,
                {"metrics_count": len(metrics)}
            )
            
            return metrics
            
        except Exception as e:
            self.error_handler.handle_error(
                "MetricsCalculationError",
                f"Failed to calculate Twitter metrics: {str(e)}"
            )
            return {}
    
    def validate_data(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        Validate the fetched Twitter data.
        
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