"""
Comparative Analytics Agent for analyzing and comparing performance across different data sources.
"""

from typing import Dict, List, Any, Union
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config
from ..data import DataTransformerAgent, MetricsCalculatorAgent, TrendAnalysisAgent

class ComparativeAnalyticsAgent:
    """Agent responsible for analyzing and comparing performance across different data sources."""
    
    def __init__(self):
        """Initialize the Comparative Analytics Agent."""
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
        self.transformer = DataTransformerAgent()
        self.metrics_calculator = MetricsCalculatorAgent()
        self.trend_analyzer = TrendAnalysisAgent()
    
    def compare_performance(
        self,
        website_data: pd.DataFrame,
        analytics_data: pd.DataFrame,
        twitter_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Compare performance metrics across different data sources.
        
        Args:
            website_data (pd.DataFrame): Raw website data
            analytics_data (pd.DataFrame): Raw Google Analytics data
            twitter_data (pd.DataFrame): Raw Twitter data
            
        Returns:
            Dict[str, Any]: Dictionary containing comparative analysis results
        """
        try:
            # Transform data
            website_df = self.transformer.clean_website_data(website_data)
            analytics_df = self.transformer.clean_analytics_data(analytics_data)
            twitter_df = self.transformer.clean_twitter_data(twitter_data)
            
            # Calculate metrics
            website_metrics = self.metrics_calculator.calculate_website_metrics(website_df)
            analytics_metrics = self.metrics_calculator.calculate_analytics_metrics(analytics_df)
            twitter_metrics = self.metrics_calculator.calculate_twitter_metrics(twitter_df)
            
            # Analyze trends
            website_trends = self.trend_analyzer.analyze_website_trends(website_df)
            analytics_trends = self.trend_analyzer.analyze_analytics_trends(analytics_df)
            twitter_trends = self.trend_analyzer.analyze_twitter_trends(twitter_df)
            
            # Combine results
            analysis = {
                'metrics_comparison': self._compare_metrics(
                    website_metrics, analytics_metrics, twitter_metrics
                ),
                'trend_comparison': self._compare_trends(
                    website_trends, analytics_trends, twitter_trends
                ),
                'correlation_analysis': self._analyze_correlations(
                    website_df, analytics_df, twitter_df
                ),
                'performance_insights': self._generate_comparative_insights(
                    website_metrics, analytics_metrics, twitter_metrics,
                    website_trends, analytics_trends, twitter_trends
                )
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "comparative_analysis_completed",
                1,
                {"analysis_count": len(analysis)}
            )
            
            return analysis
            
        except Exception as e:
            self.error_handler.handle_error(
                "ComparativeAnalysisError",
                f"Failed to compare performance: {str(e)}"
            )
            return {}
    
    def analyze_cross_channel_impact(
        self,
        website_data: pd.DataFrame,
        analytics_data: pd.DataFrame,
        twitter_data: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Analyze impact across different channels.
        
        Args:
            website_data (pd.DataFrame): Raw website data
            analytics_data (pd.DataFrame): Raw Google Analytics data
            twitter_data (pd.DataFrame): Raw Twitter data
            
        Returns:
            Dict[str, Any]: Dictionary containing cross-channel impact analysis results
        """
        try:
            # Transform data
            website_df = self.transformer.clean_website_data(website_data)
            analytics_df = self.transformer.clean_analytics_data(analytics_data)
            twitter_df = self.transformer.clean_twitter_data(twitter_data)
            
            # Analyze impact
            impact_analysis = {
                'twitter_to_website': self._analyze_twitter_website_impact(twitter_df, website_df),
                'social_to_analytics': self._analyze_social_analytics_impact(twitter_df, analytics_df),
                'channel_synergy': self._analyze_channel_synergy(website_df, analytics_df, twitter_df)
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "cross_channel_impact_analysis_completed",
                1,
                {"analysis_count": len(impact_analysis)}
            )
            
            return impact_analysis
            
        except Exception as e:
            self.error_handler.handle_error(
                "CrossChannelAnalysisError",
                f"Failed to analyze cross-channel impact: {str(e)}"
            )
            return {}
    
    def _compare_metrics(
        self,
        website_metrics: Dict[str, Any],
        analytics_metrics: Dict[str, Any],
        twitter_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare metrics across different data sources.
        
        Args:
            website_metrics (Dict[str, Any]): Website metrics
            analytics_metrics (Dict[str, Any]): Analytics metrics
            twitter_metrics (Dict[str, Any]): Twitter metrics
            
        Returns:
            Dict[str, Any]: Metrics comparison results
        """
        try:
            comparison = {
                'traffic_sources': {
                    'website': website_metrics.get('total_visitors', 0),
                    'analytics': analytics_metrics.get('total_users', 0),
                    'twitter': twitter_metrics.get('total_reach', 0)
                },
                'engagement_rates': {
                    'website': website_metrics.get('avg_session_duration', 0),
                    'analytics': analytics_metrics.get('avg_session_duration', 0),
                    'twitter': twitter_metrics.get('engagement_rate', 0)
                },
                'growth_rates': {
                    'website': website_metrics.get('visitor_growth', 0),
                    'analytics': analytics_metrics.get('user_growth', 0),
                    'twitter': twitter_metrics.get('follower_growth', 0)
                }
            }
            
            return comparison
            
        except Exception:
            return {}
    
    def _compare_trends(
        self,
        website_trends: Dict[str, Any],
        analytics_trends: Dict[str, Any],
        twitter_trends: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compare trends across different data sources.
        
        Args:
            website_trends (Dict[str, Any]): Website trends
            analytics_trends (Dict[str, Any]): Analytics trends
            twitter_trends (Dict[str, Any]): Twitter trends
            
        Returns:
            Dict[str, Any]: Trends comparison results
        """
        try:
            comparison = {
                'growth_trends': {
                    'website': website_trends.get('visitor_growth', {}),
                    'analytics': analytics_trends.get('user_growth', {}),
                    'twitter': twitter_trends.get('follower_growth', {})
                },
                'engagement_trends': {
                    'website': website_trends.get('session_duration_trend', {}),
                    'analytics': analytics_trends.get('session_duration_trend', {}),
                    'twitter': twitter_trends.get('engagement_trend', {})
                },
                'seasonal_patterns': {
                    'website': website_trends.get('seasonal_patterns', {}),
                    'analytics': analytics_trends.get('seasonal_patterns', {}),
                    'twitter': twitter_trends.get('seasonal_patterns', {})
                }
            }
            
            return comparison
            
        except Exception:
            return {}
    
    def _analyze_correlations(
        self,
        website_df: pd.DataFrame,
        analytics_df: pd.DataFrame,
        twitter_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Analyze correlations between different data sources.
        
        Args:
            website_df (pd.DataFrame): Website data
            analytics_df (pd.DataFrame): Analytics data
            twitter_df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Correlation analysis results
        """
        try:
            # Merge datasets on date
            merged_df = self._merge_datasets(website_df, analytics_df, twitter_df)
            
            if merged_df.empty:
                return {}
            
            # Calculate correlations
            correlations = {
                'twitter_website': self._calculate_correlation(
                    merged_df, 'total_engagement', 'total_visitors'
                ),
                'twitter_analytics': self._calculate_correlation(
                    merged_df, 'total_engagement', 'total_users'
                ),
                'website_analytics': self._calculate_correlation(
                    merged_df, 'total_visitors', 'total_users'
                )
            }
            
            return correlations
            
        except Exception:
            return {}
    
    def _generate_comparative_insights(
        self,
        website_metrics: Dict[str, Any],
        analytics_metrics: Dict[str, Any],
        twitter_metrics: Dict[str, Any],
        website_trends: Dict[str, Any],
        analytics_trends: Dict[str, Any],
        twitter_trends: Dict[str, Any]
    ) -> List[str]:
        """
        Generate insights from comparative analysis.
        
        Args:
            website_metrics (Dict[str, Any]): Website metrics
            analytics_metrics (Dict[str, Any]): Analytics metrics
            twitter_metrics (Dict[str, Any]): Twitter metrics
            website_trends (Dict[str, Any]): Website trends
            analytics_trends (Dict[str, Any]): Analytics trends
            twitter_trends (Dict[str, Any]): Twitter trends
            
        Returns:
            List[str]: List of comparative insights
        """
        insights = []
        
        # Compare growth rates
        website_growth = website_trends.get('visitor_growth', {}).get('growth_rate', 0)
        twitter_growth = twitter_trends.get('follower_growth', {}).get('growth_rate', 0)
        
        if website_growth > twitter_growth:
            insights.append("Website growth is outpacing Twitter growth")
        else:
            insights.append("Twitter growth is outpacing website growth")
        
        # Compare engagement rates
        website_engagement = website_metrics.get('avg_session_duration', 0)
        twitter_engagement = twitter_metrics.get('engagement_rate', 0)
        
        if website_engagement > 180 and twitter_engagement > 0.02:
            insights.append("Both website and Twitter show strong engagement")
        elif website_engagement > 180:
            insights.append("Website engagement is strong, but Twitter needs improvement")
        elif twitter_engagement > 0.02:
            insights.append("Twitter engagement is strong, but website needs improvement")
        else:
            insights.append("Both website and Twitter engagement need improvement")
        
        # Analyze channel synergy
        if website_trends.get('visitor_growth', {}).get('is_growing', False) and \
           twitter_trends.get('follower_growth', {}).get('is_growing', False):
            insights.append("Positive growth across all channels indicates strong channel synergy")
        else:
            insights.append("Channel growth is uneven - consider cross-channel optimization")
        
        return insights
    
    def _analyze_twitter_website_impact(
        self,
        twitter_df: pd.DataFrame,
        website_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Analyze impact of Twitter activity on website traffic.
        
        Args:
            twitter_df (pd.DataFrame): Twitter data
            website_df (pd.DataFrame): Website data
            
        Returns:
            Dict[str, Any]: Twitter-Website impact analysis
        """
        try:
            # Merge datasets on date
            merged_df = self._merge_datasets(website_df, None, twitter_df)
            
            if merged_df.empty:
                return {}
            
            # Calculate impact metrics
            impact_metrics = {
                'correlation': self._calculate_correlation(
                    merged_df, 'total_engagement', 'total_visitors'
                ),
                'lag_analysis': self._analyze_lag_impact(
                    merged_df, 'total_engagement', 'total_visitors'
                ),
                'content_impact': self._analyze_content_impact(
                    merged_df, 'total_engagement', 'total_visitors'
                )
            }
            
            return impact_metrics
            
        except Exception:
            return {}
    
    def _analyze_social_analytics_impact(
        self,
        twitter_df: pd.DataFrame,
        analytics_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Analyze impact of social media on analytics metrics.
        
        Args:
            twitter_df (pd.DataFrame): Twitter data
            analytics_df (pd.DataFrame): Analytics data
            
        Returns:
            Dict[str, Any]: Social-Analytics impact analysis
        """
        try:
            # Merge datasets on date
            merged_df = self._merge_datasets(None, analytics_df, twitter_df)
            
            if merged_df.empty:
                return {}
            
            # Calculate impact metrics
            impact_metrics = {
                'correlation': self._calculate_correlation(
                    merged_df, 'total_engagement', 'total_users'
                ),
                'lag_analysis': self._analyze_lag_impact(
                    merged_df, 'total_engagement', 'total_users'
                ),
                'conversion_impact': self._analyze_conversion_impact(
                    merged_df, 'total_engagement', 'total_users'
                )
            }
            
            return impact_metrics
            
        except Exception:
            return {}
    
    def _analyze_channel_synergy(
        self,
        website_df: pd.DataFrame,
        analytics_df: pd.DataFrame,
        twitter_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Analyze synergy between different channels.
        
        Args:
            website_df (pd.DataFrame): Website data
            analytics_df (pd.DataFrame): Analytics data
            twitter_df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Channel synergy analysis
        """
        try:
            # Merge datasets
            merged_df = self._merge_datasets(website_df, analytics_df, twitter_df)
            
            if merged_df.empty:
                return {}
            
            # Calculate synergy metrics
            synergy_metrics = {
                'cross_channel_correlation': self._calculate_cross_channel_correlation(merged_df),
                'channel_contribution': self._analyze_channel_contribution(merged_df),
                'optimal_mix': self._determine_optimal_channel_mix(merged_df)
            }
            
            return synergy_metrics
            
        except Exception:
            return {}
    
    def _merge_datasets(
        self,
        website_df: pd.DataFrame,
        analytics_df: pd.DataFrame,
        twitter_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Merge datasets from different sources.
        
        Args:
            website_df (pd.DataFrame): Website data
            analytics_df (pd.DataFrame): Analytics data
            twitter_df (pd.DataFrame): Twitter data
            
        Returns:
            pd.DataFrame: Merged dataset
        """
        try:
            dfs = []
            
            if website_df is not None:
                website_df['date'] = pd.to_datetime(website_df['Date']).dt.date
                dfs.append(website_df)
            
            if analytics_df is not None:
                analytics_df['date'] = pd.to_datetime(analytics_df['Date']).dt.date
                dfs.append(analytics_df)
            
            if twitter_df is not None:
                twitter_df['date'] = pd.to_datetime(twitter_df['created_at']).dt.date
                dfs.append(twitter_df)
            
            if not dfs:
                return pd.DataFrame()
            
            # Merge all datasets
            merged_df = dfs[0]
            for df in dfs[1:]:
                merged_df = pd.merge(merged_df, df, on='date', how='outer')
            
            return merged_df
            
        except Exception:
            return pd.DataFrame()
    
    def _calculate_correlation(
        self,
        df: pd.DataFrame,
        col1: str,
        col2: str
    ) -> Dict[str, float]:
        """
        Calculate correlation between two columns.
        
        Args:
            df (pd.DataFrame): Dataframe containing the columns
            col1 (str): First column name
            col2 (str): Second column name
            
        Returns:
            Dict[str, float]: Correlation metrics
        """
        try:
            if col1 not in df.columns or col2 not in df.columns:
                return {}
            
            correlation = df[col1].corr(df[col2])
            
            return {
                'correlation_coefficient': correlation,
                'strength': 'strong' if abs(correlation) > 0.7 else 'moderate' if abs(correlation) > 0.3 else 'weak',
                'direction': 'positive' if correlation > 0 else 'negative'
            }
            
        except Exception:
            return {}
    
    def _analyze_lag_impact(
        self,
        df: pd.DataFrame,
        cause_col: str,
        effect_col: str,
        max_lag: int = 7
    ) -> Dict[str, Any]:
        """
        Analyze impact with different time lags.
        
        Args:
            df (pd.DataFrame): Dataframe containing the columns
            cause_col (str): Cause column name
            effect_col (str): Effect column name
            max_lag (int): Maximum number of days to lag
            
        Returns:
            Dict[str, Any]: Lag impact analysis
        """
        try:
            if cause_col not in df.columns or effect_col not in df.columns:
                return {}
            
            lag_analysis = {}
            for lag in range(max_lag + 1):
                correlation = df[cause_col].shift(lag).corr(df[effect_col])
                lag_analysis[f'lag_{lag}'] = correlation
            
            # Find optimal lag
            optimal_lag = max(lag_analysis.items(), key=lambda x: abs(x[1]))[0]
            
            return {
                'lag_correlations': lag_analysis,
                'optimal_lag': optimal_lag,
                'max_correlation': lag_analysis[optimal_lag]
            }
            
        except Exception:
            return {}
    
    def _analyze_content_impact(
        self,
        df: pd.DataFrame,
        engagement_col: str,
        traffic_col: str
    ) -> Dict[str, Any]:
        """
        Analyze impact of content on traffic.
        
        Args:
            df (pd.DataFrame): Dataframe containing the columns
            engagement_col (str): Engagement column name
            traffic_col (str): Traffic column name
            
        Returns:
            Dict[str, Any]: Content impact analysis
        """
        try:
            if engagement_col not in df.columns or traffic_col not in df.columns:
                return {}
            
            # Calculate content impact metrics
            impact_metrics = {
                'avg_traffic_per_engagement': df[traffic_col].sum() / df[engagement_col].sum(),
                'engagement_traffic_ratio': df[engagement_col].sum() / df[traffic_col].sum(),
                'high_engagement_days': len(df[df[engagement_col] > df[engagement_col].mean()])
            }
            
            return impact_metrics
            
        except Exception:
            return {}
    
    def _analyze_conversion_impact(
        self,
        df: pd.DataFrame,
        engagement_col: str,
        conversion_col: str
    ) -> Dict[str, Any]:
        """
        Analyze impact of engagement on conversions.
        
        Args:
            df (pd.DataFrame): Dataframe containing the columns
            engagement_col (str): Engagement column name
            conversion_col (str): Conversion column name
            
        Returns:
            Dict[str, Any]: Conversion impact analysis
        """
        try:
            if engagement_col not in df.columns or conversion_col not in df.columns:
                return {}
            
            # Calculate conversion impact metrics
            impact_metrics = {
                'conversion_rate': df[conversion_col].sum() / df[engagement_col].sum(),
                'engagement_conversion_ratio': df[engagement_col].sum() / df[conversion_col].sum(),
                'high_conversion_days': len(df[df[conversion_col] > df[conversion_col].mean()])
            }
            
            return impact_metrics
            
        except Exception:
            return {}
    
    def _calculate_cross_channel_correlation(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate correlations between all channels.
        
        Args:
            df (pd.DataFrame): Merged dataset
            
        Returns:
            Dict[str, Any]: Cross-channel correlation analysis
        """
        try:
            # Define channel metrics
            channel_metrics = {
                'website': ['total_visitors', 'avg_session_duration'],
                'analytics': ['total_users', 'avg_session_duration'],
                'twitter': ['total_engagement', 'engagement_rate']
            }
            
            correlations = {}
            for channel1, metrics1 in channel_metrics.items():
                for channel2, metrics2 in channel_metrics.items():
                    if channel1 != channel2:
                        for metric1 in metrics1:
                            for metric2 in metrics2:
                                if metric1 in df.columns and metric2 in df.columns:
                                    correlation = df[metric1].corr(df[metric2])
                                    correlations[f'{channel1}_{metric1}_{channel2}_{metric2}'] = correlation
            
            return correlations
            
        except Exception:
            return {}
    
    def _analyze_channel_contribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze contribution of each channel to overall performance.
        
        Args:
            df (pd.DataFrame): Merged dataset
            
        Returns:
            Dict[str, Any]: Channel contribution analysis
        """
        try:
            # Calculate total metrics
            total_visitors = df['total_visitors'].sum()
            total_users = df['total_users'].sum()
            total_engagement = df['total_engagement'].sum()
            
            # Calculate channel contributions
            contributions = {
                'website_contribution': total_visitors / (total_visitors + total_users + total_engagement),
                'analytics_contribution': total_users / (total_visitors + total_users + total_engagement),
                'twitter_contribution': total_engagement / (total_visitors + total_users + total_engagement)
            }
            
            return contributions
            
        except Exception:
            return {}
    
    def _determine_optimal_channel_mix(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Determine optimal mix of channels based on performance.
        
        Args:
            df (pd.DataFrame): Merged dataset
            
        Returns:
            Dict[str, Any]: Optimal channel mix analysis
        """
        try:
            # Calculate performance metrics
            website_performance = df['total_visitors'].mean() / df['total_visitors'].std()
            analytics_performance = df['total_users'].mean() / df['total_users'].std()
            twitter_performance = df['total_engagement'].mean() / df['total_engagement'].std()
            
            # Calculate optimal mix
            total_performance = website_performance + analytics_performance + twitter_performance
            
            optimal_mix = {
                'website_share': website_performance / total_performance,
                'analytics_share': analytics_performance / total_performance,
                'twitter_share': twitter_performance / total_performance
            }
            
            return optimal_mix
            
        except Exception:
            return {} 