"""
Unit tests for the AlertManagerAgent.
"""

import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime

from agents.alerting import AlertManagerAgent
from tests.config import (
    setup_test_environment,
    cleanup_test_environment,
    MOCK_WEBSITE_DATA,
    MOCK_TWITTER_DATA,
    MOCK_ALERT_CONFIGS
)

class TestAlertManagerAgent(unittest.TestCase):
    """Test cases for the AlertManagerAgent."""
    
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
        self.agent = AlertManagerAgent()
    
    def test_monitor_metrics_threshold(self):
        """Test monitoring metrics with threshold alerts."""
        # Test website metrics
        website_alerts = self.agent.monitor_metrics(
            {'visitors': 12000, 'bounce_rate': 0.65},
            source="website",
            alert_type="threshold"
        )
        
        self.assertEqual(len(website_alerts), 2)
        self.assertEqual(website_alerts[0]['type'], 'high')
        self.assertEqual(website_alerts[1]['type'], 'low')
        
        # Test Twitter metrics
        twitter_alerts = self.agent.monitor_metrics(
            {'engagement_rate': 0.15, 'reach': 5000},
            source="twitter",
            alert_type="threshold"
        )
        
        self.assertEqual(len(twitter_alerts), 2)
        self.assertEqual(twitter_alerts[0]['type'], 'high')
        self.assertEqual(twitter_alerts[1]['type'], 'low')
    
    def test_monitor_metrics_anomaly(self):
        """Test monitoring metrics with anomaly detection."""
        # Test with historical data
        history = [0.05, 0.06, 0.07, 0.08, 0.09]
        alerts = self.agent.monitor_metrics(
            {'engagement_rate': 0.15},
            source="twitter",
            alert_type="anomaly"
        )
        
        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]['type'], 'anomaly')
    
    @patch('requests.post')
    def test_send_notification(self, mock_post):
        """Test sending notifications."""
        # Configure mock response
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Test sending notification
        alert = {
            'timestamp': datetime.now().isoformat(),
            'source': 'website',
            'metric': 'visitors',
            'type': 'high',
            'current_value': 12000,
            'threshold': 10000,
            'message': 'Test alert message'
        }
        
        success = self.agent.send_notification(
            alert,
            channels=['telegram', 'slack']
        )
        
        self.assertTrue(success)
        self.assertEqual(mock_post.call_count, 2)
    
    def test_load_alert_configs(self):
        """Test loading alert configurations."""
        configs = self.agent._load_alert_configs()
        
        self.assertIn('website', configs)
        self.assertIn('twitter', configs)
        self.assertEqual(
            configs['website']['visitors']['max_threshold'],
            MOCK_ALERT_CONFIGS['website']['visitors']['max_threshold']
        )
    
    def test_create_alert(self):
        """Test creating an alert object."""
        alert = self.agent._create_alert(
            source="website",
            metric="visitors",
            alert_type="high",
            current_value=12000,
            threshold=10000
        )
        
        self.assertEqual(alert['source'], 'website')
        self.assertEqual(alert['metric'], 'visitors')
        self.assertEqual(alert['type'], 'high')
        self.assertEqual(alert['current_value'], 12000)
        self.assertEqual(alert['threshold'], 10000)
        self.assertIn('timestamp', alert)
        self.assertIn('message', alert)
    
    def test_generate_alert_message(self):
        """Test generating alert messages."""
        # Test threshold message
        threshold_message = self.agent._generate_alert_message(
            source="website",
            metric="visitors",
            alert_type="high",
            current_value=12000,
            threshold=10000
        )
        
        self.assertIn('above threshold', threshold_message)
        self.assertIn('12000', threshold_message)
        self.assertIn('10000', threshold_message)
        
        # Test anomaly message
        anomaly_message = self.agent._generate_alert_message(
            source="twitter",
            metric="engagement_rate",
            alert_type="anomaly",
            current_value=0.15,
            threshold=None
        )
        
        self.assertIn('Anomaly detected', anomaly_message)
        self.assertIn('0.15', anomaly_message)
    
    def test_detect_anomaly(self):
        """Test anomaly detection."""
        # Test with normal value
        history = [0.05, 0.06, 0.07, 0.08, 0.09]
        is_anomaly = self.agent._detect_anomaly(0.07, history)
        self.assertFalse(is_anomaly)
        
        # Test with anomalous value
        is_anomaly = self.agent._detect_anomaly(0.15, history)
        self.assertTrue(is_anomaly)
        
        # Test with empty history
        is_anomaly = self.agent._detect_anomaly(0.15, [])
        self.assertFalse(is_anomaly)

if __name__ == '__main__':
    unittest.main() 