"""
Trend Analysis Agent for analyzing trends and patterns in data.
"""

from typing import Dict, List, Any, Union, Tuple
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from scipy import stats

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config

class TrendAnalysisAgent:
    """Agent responsible for analyzing trends and patterns in data."""
    
    def __init__(self):
        """Initialize the Trend Analysis Agent."""
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
    
    def analyze_website_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trends in website data.
        
        Args:
            df (pd.DataFrame): Transformed website data
            
        Returns:
            Dict[str, Any]: Dictionary containing trend analysis results
        """
        try:
            if df.empty:
                return {}
            
            analysis = {
                'visitor_growth': self._analyze_growth(df, 'Visitors'),
                'pageview_growth': self._analyze_growth(df, 'Pageviews'),
                'bounce_rate_trend': self._analyze_trend(df, 'Bounce Rate'),
                'session_duration_trend': self._analyze_trend(df, 'Avg. Session Duration'),
                'seasonal_patterns': self._analyze_seasonality(df, 'Visitors'),
                'correlation_analysis': self._analyze_correlations(df, ['Visitors', 'Pageviews', 'Bounce Rate'])
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "website_trend_analysis_completed",
                1,
                {"analysis_count": len(analysis)}
            )
            
            return analysis
            
        except Exception as e:
            self.error_handler.handle_error(
                "TrendAnalysisError",
                f"Failed to analyze website trends: {str(e)}"
            )
            return {}
    
    def analyze_twitter_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trends in Twitter data.
        
        Args:
            df (pd.DataFrame): Transformed Twitter data
            
        Returns:
            Dict[str, Any]: Dictionary containing trend analysis results
        """
        try:
            if df.empty:
                return {}
            
            analysis = {
                'engagement_growth': self._analyze_growth(df, 'total_engagement'),
                'reach_growth': self._analyze_growth(df, 'user_followers'),
                'engagement_trend': self._analyze_trend(df, 'total_engagement'),
                'seasonal_patterns': self._analyze_seasonality(df, 'total_engagement'),
                'correlation_analysis': self._analyze_correlations(df, ['total_engagement', 'user_followers', 'retweet_count', 'favorite_count'])
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "twitter_trend_analysis_completed",
                1,
                {"analysis_count": len(analysis)}
            )
            
            return analysis
            
        except Exception as e:
            self.error_handler.handle_error(
                "TrendAnalysisError",
                f"Failed to analyze Twitter trends: {str(e)}"
            )
            return {}
    
    def analyze_analytics_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trends in Google Analytics data.
        
        Args:
            df (pd.DataFrame): Transformed analytics data
            
        Returns:
            Dict[str, Any]: Dictionary containing trend analysis results
        """
        try:
            if df.empty:
                return {}
            
            analysis = {
                'session_growth': self._analyze_growth(df, 'Sessions'),
                'user_growth': self._analyze_growth(df, 'Users'),
                'bounce_rate_trend': self._analyze_trend(df, 'Bounce Rate'),
                'pages_per_session_trend': self._analyze_trend(df, 'Pages per Session'),
                'seasonal_patterns': self._analyze_seasonality(df, 'Sessions'),
                'correlation_analysis': self._analyze_correlations(df, ['Sessions', 'Users', 'Pageviews', 'Bounce Rate'])
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "analytics_trend_analysis_completed",
                1,
                {"analysis_count": len(analysis)}
            )
            
            return analysis
            
        except Exception as e:
            self.error_handler.handle_error(
                "TrendAnalysisError",
                f"Failed to analyze analytics trends: {str(e)}"
            )
            return {}
    
    def _analyze_growth(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Analyze growth of a metric over time.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            column (str): Column name to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing growth analysis results
        """
        try:
            if df.empty or column not in df.columns:
                return {}
            
            # Calculate growth rates
            current_value = df[column].iloc[-1]
            previous_value = df[column].iloc[-2] if len(df) > 1 else current_value
            growth_rate = (current_value - previous_value) / previous_value if previous_value != 0 else 0
            
            # Calculate compound growth rate
            if len(df) > 1:
                cagr = (current_value / df[column].iloc[0]) ** (1 / len(df)) - 1
            else:
                cagr = 0
            
            return {
                'current_value': current_value,
                'growth_rate': growth_rate,
                'cagr': cagr,
                'is_growing': growth_rate > 0
            }
            
        except Exception:
            return {}
    
    def _analyze_trend(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Analyze trend of a metric over time.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            column (str): Column name to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing trend analysis results
        """
        try:
            if df.empty or column not in df.columns:
                return {}
            
            # Calculate linear regression
            x = np.arange(len(df))
            y = df[column].values
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            return {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value ** 2,
                'p_value': p_value,
                'is_significant': p_value < 0.05,
                'trend_direction': 'increasing' if slope > 0 else 'decreasing'
            }
            
        except Exception:
            return {}
    
    def _analyze_seasonality(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Analyze seasonality of a metric.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            column (str): Column name to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing seasonality analysis results
        """
        try:
            if df.empty or column not in df.columns:
                return {}
            
            # Calculate daily averages
            df['day_of_week'] = df.index.dayofweek
            daily_avg = df.groupby('day_of_week')[column].mean()
            
            # Calculate weekly averages
            df['week'] = df.index.isocalendar().week
            weekly_avg = df.groupby('week')[column].mean()
            
            return {
                'daily_pattern': daily_avg.to_dict(),
                'weekly_pattern': weekly_avg.to_dict(),
                'has_seasonality': len(set(daily_avg)) > 1
            }
            
        except Exception:
            return {}
    
    def _analyze_correlations(self, df: pd.DataFrame, columns: List[str]) -> Dict[str, Any]:
        """
        Analyze correlations between metrics.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            columns (List[str]): List of column names to analyze
            
        Returns:
            Dict[str, Any]: Dictionary containing correlation analysis results
        """
        try:
            if df.empty or not all(col in df.columns for col in columns):
                return {}
            
            # Calculate correlation matrix
            corr_matrix = df[columns].corr()
            
            # Find strong correlations
            strong_correlations = []
            for i in range(len(columns)):
                for j in range(i + 1, len(columns)):
                    corr = corr_matrix.iloc[i, j]
                    if abs(corr) > 0.7:  # Strong correlation threshold
                        strong_correlations.append({
                            'metric1': columns[i],
                            'metric2': columns[j],
                            'correlation': corr
                        })
            
            return {
                'correlation_matrix': corr_matrix.to_dict(),
                'strong_correlations': strong_correlations
            }
            
        except Exception:
            return {} 