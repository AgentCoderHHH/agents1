"""
Social Media Analytics Agent for analyzing social media performance and engagement.
"""

from typing import Dict, List, Any, Union
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config
from ..data import DataTransformerAgent, MetricsCalculatorAgent, TrendAnalysisAgent

class SocialMediaAnalyticsAgent:
    """Agent responsible for analyzing social media performance and engagement."""
    
    def __init__(self):
        """Initialize the Social Media Analytics Agent."""
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
        self.transformer = DataTransformerAgent()
        self.metrics_calculator = MetricsCalculatorAgent()
        self.trend_analyzer = TrendAnalysisAgent()
    
    def analyze_twitter_performance(self, twitter_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze Twitter performance metrics.
        
        Args:
            twitter_data (pd.DataFrame): Raw Twitter data
            
        Returns:
            Dict[str, Any]: Dictionary containing Twitter performance analysis results
        """
        try:
            # Transform data
            df = self.transformer.clean_twitter_data(twitter_data)
            
            # Calculate metrics
            metrics = self.metrics_calculator.calculate_twitter_metrics(df)
            
            # Analyze trends
            trends = self.trend_analyzer.analyze_twitter_trends(df)
            
            # Combine results
            analysis = {
                'metrics': metrics,
                'trends': trends,
                'performance_insights': self._generate_twitter_insights(metrics, trends),
                'content_analysis': self._analyze_twitter_content(df),
                'audience_analysis': self._analyze_twitter_audience(df)
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "twitter_performance_analysis_completed",
                1,
                {"analysis_count": len(analysis)}
            )
            
            return analysis
            
        except Exception as e:
            self.error_handler.handle_error(
                "TwitterAnalysisError",
                f"Failed to analyze Twitter performance: {str(e)}"
            )
            return {}
    
    def analyze_engagement(self, twitter_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze social media engagement patterns.
        
        Args:
            twitter_data (pd.DataFrame): Raw Twitter data
            
        Returns:
            Dict[str, Any]: Dictionary containing engagement analysis results
        """
        try:
            # Transform data
            df = self.transformer.clean_twitter_data(twitter_data)
            
            # Calculate engagement metrics
            engagement_metrics = {
                'total_engagement': df['total_engagement'].sum(),
                'avg_engagement': df['total_engagement'].mean(),
                'engagement_rate': df['total_engagement'].sum() / df['user_followers'].sum(),
                'engagement_distribution': self._analyze_engagement_distribution(df),
                'top_engaging_tweets': self._get_top_engaging_tweets(df),
                'engagement_trends': self._analyze_engagement_trends(df)
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "social_media_engagement_analysis_completed",
                1,
                {"metrics_count": len(engagement_metrics)}
            )
            
            return engagement_metrics
            
        except Exception as e:
            self.error_handler.handle_error(
                "EngagementAnalysisError",
                f"Failed to analyze social media engagement: {str(e)}"
            )
            return {}
    
    def analyze_content_performance(self, twitter_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze content performance and effectiveness.
        
        Args:
            twitter_data (pd.DataFrame): Raw Twitter data
            
        Returns:
            Dict[str, Any]: Dictionary containing content performance analysis results
        """
        try:
            # Transform data
            df = self.transformer.clean_twitter_data(twitter_data)
            
            # Calculate content metrics
            content_metrics = {
                'content_types': self._analyze_content_types(df),
                'best_performing_content': self._get_best_performing_content(df),
                'content_trends': self._analyze_content_trends(df),
                'optimal_posting_times': self._analyze_posting_times(df)
            }
            
            # Log analysis
            self.monitoring.log_metric(
                "content_performance_analysis_completed",
                1,
                {"metrics_count": len(content_metrics)}
            )
            
            return content_metrics
            
        except Exception as e:
            self.error_handler.handle_error(
                "ContentAnalysisError",
                f"Failed to analyze content performance: {str(e)}"
            )
            return {}
    
    def _generate_twitter_insights(
        self,
        metrics: Dict[str, Any],
        trends: Dict[str, Any]
    ) -> List[str]:
        """
        Generate insights from Twitter metrics and trends.
        
        Args:
            metrics (Dict[str, Any]): Twitter metrics
            trends (Dict[str, Any]): Twitter trends
            
        Returns:
            List[str]: List of Twitter insights
        """
        insights = []
        
        # Analyze engagement trends
        if trends.get('engagement_growth', {}).get('is_growing', False):
            insights.append("Twitter engagement is showing positive growth")
        else:
            insights.append("Twitter engagement growth needs attention")
        
        # Analyze engagement rate
        if metrics.get('engagement_rate', 0) > 0.02:
            insights.append("Engagement rate is above industry average")
        else:
            insights.append("Consider improving content engagement")
        
        # Analyze follower growth
        if trends.get('follower_growth', {}).get('is_growing', False):
            insights.append("Follower base is growing steadily")
        else:
            insights.append("Follower growth needs improvement")
        
        # Analyze content performance
        if metrics.get('avg_engagement', 0) > metrics.get('previous_avg_engagement', 0):
            insights.append("Content performance is improving")
        else:
            insights.append("Content strategy needs review")
        
        return insights
    
    def _analyze_twitter_content(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze Twitter content characteristics.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Content analysis results
        """
        try:
            content_analysis = {
                'tweet_length_distribution': self._analyze_tweet_lengths(df),
                'hashtag_usage': self._analyze_hashtag_usage(df),
                'mention_usage': self._analyze_mention_usage(df),
                'media_usage': self._analyze_media_usage(df)
            }
            
            return content_analysis
            
        except Exception:
            return {}
    
    def _analyze_twitter_audience(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze Twitter audience characteristics.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Audience analysis results
        """
        try:
            audience_analysis = {
                'follower_growth': self._analyze_follower_growth(df),
                'audience_engagement': self._analyze_audience_engagement(df),
                'active_followers': self._analyze_active_followers(df)
            }
            
            return audience_analysis
            
        except Exception:
            return {}
    
    def _analyze_engagement_distribution(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze distribution of engagement metrics.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Engagement distribution metrics
        """
        try:
            engagement_stats = {
                'retweet_distribution': df['retweet_count'].value_counts(bins=5).to_dict(),
                'like_distribution': df['favorite_count'].value_counts(bins=5).to_dict(),
                'reply_distribution': df['reply_count'].value_counts(bins=5).to_dict()
            }
            
            return engagement_stats
            
        except Exception:
            return {}
    
    def _get_top_engaging_tweets(self, df: pd.DataFrame, n: int = 5) -> List[Dict[str, Any]]:
        """
        Get top engaging tweets.
        
        Args:
            df (pd.DataFrame): Twitter data
            n (int): Number of top tweets to return
            
        Returns:
            List[Dict[str, Any]]: List of top engaging tweets
        """
        try:
            top_tweets = df.nlargest(n, 'total_engagement')
            return top_tweets[['tweet_id', 'text', 'total_engagement']].to_dict('records')
            
        except Exception:
            return []
    
    def _analyze_engagement_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trends in engagement metrics.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Engagement trend analysis
        """
        try:
            if 'created_at' not in df.columns:
                return {}
            
            # Calculate daily engagement
            daily_engagement = df.groupby(df['created_at'].dt.date)['total_engagement'].sum()
            
            # Calculate engagement trends
            engagement_trends = {
                'daily_engagement': daily_engagement.to_dict(),
                'avg_daily_engagement': daily_engagement.mean(),
                'engagement_growth': (daily_engagement.iloc[-1] - daily_engagement.iloc[0]) / daily_engagement.iloc[0]
            }
            
            return engagement_trends
            
        except Exception:
            return {}
    
    def _analyze_content_types(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Analyze distribution of content types.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, float]: Content type distribution
        """
        try:
            content_types = {
                'text_only': len(df[df['media_type'].isna()]) / len(df),
                'with_media': len(df[df['media_type'].notna()]) / len(df),
                'with_links': len(df[df['urls'].notna()]) / len(df)
            }
            
            return content_types
            
        except Exception:
            return {}
    
    def _get_best_performing_content(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get best performing content by type.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Best performing content analysis
        """
        try:
            best_content = {
                'text_tweets': df[df['media_type'].isna()].nlargest(3, 'total_engagement')[['text', 'total_engagement']].to_dict('records'),
                'media_tweets': df[df['media_type'].notna()].nlargest(3, 'total_engagement')[['text', 'media_type', 'total_engagement']].to_dict('records'),
                'link_tweets': df[df['urls'].notna()].nlargest(3, 'total_engagement')[['text', 'urls', 'total_engagement']].to_dict('records')
            }
            
            return best_content
            
        except Exception:
            return {}
    
    def _analyze_content_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze trends in content performance.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Content trend analysis
        """
        try:
            if 'created_at' not in df.columns:
                return {}
            
            # Calculate content performance by type
            content_trends = {
                'text_performance': df[df['media_type'].isna()].groupby(df['created_at'].dt.date)['total_engagement'].mean().to_dict(),
                'media_performance': df[df['media_type'].notna()].groupby(df['created_at'].dt.date)['total_engagement'].mean().to_dict(),
                'link_performance': df[df['urls'].notna()].groupby(df['created_at'].dt.date)['total_engagement'].mean().to_dict()
            }
            
            return content_trends
            
        except Exception:
            return {}
    
    def _analyze_posting_times(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze optimal posting times.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Posting time analysis
        """
        try:
            if 'created_at' not in df.columns:
                return {}
            
            # Calculate engagement by hour
            df['hour'] = df['created_at'].dt.hour
            engagement_by_hour = df.groupby('hour')['total_engagement'].mean()
            
            # Find optimal posting times
            optimal_times = {
                'best_hours': engagement_by_hour.nlargest(3).index.tolist(),
                'worst_hours': engagement_by_hour.nsmallest(3).index.tolist(),
                'hourly_engagement': engagement_by_hour.to_dict()
            }
            
            return optimal_times
            
        except Exception:
            return {}
    
    def _analyze_tweet_lengths(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze distribution of tweet lengths.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Tweet length analysis
        """
        try:
            if 'text' not in df.columns:
                return {}
            
            df['tweet_length'] = df['text'].str.len()
            length_stats = {
                'mean_length': df['tweet_length'].mean(),
                'median_length': df['tweet_length'].median(),
                'length_distribution': df['tweet_length'].value_counts(bins=5).to_dict()
            }
            
            return length_stats
            
        except Exception:
            return {}
    
    def _analyze_hashtag_usage(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze hashtag usage patterns.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Hashtag analysis
        """
        try:
            if 'hashtags' not in df.columns:
                return {}
            
            hashtag_analysis = {
                'avg_hashtags': df['hashtags'].str.len().mean(),
                'top_hashtags': df['hashtags'].explode().value_counts().head(10).to_dict(),
                'hashtag_engagement': self._analyze_hashtag_engagement(df)
            }
            
            return hashtag_analysis
            
        except Exception:
            return {}
    
    def _analyze_mention_usage(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze mention usage patterns.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Mention analysis
        """
        try:
            if 'mentions' not in df.columns:
                return {}
            
            mention_analysis = {
                'avg_mentions': df['mentions'].str.len().mean(),
                'top_mentioned': df['mentions'].explode().value_counts().head(10).to_dict(),
                'mention_engagement': self._analyze_mention_engagement(df)
            }
            
            return mention_analysis
            
        except Exception:
            return {}
    
    def _analyze_media_usage(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze media usage patterns.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Media analysis
        """
        try:
            if 'media_type' not in df.columns:
                return {}
            
            media_analysis = {
                'media_distribution': df['media_type'].value_counts(normalize=True).to_dict(),
                'media_engagement': df.groupby('media_type')['total_engagement'].mean().to_dict()
            }
            
            return media_analysis
            
        except Exception:
            return {}
    
    def _analyze_follower_growth(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze follower growth patterns.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Follower growth analysis
        """
        try:
            if 'user_followers' not in df.columns or 'created_at' not in df.columns:
                return {}
            
            # Calculate daily follower counts
            daily_followers = df.groupby(df['created_at'].dt.date)['user_followers'].max()
            
            follower_growth = {
                'current_followers': daily_followers.iloc[-1],
                'growth_rate': (daily_followers.iloc[-1] - daily_followers.iloc[0]) / daily_followers.iloc[0],
                'daily_growth': daily_followers.diff().mean()
            }
            
            return follower_growth
            
        except Exception:
            return {}
    
    def _analyze_audience_engagement(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze audience engagement patterns.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Audience engagement analysis
        """
        try:
            if 'user_followers' not in df.columns:
                return {}
            
            engagement_analysis = {
                'avg_engagement_rate': (df['total_engagement'].sum() / df['user_followers'].sum()),
                'active_audience_ratio': len(df[df['total_engagement'] > 0]) / len(df),
                'engagement_distribution': df['total_engagement'].value_counts(bins=5).to_dict()
            }
            
            return engagement_analysis
            
        except Exception:
            return {}
    
    def _analyze_active_followers(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze active follower patterns.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, Any]: Active follower analysis
        """
        try:
            if 'user_followers' not in df.columns or 'created_at' not in df.columns:
                return {}
            
            # Calculate daily active followers
            daily_active = df.groupby(df['created_at'].dt.date)['user_followers'].count()
            
            active_analysis = {
                'avg_daily_active': daily_active.mean(),
                'active_growth': (daily_active.iloc[-1] - daily_active.iloc[0]) / daily_active.iloc[0],
                'active_ratio': daily_active.mean() / df['user_followers'].mean()
            }
            
            return active_analysis
            
        except Exception:
            return {}
    
    def _analyze_hashtag_engagement(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Analyze engagement by hashtag.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, float]: Hashtag engagement analysis
        """
        try:
            if 'hashtags' not in df.columns or 'total_engagement' not in df.columns:
                return {}
            
            hashtag_engagement = {}
            for hashtag in df['hashtags'].explode().unique():
                hashtag_tweets = df[df['hashtags'].apply(lambda x: hashtag in x if isinstance(x, list) else False)]
                hashtag_engagement[hashtag] = hashtag_tweets['total_engagement'].mean()
            
            return dict(sorted(hashtag_engagement.items(), key=lambda x: x[1], reverse=True)[:10])
            
        except Exception:
            return {}
    
    def _analyze_mention_engagement(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Analyze engagement by mention.
        
        Args:
            df (pd.DataFrame): Twitter data
            
        Returns:
            Dict[str, float]: Mention engagement analysis
        """
        try:
            if 'mentions' not in df.columns or 'total_engagement' not in df.columns:
                return {}
            
            mention_engagement = {}
            for mention in df['mentions'].explode().unique():
                mention_tweets = df[df['mentions'].apply(lambda x: mention in x if isinstance(x, list) else False)]
                mention_engagement[mention] = mention_tweets['total_engagement'].mean()
            
            return dict(sorted(mention_engagement.items(), key=lambda x: x[1], reverse=True)[:10])
            
        except Exception:
            return {} 