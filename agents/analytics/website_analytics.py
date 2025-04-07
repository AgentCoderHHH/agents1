"""
Website Analytics Agent for analyzing website performance and user behavior.
"""

from typing import Dict, List, Any, Union
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config
from ..data import DataTransformerAgent, MetricsCalculatorAgent, TrendAnalysisAgent

class WebsiteAnalyticsAgent:
    """Agent responsible for analyzing website performance and user behavior."""
    
    def __init__(self):
        """Initialize the Website Analytics Agent."""
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
        self.transformer = DataTransformerAgent()
        self.metrics_calculator = MetricsCalculatorAgent()
        self.trend_analyzer = TrendAnalysisAgent()
    
    def analyze_performance(self, website_data: pd.DataFrame, analytics_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze website performance metrics.
        
        Args:
            website_data (pd.DataFrame): Raw website data
            analytics_data (pd.DataFrame): Raw Google Analytics data
            
        Returns:
            Dict[str, Any]: Dictionary containing performance analysis results
        """
        try:
            # Transform data
            website_df = self.transformer.clean_website_data(website_data)
            analytics_df = self.transformer.clean_analytics_data(analytics_data)
            
            # Calculate metrics
            website_metrics = self.metrics_calculator.calculate_website_metrics(website_df)
            analytics_metrics = self.metrics_calculator.calculate_analytics_metrics(analytics_df)
            
            # Analyze trends
            website_trends = self.trend_analyzer.analyze_website_trends(website_df)
            analytics_trends = self.trend_analyzer.analyze_analytics_trends(analytics_df)
            
            # Combine results
            analysis = {
                'website_metrics': website_metrics,
                'analytics_metrics': analytics_metrics,
                'website_trends': website_trends,
                'analytics_trends': analytics_trends,
                'performance_insights': self._generate_performance_insights(
                    website_metrics, analytics_metrics, website_trends, analytics_trends
                )
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "website_performance_analysis_completed",
                1,
                {"analysis_count": len(analysis)}
            )
            
            return analysis
            
        except Exception as e:
            self.error_handler.handle_error(
                "WebsiteAnalysisError",
                f"Failed to analyze website performance: {str(e)}"
            )
            return {}
    
    def analyze_user_behavior(self, analytics_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze user behavior patterns.
        
        Args:
            analytics_data (pd.DataFrame): Raw Google Analytics data
            
        Returns:
            Dict[str, Any]: Dictionary containing user behavior analysis results
        """
        try:
            # Transform data
            df = self.transformer.clean_analytics_data(analytics_data)
            
            # Calculate user behavior metrics
            behavior_metrics = {
                'avg_session_duration': df['Avg. Session Duration'].mean(),
                'avg_pages_per_session': df['Pages per Session'].mean(),
                'bounce_rate': df['Bounce Rate'].mean(),
                'new_vs_returning': self._analyze_user_types(df),
                'session_distribution': self._analyze_session_distribution(df),
                'page_engagement': self._analyze_page_engagement(df)
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "user_behavior_analysis_completed",
                1,
                {"metrics_count": len(behavior_metrics)}
            )
            
            return behavior_metrics
            
        except Exception as e:
            self.error_handler.handle_error(
                "UserBehaviorAnalysisError",
                f"Failed to analyze user behavior: {str(e)}"
            )
            return {}
    
    def analyze_traffic_sources(self, analytics_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze traffic sources and their performance.
        
        Args:
            analytics_data (pd.DataFrame): Raw Google Analytics data
            
        Returns:
            Dict[str, Any]: Dictionary containing traffic source analysis results
        """
        try:
            # Transform data
            df = self.transformer.clean_analytics_data(analytics_data)
            
            # Calculate traffic source metrics
            traffic_metrics = {
                'source_distribution': self._analyze_source_distribution(df),
                'source_performance': self._analyze_source_performance(df),
                'source_trends': self._analyze_source_trends(df)
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "traffic_source_analysis_completed",
                1,
                {"metrics_count": len(traffic_metrics)}
            )
            
            return traffic_metrics
            
        except Exception as e:
            self.error_handler.handle_error(
                "TrafficSourceAnalysisError",
                f"Failed to analyze traffic sources: {str(e)}"
            )
            return {}
    
    def _generate_performance_insights(
        self,
        website_metrics: Dict[str, Any],
        analytics_metrics: Dict[str, Any],
        website_trends: Dict[str, Any],
        analytics_trends: Dict[str, Any]
    ) -> List[str]:
        """
        Generate performance insights from metrics and trends.
        
        Args:
            website_metrics (Dict[str, Any]): Website metrics
            analytics_metrics (Dict[str, Any]): Analytics metrics
            website_trends (Dict[str, Any]): Website trends
            analytics_trends (Dict[str, Any]): Analytics trends
            
        Returns:
            List[str]: List of performance insights
        """
        insights = []
        
        # Analyze visitor trends
        if website_trends.get('visitor_growth', {}).get('is_growing', False):
            insights.append("Website traffic is showing positive growth")
        else:
            insights.append("Website traffic growth needs attention")
        
        # Analyze engagement metrics
        if analytics_metrics.get('avg_session_duration', 0) > 180:
            insights.append("Users are spending significant time on the website")
        else:
            insights.append("Consider improving content engagement")
        
        # Analyze bounce rate
        if analytics_metrics.get('bounce_rate', 0) < 0.4:
            insights.append("Bounce rate is at a healthy level")
        else:
            insights.append("High bounce rate detected - review landing pages")
        
        # Analyze conversion trends
        if analytics_trends.get('conversion_trend', {}).get('is_increasing', False):
            insights.append("Conversion rates are improving")
        else:
            insights.append("Conversion optimization needed")
        
        return insights
    
    def _analyze_user_types(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Analyze distribution of new vs returning users.
        
        Args:
            df (pd.DataFrame): Analytics data
            
        Returns:
            Dict[str, float]: Distribution of user types
        """
        try:
            if 'User Type' not in df.columns:
                return {}
            
            user_distribution = df['User Type'].value_counts(normalize=True)
            return user_distribution.to_dict()
            
        except Exception:
            return {}
    
    def _analyze_session_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze distribution of session durations.
        
        Args:
            df (pd.DataFrame): Analytics data
            
        Returns:
            Dict[str, Any]: Session distribution metrics
        """
        try:
            if 'Session Duration' not in df.columns:
                return {}
            
            session_stats = {
                'mean': df['Session Duration'].mean(),
                'median': df['Session Duration'].median(),
                'distribution': df['Session Duration'].value_counts(bins=5).to_dict()
            }
            
            return session_stats
            
        except Exception:
            return {}
    
    def _analyze_page_engagement(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze page engagement metrics.
        
        Args:
            df (pd.DataFrame): Analytics data
            
        Returns:
            Dict[str, Any]: Page engagement metrics
        """
        try:
            if 'Pageviews' not in df.columns or 'Unique Pageviews' not in df.columns:
                return {}
            
            engagement_metrics = {
                'avg_pageviews': df['Pageviews'].mean(),
                'avg_unique_pageviews': df['Unique Pageviews'].mean(),
                'pages_per_session': df['Pageviews'].sum() / df['Sessions'].sum(),
                'top_pages': df.nlargest(5, 'Pageviews')[['Page', 'Pageviews']].to_dict('records')
            }
            
            return engagement_metrics
            
        except Exception:
            return {}
    
    def _analyze_source_distribution(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Analyze distribution of traffic sources.
        
        Args:
            df (pd.DataFrame): Analytics data
            
        Returns:
            Dict[str, float]: Source distribution
        """
        try:
            if 'Source' not in df.columns:
                return {}
            
            source_distribution = df['Source'].value_counts(normalize=True)
            return source_distribution.to_dict()
            
        except Exception:
            return {}
    
    def _analyze_source_performance(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze performance metrics by traffic source.
        
        Args:
            df (pd.DataFrame): Analytics data
            
        Returns:
            Dict[str, Any]: Source performance metrics
        """
        try:
            if 'Source' not in df.columns:
                return {}
            
            source_metrics = df.groupby('Source').agg({
                'Sessions': 'sum',
                'Bounce Rate': 'mean',
                'Pages per Session': 'mean',
                'Avg. Session Duration': 'mean'
            }).to_dict('index')
            
            return source_metrics
            
        except Exception:
            return {}
    
    def _analyze_source_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trends in traffic sources.
        
        Args:
            df (pd.DataFrame): Analytics data
            
        Returns:
            Dict[str, Any]: Source trend analysis
        """
        try:
            if 'Source' not in df.columns or 'Date' not in df.columns:
                return {}
            
            # Calculate source growth rates
            source_growth = {}
            for source in df['Source'].unique():
                source_data = df[df['Source'] == source]
                if len(source_data) > 1:
                    growth_rate = (source_data['Sessions'].iloc[-1] - source_data['Sessions'].iloc[0]) / source_data['Sessions'].iloc[0]
                    source_growth[source] = growth_rate
            
            return {
                'source_growth': source_growth,
                'top_growing_sources': sorted(source_growth.items(), key=lambda x: x[1], reverse=True)[:5]
            }
            
        except Exception:
            return {} 