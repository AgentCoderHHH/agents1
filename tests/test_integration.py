"""
Integration tests for testing agents working together.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from agents.analytics import (
    WebsiteAnalyticsAgent,
    SocialMediaAnalyticsAgent,
    ComparativeAnalyticsAgent
)
from agents.presentation import ReportGeneratorAgent
from agents.alerting import AlertManagerAgent
from tests.config import (
    setup_test_environment,
    cleanup_test_environment,
    MOCK_WEBSITE_DATA,
    MOCK_ANALYTICS_DATA,
    MOCK_TWITTER_DATA
)

class TestAgentIntegration(unittest.TestCase):
    """Integration tests for testing agents working together."""
    
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
        # Initialize all agents
        self.website_agent = WebsiteAnalyticsAgent()
        self.social_media_agent = SocialMediaAnalyticsAgent()
        self.comparative_agent = ComparativeAnalyticsAgent()
        self.report_agent = ReportGeneratorAgent()
        self.alert_agent = AlertManagerAgent()
        
        # Create test data
        self.website_df = pd.DataFrame(MOCK_WEBSITE_DATA)
        self.analytics_df = pd.DataFrame(MOCK_ANALYTICS_DATA)
        self.twitter_df = pd.DataFrame(MOCK_TWITTER_DATA)
    
    def test_website_analytics_pipeline(self):
        """Test the website analytics pipeline."""
        # Analyze website performance
        performance = self.website_agent.analyze_performance(self.website_df)
        self.assertIsInstance(performance, dict)
        
        # Analyze user behavior
        behavior = self.website_agent.analyze_user_behavior(self.website_df)
        self.assertIsInstance(behavior, dict)
        
        # Analyze traffic sources
        traffic = self.website_agent.analyze_traffic_sources(self.website_df)
        self.assertIsInstance(traffic, dict)
        
        # Generate report
        report = self.report_agent.generate_website_report(
            self.website_df,
            report_type='performance',
            output_format='html'
        )
        self.assertIsInstance(report, dict)
        self.assertIn('report_content', report)
    
    def test_social_media_analytics_pipeline(self):
        """Test the social media analytics pipeline."""
        # Analyze Twitter performance
        performance = self.social_media_agent.analyze_twitter_performance(self.twitter_df)
        self.assertIsInstance(performance, dict)
        
        # Analyze engagement
        engagement = self.social_media_agent.analyze_engagement(self.twitter_df)
        self.assertIsInstance(engagement, dict)
        
        # Analyze content performance
        content = self.social_media_agent.analyze_content_performance(self.twitter_df)
        self.assertIsInstance(content, dict)
        
        # Generate report
        report = self.report_agent.generate_social_media_report(
            self.twitter_df,
            report_type='performance',
            output_format='html'
        )
        self.assertIsInstance(report, dict)
        self.assertIn('report_content', report)
    
    def test_comparative_analytics_pipeline(self):
        """Test the comparative analytics pipeline."""
        # Compare performance
        comparison = self.comparative_agent.compare_performance(
            self.website_df,
            self.analytics_df,
            self.twitter_df
        )
        self.assertIsInstance(comparison, dict)
        
        # Analyze cross-channel impact
        impact = self.comparative_agent.analyze_cross_channel_impact(
            self.website_df,
            self.analytics_df,
            self.twitter_df
        )
        self.assertIsInstance(impact, dict)
        
        # Generate report
        report = self.report_agent.generate_comparative_report(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            report_type='performance',
            output_format='html'
        )
        self.assertIsInstance(report, dict)
        self.assertIn('report_content', report)
    
    def test_comprehensive_analytics_pipeline(self):
        """Test the comprehensive analytics pipeline."""
        # Generate comprehensive report
        report = self.report_agent.generate_comprehensive_report(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            output_format='html'
        )
        self.assertIsInstance(report, dict)
        self.assertIn('report_content', report)
    
    @patch('agents.alerting.AlertManagerAgent.send_notification')
    def test_alerting_pipeline(self, mock_send_notification):
        """Test the alerting pipeline."""
        # Configure mock
        mock_send_notification.return_value = True
        
        # Monitor metrics
        alerts = self.alert_agent.monitor_metrics(
            {
                'website': {'visitors': 12000, 'bounce_rate': 0.65},
                'twitter': {'engagement_rate': 0.15, 'reach': 5000}
            },
            alert_type='threshold'
        )
        
        self.assertIsInstance(alerts, list)
        mock_send_notification.assert_called()
    
    def test_end_to_end_pipeline(self):
        """Test the complete end-to-end pipeline."""
        # Website analysis
        website_performance = self.website_agent.analyze_performance(self.website_df)
        website_behavior = self.website_agent.analyze_user_behavior(self.website_df)
        website_traffic = self.website_agent.analyze_traffic_sources(self.website_df)
        
        # Social media analysis
        twitter_performance = self.social_media_agent.analyze_twitter_performance(self.twitter_df)
        twitter_engagement = self.social_media_agent.analyze_engagement(self.twitter_df)
        twitter_content = self.social_media_agent.analyze_content_performance(self.twitter_df)
        
        # Comparative analysis
        comparison = self.comparative_agent.compare_performance(
            self.website_df,
            self.analytics_df,
            self.twitter_df
        )
        impact = self.comparative_agent.analyze_cross_channel_impact(
            self.website_df,
            self.analytics_df,
            self.twitter_df
        )
        
        # Generate comprehensive report
        report = self.report_agent.generate_comprehensive_report(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            output_format='html'
        )
        
        # Monitor metrics and send alerts
        alerts = self.alert_agent.monitor_metrics(
            {
                'website': {
                    'visitors': website_performance['visitor_growth']['current_value'],
                    'bounce_rate': website_performance['bounce_rate_trend']['current_value']
                },
                'twitter': {
                    'engagement_rate': twitter_performance['engagement_growth']['current_value'],
                    'reach': twitter_performance['reach_growth']['current_value']
                }
            },
            alert_type='threshold'
        )
        
        # Verify results
        self.assertIsInstance(website_performance, dict)
        self.assertIsInstance(website_behavior, dict)
        self.assertIsInstance(website_traffic, dict)
        self.assertIsInstance(twitter_performance, dict)
        self.assertIsInstance(twitter_engagement, dict)
        self.assertIsInstance(twitter_content, dict)
        self.assertIsInstance(comparison, dict)
        self.assertIsInstance(impact, dict)
        self.assertIsInstance(report, dict)
        self.assertIsInstance(alerts, list)

if __name__ == '__main__':
    unittest.main() 