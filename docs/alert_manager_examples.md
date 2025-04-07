# Alert Manager Agent Examples

This document provides examples of how to use the AlertManagerAgent in the AgentOpenApi system.

## 1. Basic Alert Monitoring Example

```python
from agents.alerting import AlertManagerAgent

# Initialize the agent
alert_manager = AlertManagerAgent()

# Example metrics to monitor
website_metrics = {
    'visitors': 12000,  # Above threshold
    'bounce_rate': 0.65  # Below threshold
}

# Monitor metrics
alerts = alert_manager.monitor_metrics(
    website_metrics,
    source="website",
    alert_type="threshold"
)
print("Generated Alerts:", alerts)
```

## 2. Anomaly Detection Example

```python
from agents.alerting import AlertManagerAgent

# Initialize the agent
alert_manager = AlertManagerAgent()

# Example metrics with historical data
twitter_metrics = {
    'engagement_rate': 0.15  # Anomaly if significantly different from history
}

# Monitor for anomalies
alerts = alert_manager.monitor_metrics(
    twitter_metrics,
    source="twitter",
    alert_type="anomaly"
)
print("Anomaly Alerts:", alerts)
```

## 3. Custom Notification Channels Example

```python
from agents.alerting import AlertManagerAgent

# Initialize the agent
alert_manager = AlertManagerAgent()

# Example alert
alert = {
    'timestamp': '2024-01-01T12:00:00',
    'source': 'website',
    'metric': 'visitors',
    'type': 'high',
    'current_value': 12000,
    'threshold': 10000,
    'message': 'Website visitors is above threshold: 12000 (threshold: 10000)'
}

# Send notification through specific channels
success = alert_manager.send_notification(
    alert,
    channels=['telegram', 'slack']
)
print("Notification Sent:", success)
```

## 4. Error Handling Example

```python
from agents.alerting import AlertManagerAgent
from agents.error_handler import ErrorHandler

# Initialize agents
alert_manager = AlertManagerAgent()
error_handler = ErrorHandler()

try:
    # Attempt to monitor invalid metrics
    invalid_metrics = {
        'invalid_metric': 'not_a_number'
    }
    
    alerts = alert_manager.monitor_metrics(invalid_metrics, "website")
    
except Exception as e:
    # Handle the error
    error_handler.handle_error(
        "AlertMonitoringError",
        f"Failed to monitor metrics: {str(e)}"
    )
```

## 5. Monitoring Example

```python
from agents.alerting import AlertManagerAgent
from agents.monitoring import MonitoringAgent

# Initialize agents
alert_manager = AlertManagerAgent()
monitoring = MonitoringAgent()

# Example metrics
metrics = {
    'visitors': 12000,
    'bounce_rate': 0.65
}

# Monitor with tracking
def monitor_with_tracking():
    # Start monitoring
    monitoring.start_monitoring("alert_monitoring")
    
    try:
        # Monitor metrics
        alerts = alert_manager.monitor_metrics(metrics, "website")
        
        # Log success
        monitoring.log_metric(
            "alerts_generated",
            len(alerts),
            {"source": "website"}
        )
        
        return alerts
        
    except Exception as e:
        # Log error
        monitoring.log_error(
            "monitoring_failed",
            str(e),
            {"metrics": list(metrics.keys())}
        )
        raise
        
    finally:
        # Stop monitoring
        monitoring.stop_monitoring("alert_monitoring")

# Execute monitored alerting
alerts = monitor_with_tracking()
print("Generated Alerts with Monitoring:", alerts)
```

## 6. Configuration Example

```python
from agents.alerting import AlertManagerAgent
import json
from pathlib import Path

# Initialize the agent
alert_manager = AlertManagerAgent()

# Example alert configurations
alert_configs = {
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
        }
    }
}

# Save configurations
config_path = Path("config") / "alert_configs.json"
config_path.parent.mkdir(exist_ok=True)

with open(config_path, 'w') as f:
    json.dump(alert_configs, f, indent=2)

print("Alert configurations saved to:", config_path)
``` 