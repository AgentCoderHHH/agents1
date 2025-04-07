"""
Metrics Calculator Agent for calculating various metrics from transformed data.
"""

from typing import Dict, List, Any, Union
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config

class MetricsCalculatorAgent:
    """Agent responsible for calculating metrics from transformed data."""
    
    def __init__(self):
        """Initialize the Metrics Calculator Agent."""
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
    
    def calculate_website_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate website metrics from transformed data.
        
        Args:
            df (pd.DataFrame): Transformed website data
            
        Returns:
            Dict[str, Any]: Dictionary containing calculated metrics
        """
        try:
            if df.empty:
                return {}
            
            metrics = {
                'total_visitors': df['Visitors'].sum(),
                'total_pageviews': df['Pageviews'].sum(),
                'avg_bounce_rate': df['Bounce Rate'].mean(),
                'avg_session_duration': df['Avg. Session Duration'].mean(),
                'visitors_trend': self._calculate_trend(df, 'Visitors'),
                'pageviews_trend': self._calculate_trend(df, 'Pageviews'),
                'top_performing_days': self._get_top_performing_days(df, 'Visitors', 5)
            }
            
            # Log metrics calculation
            self.monitoring.log_metric(
                "website_metrics_calculated",
                1,
                {"metrics_count": len(metrics)}
            )
            
            return metrics
            
        except Exception as e:
            self.error_handler.handle_error(
                "MetricsCalculationError",
                f"Failed to calculate website metrics: {str(e)}"
            )
            return {}
    
    def calculate_twitter_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate Twitter metrics from transformed data.
        
        Args:
            df (pd.DataFrame): Transformed Twitter data
            
        Returns:
            Dict[str, Any]: Dictionary containing calculated metrics
        """
        try:
            if df.empty:
                return {}
            
            metrics = {
                'total_tweets': len(df),
                'total_engagement': df['total_engagement'].sum(),
                'avg_engagement': df['total_engagement'].mean(),
                'total_reach': df['user_followers'].sum(),
                'engagement_rate': df['total_engagement'].sum() / df['user_followers'].sum() if df['user_followers'].sum() > 0 else 0,
                'engagement_trend': self._calculate_trend(df, 'total_engagement'),
                'top_performing_tweets': self._get_top_performing_tweets(df, 'total_engagement', 5)
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
    
    def calculate_analytics_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate Google Analytics metrics from transformed data.
        
        Args:
            df (pd.DataFrame): Transformed analytics data
            
        Returns:
            Dict[str, Any]: Dictionary containing calculated metrics
        """
        try:
            if df.empty:
                return {}
            
            metrics = {
                'total_sessions': df['Sessions'].sum(),
                'total_users': df['Users'].sum(),
                'total_pageviews': df['Pageviews'].sum(),
                'avg_bounce_rate': df['Bounce Rate'].mean(),
                'avg_pages_per_session': df['Pages per Session'].mean(),
                'avg_session_duration': df['Avg. Session Duration'].mean(),
                'sessions_trend': self._calculate_trend(df, 'Sessions'),
                'users_trend': self._calculate_trend(df, 'Users'),
                'top_performing_days': self._get_top_performing_days(df, 'Sessions', 5)
            }
            
            # Log metrics calculation
            self.monitoring.log_metric(
                "analytics_metrics_calculated",
                1,
                {"metrics_count": len(metrics)}
            )
            
            return metrics
            
        except Exception as e:
            self.error_handler.handle_error(
                "MetricsCalculationError",
                f"Failed to calculate analytics metrics: {str(e)}"
            )
            return {}
    
    def _calculate_trend(self, df: pd.DataFrame, column: str, window: int = 7) -> float:
        """
        Calculate the trend of a metric over time.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            column (str): Column name to calculate trend for
            window (int): Window size for trend calculation (default: 7)
            
        Returns:
            float: Trend value (positive for increasing, negative for decreasing)
        """
        try:
            if len(df) < window:
                return 0.0
            
            # Calculate moving average
            ma = df[column].rolling(window=window).mean()
            
            # Calculate trend
            if len(ma) >= 2:
                return (ma.iloc[-1] - ma.iloc[0]) / ma.iloc[0]
            return 0.0
            
        except Exception:
            return 0.0
    
    def _get_top_performing_days(self, df: pd.DataFrame, metric: str, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the top performing days based on a metric.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            metric (str): Metric to sort by
            n (int): Number of top days to return (default: 5)
            
        Returns:
            List[Dict[str, Any]]: List of top performing days
        """
        try:
            if df.empty or metric not in df.columns:
                return []
            
            top_days = df.nlargest(n, metric)
            return top_days[['Date', metric]].to_dict('records')
            
        except Exception:
            return []
    
    def _get_top_performing_tweets(self, df: pd.DataFrame, metric: str, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get the top performing tweets based on a metric.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            metric (str): Metric to sort by
            n (int): Number of top tweets to return (default: 5)
            
        Returns:
            List[Dict[str, Any]]: List of top performing tweets
        """
        try:
            if df.empty or metric not in df.columns:
                return []
            
            top_tweets = df.nlargest(n, metric)
            return top_tweets[['tweet_id', 'text', metric]].to_dict('records')
            
        except Exception:
            return [] 