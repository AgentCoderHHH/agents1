"""
Unit tests for the WebsiteAnalyticsAgent.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

from agents.analytics import WebsiteAnalyticsAgent
from tests.config import (
    setup_test_environment,
    cleanup_test_environment,
    MOCK_WEBSITE_DATA,
    MOCK_ANALYTICS_DATA
)

class TestWebsiteAnalyticsAgent(unittest.TestCase):
    """Test cases for the WebsiteAnalyticsAgent."""
    
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
        self.agent = WebsiteAnalyticsAgent()
        self.website_df = pd.DataFrame(MOCK_WEBSITE_DATA)
        self.analytics_df = pd.DataFrame(MOCK_ANALYTICS_DATA)
    
    def test_analyze_performance(self):
        """Test analyzing website performance."""
        analysis = self.agent.analyze_performance(self.website_df)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('visitor_growth', analysis)
        self.assertIn('pageview_growth', analysis)
        self.assertIn('bounce_rate_trend', analysis)
        self.assertIn('session_duration_trend', analysis)
        self.assertIn('seasonal_patterns', analysis)
        self.assertIn('correlation_analysis', analysis)
    
    def test_analyze_user_behavior(self):
        """Test analyzing user behavior."""
        analysis = self.agent.analyze_user_behavior(self.website_df)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('user_types', analysis)
        self.assertIn('session_distribution', analysis)
        self.assertIn('page_engagement', analysis)
        self.assertIn('user_flow', analysis)
        self.assertIn('conversion_analysis', analysis)
    
    def test_analyze_traffic_sources(self):
        """Test analyzing traffic sources."""
        analysis = self.agent.analyze_traffic_sources(self.website_df)
        
        self.assertIsInstance(analysis, dict)
        self.assertIn('source_distribution', analysis)
        self.assertIn('source_performance', analysis)
        self.assertIn('source_trends', analysis)
        self.assertIn('campaign_analysis', analysis)
        self.assertIn('referral_analysis', analysis)
    
    def test_analyze_growth(self):
        """Test analyzing growth metrics."""
        # Test visitor growth
        visitor_growth = self.agent._analyze_growth(
            self.website_df,
            'Visitors'
        )
        
        self.assertIsInstance(visitor_growth, dict)
        self.assertIn('growth_rate', visitor_growth)
        self.assertIn('cagr', visitor_growth)
        self.assertIn('trend', visitor_growth)
        
        # Test pageview growth
        pageview_growth = self.agent._analyze_growth(
            self.website_df,
            'Pageviews'
        )
        
        self.assertIsInstance(pageview_growth, dict)
        self.assertIn('growth_rate', pageview_growth)
        self.assertIn('cagr', pageview_growth)
        self.assertIn('trend', pageview_growth)
    
    def test_analyze_trend(self):
        """Test analyzing trends."""
        # Test bounce rate trend
        bounce_rate_trend = self.agent._analyze_trend(
            self.website_df,
            'BounceRate'
        )
        
        self.assertIsInstance(bounce_rate_trend, dict)
        self.assertIn('slope', bounce_rate_trend)
        self.assertIn('intercept', bounce_rate_trend)
        self.assertIn('r_value', bounce_rate_trend)
        self.assertIn('p_value', bounce_rate_trend)
        
        # Test session duration trend
        session_duration_trend = self.agent._analyze_trend(
            self.website_df,
            'SessionDuration'
        )
        
        self.assertIsInstance(session_duration_trend, dict)
        self.assertIn('slope', session_duration_trend)
        self.assertIn('intercept', session_duration_trend)
        self.assertIn('r_value', session_duration_trend)
        self.assertIn('p_value', session_duration_trend)
    
    def test_analyze_seasonality(self):
        """Test analyzing seasonality."""
        # Test daily patterns
        daily_patterns = self.agent._analyze_seasonality(
            self.website_df,
            'Visitors'
        )
        
        self.assertIsInstance(daily_patterns, dict)
        self.assertIn('daily', daily_patterns)
        self.assertIn('weekly', daily_patterns)
        self.assertIn('monthly', daily_patterns)
        
        # Test weekly patterns
        weekly_patterns = self.agent._analyze_seasonality(
            self.website_df,
            'Pageviews'
        )
        
        self.assertIsInstance(weekly_patterns, dict)
        self.assertIn('daily', weekly_patterns)
        self.assertIn('weekly', weekly_patterns)
        self.assertIn('monthly', weekly_patterns)
    
    def test_analyze_correlations(self):
        """Test analyzing correlations."""
        metrics = ['Visitors', 'Pageviews', 'BounceRate', 'SessionDuration']
        correlations = self.agent._analyze_correlations(
            self.website_df,
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

if __name__ == '__main__':
    unittest.main() 