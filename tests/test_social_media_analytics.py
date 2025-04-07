"""
Unit tests for the SocialMediaAnalyticsAgent.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

from agents.analytics import SocialMediaAnalyticsAgent
from tests.config import (
    setup_test_environment,
    cleanup_test_environment,
    MOCK_TWITTER_DATA
)

class TestSocialMediaAnalyticsAgent(unittest.TestCase):
    """Test cases for the SocialMediaAnalyticsAgent."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        setup_test_environment()
    
    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment."""
        cleanup_test_environment()
    
    def setUp(self):
        """Set up each test case."""
        self.agent = SocialMediaAnalyticsAgent()
        self.twitter_df = pd.DataFrame(MOCK_TWITTER_DATA)
    
    def test_analyze_twitter_performance(self):
        """Test analyzing Twitter performance."""
        analysis = self.agent.analyze_twitter_performance(self.twitter_df)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('engagement_growth', analysis)
        self.assertIn('reach_growth', analysis)
        self.assertIn('engagement_trend', analysis)
        self.assertIn('seasonal_patterns', analysis)
        self.assertIn('correlation_analysis', analysis)
    
    def test_analyze_engagement(self):
        """Test analyzing engagement patterns."""
        analysis = self.agent.analyze_engagement(self.twitter_df)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('total_engagement', analysis)
        self.assertIn('average_engagement', analysis)
        self.assertIn('engagement_rate', analysis)
        self.assertIn('engagement_trends', analysis)
        self.assertIn('audience_engagement', analysis)
    
    def test_analyze_content_performance(self):
        """Test analyzing content performance."""
        analysis = self.agent.analyze_content_performance(self.twitter_df)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('content_types', analysis)
        self.assertIn('best_performing', analysis)
        self.assertIn('content_trends', analysis)
        self.assertIn('optimal_times', analysis)
        self.assertIn('content_insights', analysis)
    
    def test_analyze_growth(self):
        """Test analyzing growth metrics."""
        # Test engagement growth
        engagement_growth = self.agent._analyze_growth(
            self.twitter_df,
            'engagement'
        )
        
        self.assertIsInstance(engagement_growth, dict)
        self.assertIn('growth_rate', engagement_growth)
        self.assertIn('cagr', engagement_growth)
        self.assertIn('trend', engagement_growth)
        
        # Test reach growth
        reach_growth = self.agent._analyze_growth(
            self.twitter_df,
            'reach'
        )
        
        self.assertIsInstance(reach_growth, dict)
        self.assertIn('growth_rate', reach_growth)
        self.assertIn('cagr', reach_growth)
        self.assertIn('trend', reach_growth)
    
    def test_analyze_trend(self):
        """Test analyzing trends."""
        # Test engagement trend
        engagement_trend = self.agent._analyze_trend(
            self.twitter_df,
            'engagement'
        )
        
        self.assertIsInstance(engagement_trend, dict)
        self.assertIn('slope', engagement_trend)
        self.assertIn('intercept', engagement_trend)
        self.assertIn('r_value', engagement_trend)
        self.assertIn('p_value', engagement_trend)
        
        # Test reach trend
        reach_trend = self.agent._analyze_trend(
            self.twitter_df,
            'reach'
        )
        
        self.assertIsInstance(reach_trend, dict)
        self.assertIn('slope', reach_trend)
        self.assertIn('intercept', reach_trend)
        self.assertIn('r_value', reach_trend)
        self.assertIn('p_value', reach_trend)
    
    def test_analyze_seasonality(self):
        """Test analyzing seasonality."""
        # Test daily patterns
        daily_patterns = self.agent._analyze_seasonality(
            self.twitter_df,
            'engagement'
        )
        
        self.assertIsInstance(daily_patterns, dict)
        self.assertIn('daily', daily_patterns)
        self.assertIn('weekly', daily_patterns)
        self.assertIn('monthly', daily_patterns)
        
        # Test weekly patterns
        weekly_patterns = self.agent._analyze_seasonality(
            self.twitter_df,
            'reach'
        )
        
        self.assertIsInstance(weekly_patterns, dict)
        self.assertIn('daily', weekly_patterns)
        self.assertIn('weekly', weekly_patterns)
        self.assertIn('monthly', weekly_patterns)
    
    def test_analyze_correlations(self):
        """Test analyzing correlations."""
        metrics = ['engagement', 'reach', 'retweet_count', 'favorite_count']
        correlations = self.agent._analyze_correlations(
            self.twitter_df,
            metrics
        )
        
        self.assertIsInstance(correlations, dict)
        self.assertIn('correlation_matrix', correlations)
        self.assertIn('strong_correlations', correlations)
        
        # Check correlation matrix
        matrix = correlations['correlation_matrix']
        self.assertIsInstance(matrix, pd.DataFrame)
        self.assertEqual(matrix.shape, (len(metrics), len(metrics)))
        
        # Check strong correlations
        strong_corrs = correlations['strong_correlations']
        self.assertIsInstance(strong_corrs, list)
        for corr in strong_corrs:
            self.assertIsInstance(corr, dict)
            self.assertIn('metric1', corr)
            self.assertIn('metric2', corr)
            self.assertIn('correlation', corr)
    
    def test_analyze_content_characteristics(self):
        """Test analyzing content characteristics."""
        characteristics = self.agent._analyze_content_characteristics(
            self.twitter_df
        )
        
        self.assertIsInstance(characteristics, dict)
        self.assertIn('content_types', characteristics)
        self.assertIn('content_length', characteristics)
        self.assertIn('hashtag_usage', characteristics)
        self.assertIn('mention_usage', characteristics)
        self.assertIn('link_usage', characteristics)
    
    def test_analyze_audience_characteristics(self):
        """Test analyzing audience characteristics."""
        characteristics = self.agent._analyze_audience_characteristics(
            self.twitter_df
        )
        
        self.assertIsInstance(characteristics, dict)
        self.assertIn('follower_growth', characteristics)
        self.assertIn('audience_engagement', characteristics)
        self.assertIn('audience_demographics', characteristics)
        self.assertIn('audience_interests', characteristics)
        self.assertIn('audience_behavior', characteristics)

if __name__ == '__main__':
    unittest.main() 