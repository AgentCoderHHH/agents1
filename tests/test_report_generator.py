"""
Unit tests for the ReportGeneratorAgent.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import json
from pathlib import Path

from agents.presentation import ReportGeneratorAgent
from tests.config import (
    setup_test_environment,
    cleanup_test_environment,
    MOCK_WEBSITE_DATA,
    MOCK_TWITTER_DATA,
    MOCK_ANALYTICS_DATA,
    TEST_DATA_DIR
)

class TestReportGeneratorAgent(unittest.TestCase):
    """Test cases for the ReportGeneratorAgent."""
    
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
        self.agent = ReportGeneratorAgent()
        self.website_df = pd.DataFrame(MOCK_WEBSITE_DATA)
        self.twitter_df = pd.DataFrame(MOCK_TWITTER_DATA)
        self.analytics_df = pd.DataFrame(MOCK_ANALYTICS_DATA)
    
    def test_generate_website_report(self):
        """Test generating website report."""
        # Test JSON format
        json_report = self.agent.generate_website_report(
            self.website_df,
            report_type="daily",
            output_format="json"
        )
        
        self.assertIsInstance(json_report, dict)
        self.assertIn('performance', json_report)
        self.assertIn('user_behavior', json_report)
        self.assertIn('traffic_sources', json_report)
        
        # Test HTML format
        html_report = self.agent.generate_website_report(
            self.website_df,
            report_type="daily",
            output_format="html"
        )
        
        self.assertIsInstance(html_report, str)
        self.assertIn('<!DOCTYPE html>', html_report)
        self.assertIn('Website Performance Report', html_report)
    
    def test_generate_social_media_report(self):
        """Test generating social media report."""
        # Test JSON format
        json_report = self.agent.generate_social_media_report(
            self.twitter_df,
            report_type="daily",
            output_format="json"
        )
        
        self.assertIsInstance(json_report, dict)
        self.assertIn('performance', json_report)
        self.assertIn('engagement', json_report)
        self.assertIn('content', json_report)
        
        # Test HTML format
        html_report = self.agent.generate_social_media_report(
            self.twitter_df,
            report_type="daily",
            output_format="html"
        )
        
        self.assertIsInstance(html_report, str)
        self.assertIn('<!DOCTYPE html>', html_report)
        self.assertIn('Social Media Performance Report', html_report)
    
    def test_generate_comparative_report(self):
        """Test generating comparative report."""
        # Test JSON format
        json_report = self.agent.generate_comparative_report(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            report_type="daily",
            output_format="json"
        )
        
        self.assertIsInstance(json_report, dict)
        self.assertIn('metrics_comparison', json_report)
        self.assertIn('trend_comparison', json_report)
        self.assertIn('correlation_analysis', json_report)
        
        # Test HTML format
        html_report = self.agent.generate_comparative_report(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            report_type="daily",
            output_format="html"
        )
        
        self.assertIsInstance(html_report, str)
        self.assertIn('<!DOCTYPE html>', html_report)
        self.assertIn('Comparative Performance Report', html_report)
    
    def test_generate_comprehensive_report(self):
        """Test generating comprehensive report."""
        # Test JSON format
        json_report = self.agent.generate_comprehensive_report(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            report_type="daily",
            output_format="json"
        )
        
        self.assertIsInstance(json_report, dict)
        self.assertIn('website_analysis', json_report)
        self.assertIn('social_media_analysis', json_report)
        self.assertIn('comparative_analysis', json_report)
        self.assertIn('insights', json_report)
        
        # Test HTML format
        html_report = self.agent.generate_comprehensive_report(
            self.website_df,
            self.analytics_df,
            self.twitter_df,
            report_type="daily",
            output_format="html"
        )
        
        self.assertIsInstance(html_report, str)
        self.assertIn('<!DOCTYPE html>', html_report)
        self.assertIn('Comprehensive Performance Report', html_report)
    
    def test_save_report(self):
        """Test saving reports to file."""
        # Test saving JSON report
        json_report = self.agent.generate_website_report(
            self.website_df,
            report_type="daily",
            output_format="json"
        )
        
        json_path = TEST_DATA_DIR / "website_report.json"
        self.agent._save_report(json_report, json_path)
        
        self.assertTrue(json_path.exists())
        with open(json_path, 'r') as f:
            saved_json = json.load(f)
        self.assertEqual(saved_json, json_report)
        
        # Test saving HTML report
        html_report = self.agent.generate_website_report(
            self.website_df,
            report_type="daily",
            output_format="html"
        )
        
        html_path = TEST_DATA_DIR / "website_report.html"
        self.agent._save_report(html_report, html_path)
        
        self.assertTrue(html_path.exists())
        with open(html_path, 'r') as f:
            saved_html = f.read()
        self.assertEqual(saved_html, html_report)
    
    def test_generate_html_report(self):
        """Test generating HTML report."""
        analysis = {
            'performance': {'visitors': 1000, 'pageviews': 2000},
            'user_behavior': {'bounce_rate': 0.45, 'session_duration': 180},
            'traffic_sources': {'organic': 0.6, 'direct': 0.4}
        }
        
        html_report = self.agent._generate_html_report(
            analysis,
            "Website Performance Report",
            "daily"
        )
        
        self.assertIsInstance(html_report, str)
        self.assertIn('<!DOCTYPE html>', html_report)
        self.assertIn('Website Performance Report', html_report)
        self.assertIn('1000', html_report)
        self.assertIn('2000', html_report)
    
    def test_generate_insights(self):
        """Test generating insights from analysis."""
        analysis = {
            'performance': {'visitors': 1000, 'pageviews': 2000},
            'user_behavior': {'bounce_rate': 0.45, 'session_duration': 180},
            'traffic_sources': {'organic': 0.6, 'direct': 0.4}
        }
        
        insights = self.agent._generate_insights(analysis)
        
        self.assertIsInstance(insights, list)
        self.assertTrue(len(insights) > 0)
        for insight in insights:
            self.assertIsInstance(insight, str)
            self.assertTrue(len(insight) > 0)

if __name__ == '__main__':
    unittest.main() 