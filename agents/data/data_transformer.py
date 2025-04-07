"""
Data Transformer Agent for cleaning and transforming data from various sources.
"""

from typing import Dict, List, Any, Union
import pandas as pd
import numpy as np
from datetime import datetime

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config

class DataTransformerAgent:
    """Agent responsible for transforming and cleaning data from various sources."""
    
    def __init__(self):
        """Initialize the Data Transformer Agent."""
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
    
    def clean_website_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and transform website data.
        
        Args:
            df (pd.DataFrame): Raw website data
            
        Returns:
            pd.DataFrame: Cleaned and transformed website data
        """
        try:
            # Convert date column to datetime
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
            
            # Convert numeric columns
            numeric_columns = ['Visitors', 'Pageviews', 'Bounce Rate', 'Avg. Session Duration']
            for col in numeric_columns:
                if col in df.columns:
                    if col == 'Bounce Rate':
                        df[col] = df[col].str.rstrip('%').astype('float') / 100.0
                    elif col == 'Avg. Session Duration':
                        df[col] = pd.to_timedelta(df[col]).dt.total_seconds()
                    else:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Sort by date
            if 'Date' in df.columns:
                df = df.sort_values('Date')
            
            # Log transformation
            self.monitoring.log_metric(
                "website_data_transformation_success",
                1,
                {"rows_processed": len(df)}
            )
            
            return df
            
        except Exception as e:
            self.error_handler.handle_error(
                "DataTransformationError",
                f"Failed to clean website data: {str(e)}"
            )
            return pd.DataFrame()
    
    def clean_twitter_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and transform Twitter data.
        
        Args:
            df (pd.DataFrame): Raw Twitter data
            
        Returns:
            pd.DataFrame: Cleaned and transformed Twitter data
        """
        try:
            # Convert date column to datetime
            if 'created_at' in df.columns:
                df['created_at'] = pd.to_datetime(df['created_at'])
            
            # Convert numeric columns
            numeric_columns = ['retweet_count', 'favorite_count', 'user_followers']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Calculate engagement metrics
            if all(col in df.columns for col in ['retweet_count', 'favorite_count']):
                df['total_engagement'] = df['retweet_count'] + df['favorite_count']
            
            # Remove duplicates
            df = df.drop_duplicates(subset=['tweet_id'])
            
            # Sort by date
            if 'created_at' in df.columns:
                df = df.sort_values('created_at')
            
            # Log transformation
            self.monitoring.log_metric(
                "twitter_data_transformation_success",
                1,
                {"tweets_processed": len(df)}
            )
            
            return df
            
        except Exception as e:
            self.error_handler.handle_error(
                "DataTransformationError",
                f"Failed to clean Twitter data: {str(e)}"
            )
            return pd.DataFrame()
    
    def clean_analytics_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and transform Google Analytics data.
        
        Args:
            df (pd.DataFrame): Raw analytics data
            
        Returns:
            pd.DataFrame: Cleaned and transformed analytics data
        """
        try:
            # Convert date column to datetime
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
            
            # Convert numeric columns
            numeric_columns = ['Sessions', 'Users', 'Pageviews', 'Bounce Rate']
            for col in numeric_columns:
                if col in df.columns:
                    if col == 'Bounce Rate':
                        df[col] = df[col].str.rstrip('%').astype('float') / 100.0
                    else:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Calculate derived metrics
            if all(col in df.columns for col in ['Sessions', 'Users']):
                df['Pages per Session'] = df['Pageviews'] / df['Sessions']
                df['Avg. Session Duration'] = df['Avg. Session Duration'].apply(
                    lambda x: pd.to_timedelta(x).total_seconds() if isinstance(x, str) else x
                )
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Sort by date
            if 'Date' in df.columns:
                df = df.sort_values('Date')
            
            # Log transformation
            self.monitoring.log_metric(
                "analytics_data_transformation_success",
                1,
                {"rows_processed": len(df)}
            )
            
            return df
            
        except Exception as e:
            self.error_handler.handle_error(
                "DataTransformationError",
                f"Failed to clean analytics data: {str(e)}"
            )
            return pd.DataFrame()
    
    def merge_datasets(self, datasets: Dict[str, pd.DataFrame], on: str = 'Date') -> pd.DataFrame:
        """
        Merge multiple datasets on a common column.
        
        Args:
            datasets (Dict[str, pd.DataFrame]): Dictionary of datasets to merge
            on (str): Column to merge on (default: 'Date')
            
        Returns:
            pd.DataFrame: Merged dataset
        """
        try:
            if not datasets:
                return pd.DataFrame()
            
            # Start with the first dataset
            merged_df = datasets[list(datasets.keys())[0]]
            
            # Merge remaining datasets
            for name, df in list(datasets.items())[1:]:
                if on in df.columns and on in merged_df.columns:
                    merged_df = pd.merge(merged_df, df, on=on, how='outer')
            
            # Log merge operation
            self.monitoring.log_metric(
                "dataset_merge_success",
                1,
                {"datasets_merged": len(datasets)}
            )
            
            return merged_df
            
        except Exception as e:
            self.error_handler.handle_error(
                "DataMergeError",
                f"Failed to merge datasets: {str(e)}"
            )
            return pd.DataFrame()
    
    def validate_transformed_data(self, df: pd.DataFrame, required_columns: List[str]) -> bool:
        """
        Validate the transformed data.
        
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
                f"Missing required columns in transformed data: {', '.join(missing_columns)}"
            )
            return False
            
        # Check for null values in required columns
        null_counts = df[required_columns].isnull().sum()
        if null_counts.any():
            self.error_handler.handle_error(
                "DataValidationError",
                f"Null values found in required columns: {null_counts[null_counts > 0].to_dict()}"
            )
            return False
            
        return True 