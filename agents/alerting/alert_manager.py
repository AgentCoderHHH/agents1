"""
Alert Manager Agent for monitoring and sending notifications.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
from datetime import datetime
import requests
import json
from pathlib import Path

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config

class AlertManagerAgent:
    """Agent responsible for managing alerts and notifications."""
    
    def __init__(self):
        """Initialize the Alert Manager Agent."""
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
        self.config = Config()
        
        # Load alert configurations
        self.alert_configs = self._load_alert_configs()
        
        # Initialize notification channels
        self.notification_channels = {
            'telegram': self._send_telegram_notification,
            'email': self._send_email_notification,
            'slack': self._send_slack_notification
        }
    
    def monitor_metrics(
        self,
        metrics: Dict[str, Any],
        source: str,
        alert_type: str = "threshold"
    ) -> List[Dict[str, Any]]:
        """
        Monitor metrics and generate alerts if thresholds are exceeded.
        
        Args:
            metrics (Dict[str, Any]): Metrics to monitor
            source (str): Source of the metrics (website, twitter, etc.)
            alert_type (str): Type of alert (threshold, anomaly, etc.)
            
        Returns:
            List[Dict[str, Any]]: List of generated alerts
        """
        try:
            # Start monitoring
            self.monitoring.start_monitoring("alert_monitoring")
            
            alerts = []
            
            # Check each metric against its threshold
            for metric_name, value in metrics.items():
                if metric_name in self.alert_configs[source]:
                    config = self.alert_configs[source][metric_name]
                    
                    # Check threshold
                    if alert_type == "threshold":
                        if value > config.get('max_threshold', float('inf')):
                            alerts.append(self._create_alert(
                                source,
                                metric_name,
                                "high",
                                value,
                                config['max_threshold']
                            ))
                        elif value < config.get('min_threshold', float('-inf')):
                            alerts.append(self._create_alert(
                                source,
                                metric_name,
                                "low",
                                value,
                                config['min_threshold']
                            ))
                    
                    # Check for anomalies
                    elif alert_type == "anomaly":
                        if self._detect_anomaly(value, config.get('history', [])):
                            alerts.append(self._create_alert(
                                source,
                                metric_name,
                                "anomaly",
                                value,
                                None
                            ))
            
            # Send notifications for alerts
            for alert in alerts:
                self.send_notification(alert)
            
            # Log monitoring results
            self.monitoring.log_metric(
                "alerts_generated",
                len(alerts),
                {"source": source, "alert_type": alert_type}
            )
            
            return alerts
            
        except Exception as e:
            self.error_handler.handle_error(
                "AlertMonitoringError",
                f"Failed to monitor metrics: {str(e)}"
            )
            return []
            
        finally:
            self.monitoring.stop_monitoring("alert_monitoring")
    
    def send_notification(
        self,
        alert: Dict[str, Any],
        channels: Optional[List[str]] = None
    ) -> bool:
        """
        Send notification for an alert through specified channels.
        
        Args:
            alert (Dict[str, Any]): Alert to send
            channels (Optional[List[str]]): Channels to send through
            
        Returns:
            bool: True if notification was sent successfully
        """
        try:
            # Start monitoring
            self.monitoring.start_monitoring("notification_sending")
            
            # Use default channels if none specified
            if channels is None:
                channels = self.config.get('default_notification_channels', ['telegram'])
            
            success = True
            
            # Send through each channel
            for channel in channels:
                if channel in self.notification_channels:
                    try:
                        self.notification_channels[channel](alert)
                    except Exception as e:
                        self.error_handler.handle_error(
                            "NotificationError",
                            f"Failed to send {channel} notification: {str(e)}"
                        )
                        success = False
            
            # Log notification results
            self.monitoring.log_metric(
                "notifications_sent",
                1,
                {"channels": channels, "alert_type": alert['type']}
            )
            
            return success
            
        except Exception as e:
            self.error_handler.handle_error(
                "NotificationError",
                f"Failed to send notification: {str(e)}"
            )
            return False
            
        finally:
            self.monitoring.stop_monitoring("notification_sending")
    
    def _load_alert_configs(self) -> Dict[str, Dict[str, Dict[str, Any]]]:
        """
        Load alert configurations from file.
        
        Returns:
            Dict[str, Dict[str, Dict[str, Any]]]: Alert configurations
        """
        try:
            config_path = Path(self.config.BASE_DIR) / "config" / "alert_configs.json"
            
            if config_path.exists():
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                # Return default configurations
                return {
                    'website': {
                        'visitors': {
                            'max_threshold': 10000,
                            'min_threshold': 1000
                        },
                        'bounce_rate': {
                            'max_threshold': 0.7,
                            'min_threshold': 0.1
                        }
                    },
                    'twitter': {
                        'engagement_rate': {
                            'max_threshold': 0.1,
                            'min_threshold': 0.01
                        },
                        'reach': {
                            'max_threshold': 100000,
                            'min_threshold': 1000
                        }
                    }
                }
                
        except Exception as e:
            self.error_handler.handle_error(
                "ConfigLoadError",
                f"Failed to load alert configurations: {str(e)}"
            )
            return {}
    
    def _create_alert(
        self,
        source: str,
        metric: str,
        alert_type: str,
        current_value: float,
        threshold: Optional[float]
    ) -> Dict[str, Any]:
        """
        Create an alert object.
        
        Args:
            source (str): Source of the alert
            metric (str): Metric that triggered the alert
            alert_type (str): Type of alert
            current_value (float): Current value of the metric
            threshold (Optional[float]): Threshold value
            
        Returns:
            Dict[str, Any]: Alert object
        """
        return {
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'metric': metric,
            'type': alert_type,
            'current_value': current_value,
            'threshold': threshold,
            'message': self._generate_alert_message(
                source,
                metric,
                alert_type,
                current_value,
                threshold
            )
        }
    
    def _generate_alert_message(
        self,
        source: str,
        metric: str,
        alert_type: str,
        current_value: float,
        threshold: Optional[float]
    ) -> str:
        """
        Generate alert message.
        
        Args:
            source (str): Source of the alert
            metric (str): Metric that triggered the alert
            alert_type (str): Type of alert
            current_value (float): Current value of the metric
            threshold (Optional[float]): Threshold value
            
        Returns:
            str: Alert message
        """
        if alert_type == "anomaly":
            return f"Anomaly detected in {source} {metric}: {current_value}"
        else:
            direction = "above" if alert_type == "high" else "below"
            return f"{source} {metric} is {direction} threshold: {current_value} (threshold: {threshold})"
    
    def _detect_anomaly(
        self,
        value: float,
        history: List[float],
        threshold: float = 2.0
    ) -> bool:
        """
        Detect if a value is an anomaly based on historical data.
        
        Args:
            value (float): Current value
            history (List[float]): Historical values
            threshold (float): Standard deviation threshold
            
        Returns:
            bool: True if value is an anomaly
        """
        if not history:
            return False
            
        mean = sum(history) / len(history)
        std = (sum((x - mean) ** 2 for x in history) / len(history)) ** 0.5
        
        return abs(value - mean) > threshold * std
    
    def _send_telegram_notification(self, alert: Dict[str, Any]) -> None:
        """Send notification through Telegram."""
        try:
            bot_token = self.config.get('telegram_bot_token')
            chat_id = self.config.get('telegram_chat_id')
            
            if bot_token and chat_id:
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                data = {
                    'chat_id': chat_id,
                    'text': alert['message'],
                    'parse_mode': 'HTML'
                }
                
                response = requests.post(url, json=data)
                response.raise_for_status()
                
        except Exception as e:
            raise Exception(f"Failed to send Telegram notification: {str(e)}")
    
    def _send_email_notification(self, alert: Dict[str, Any]) -> None:
        """Send notification through email."""
        # TODO: Implement email notification
        pass
    
    def _send_slack_notification(self, alert: Dict[str, Any]) -> None:
        """Send notification through Slack."""
        try:
            webhook_url = self.config.get('slack_webhook_url')
            
            if webhook_url:
                data = {
                    'text': alert['message']
                }
                
                response = requests.post(webhook_url, json=data)
                response.raise_for_status()
                
        except Exception as e:
            raise Exception(f"Failed to send Slack notification: {str(e)}") 