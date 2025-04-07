"""
Unit tests for the ComparativeAnalyticsAgent.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

from agents.analytics import ComparativeAnalyticsAgent
from tests.config import (
    setup_test_environment,
    cleanup_test_environment,
    MOCK_WEBSITE_DATA,
    MOCK_ANALYTICS_DATA,
    MOCK_TWITTER_DATA
)

class TestComparativeAnalyticsAgent(unittest.TestCase):
    """Test cases for the ComparativeAnalyticsAgent."""
    
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
        self.agent = ComparativeAnalyticsAgent()
        self.website_df = pd.DataFrame(MOCK_WEBSITE_DATA)
        self.analytics_df = pd.DataFrame(MOCK_ANALYTICS_DATA)
        self.twitter_df = pd.DataFrame(MOCK_TWITTER_DATA)
    
    def test_compare_performance(self):
        """Test comparing performance across data sources."""
        comparison = self.agent.compare_performance(
            self.website_df,
            self.analytics_df,
            self.twitter_df
        )
        
        self.assertIsInstance(comparison, dict)
        self.assertIn('metrics_comparison', comparison)
        self.assertIn('trend_comparison', comparison)
        self.assertIn('correlation_analysis', comparison)
        self.assertIn('performance_insights', comparison)
    
    def test_analyze_cross_channel_impact(self):
        """Test analyzing cross-channel impact."""
        impact = self.agent.analyze_cross_channel_impact(
            self.website_df,
            self.analytics_df,
            self.twitter_df
        )
        
        self.assertIsInstance(impact, dict)
        self.assertIn('channel_impact', impact)
        self.assertIn('correlation_analysis', impact)
        self.assertIn('impact_insights', impact)
    
    def test_compare_metrics(self):
        """Test comparing metrics across channels."""
        metrics = ['engagement', 'reach', 'conversion_rate']
        comparison = self.agent._compare_metrics(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            metrics
        )
        
        self.assertIsInstance(comparison, dict)
        for metric in metrics:
            self.assertIn(metric, comparison)
            self.assertIsInstance(comparison[metric], dict)
            self.assertIn('website', comparison[metric])
            self.assertIn('analytics', comparison[metric])
            self.assertIn('twitter', comparison[metric])
    
    def test_compare_trends(self):
        """Test comparing trends across channels."""
        metrics = ['engagement', 'reach', 'conversion_rate']
        comparison = self.agent._compare_trends(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            metrics
        )
        
        self.assertIsInstance(comparison, dict)
        for metric in metrics:
            self.assertIn(metric, comparison)
            self.assertIsInstance(comparison[metric], dict)
            self.assertIn('website', comparison[metric])
            self.assertIn('analytics', comparison[metric])
            self.assertIn('twitter', comparison[metric])
    
    def test_analyze_correlations(self):
        """Test analyzing correlations between channels."""
        metrics = ['engagement', 'reach', 'conversion_rate']
        correlations = self.agent._analyze_correlations(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            metrics
        )
        
        self.assertIsInstance(correlations, dict)
        self.assertIn('correlation_matrix', correlations)
        self.assertIn('strong_correlations', correlations)
        
        # Check correlation matrix
        matrix = correlations['correlation_matrix']
        self.assertIsInstance(matrix, pd.DataFrame)
        self.assertEqual(matrix.shape, (len(metrics) * 3, len(metrics) * 3))
        
        # Check strong correlations
        strong_corrs = correlations['strong_correlations']
        self.assertIsInstance(strong_corrs, list)
        for corr in strong_corrs:
            self.assertIsInstance(corr, dict)
            self.assertIn('channel1', corr)
            self.assertIn('channel2', corr)
            self.assertIn('metric1', corr)
            self.assertIn('metric2', corr)
            self.assertIn('correlation', corr)
    
    def test_generate_insights(self):
        """Test generating insights from comparative analysis."""
        comparison = {
            'metrics_comparison': {},
            'trend_comparison': {},
            'correlation_analysis': {}
        }
        insights = self.agent._generate_insights(comparison)
        
        self.assertIsInstance(insights, dict)
        self.assertIn('key_findings', insights)
        self.assertIn('recommendations', insights)
        self.assertIn('opportunities', insights)
        self.assertIn('risks', insights)
    
    def test_determine_optimal_mix(self):
        """Test determining optimal channel mix."""
        comparison = {
            'metrics_comparison': {},
            'trend_comparison': {},
            'correlation_analysis': {}
        }
        optimal_mix = self.agent._determine_optimal_mix(comparison)
        
        self.assertIsInstance(optimal_mix, dict)
        self.assertIn('channel_mix', optimal_mix)
        self.assertIn('allocation_recommendations', optimal_mix)
        self.assertIn('expected_impact', optimal_mix)

if __name__ == '__main__':
    unittest.main() 