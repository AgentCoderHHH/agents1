# Report Generator Agent Examples

This document provides examples of how to use the ReportGeneratorAgent in the AgentOpenApi system.

## 1. Basic Website Report Example

```python
from agents.presentation import ReportGeneratorAgent
import pandas as pd

# Initialize the agent
report_generator = ReportGeneratorAgent()

# Example website data
website_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02'],
    'Visitors': [1000, 1200],
    'Pageviews': [2000, 2400],
    'BounceRate': [0.45, 0.42],
    'SessionDuration': [180, 190]
})

# Generate website report
report = report_generator.generate_website_report(
    website_data,
    report_type="daily",
    output_format="json"
)
print("Website Report:", report)
```

## 2. Social Media Report Example

```python
from agents.presentation import ReportGeneratorAgent
import pandas as pd

# Initialize the agent
report_generator = ReportGeneratorAgent()

# Example Twitter data
twitter_data = pd.DataFrame({
    'created_at': ['2024-01-01', '2024-01-02'],
    'text': ['Sample tweet 1', 'Sample tweet 2'],
    'retweet_count': [100, 150],
    'favorite_count': [200, 250],
    'reply_count': [50, 60]
})

# Generate social media report
report = report_generator.generate_social_media_report(
    twitter_data,
    report_type="daily",
    output_format="html"
)
print("Social Media Report:", report)
```

## 3. Comparative Report Example

```python
from agents.presentation import ReportGeneratorAgent
import pandas as pd

# Initialize the agent
report_generator = ReportGeneratorAgent()

# Example data from different sources
website_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02'],
    'Visitors': [1000, 1200],
    'Pageviews': [2000, 2400]
})

analytics_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02'],
    'Users': [950, 1150],
    'Sessions': [1800, 2200]
})

twitter_data = pd.DataFrame({
    'created_at': ['2024-01-01', '2024-01-02'],
    'engagement': [350, 400],
    'reach': [5000, 6000]
})

# Generate comparative report
report = report_generator.generate_comparative_report(
    website_data,
    analytics_data,
    twitter_data,
    report_type="daily",
    output_format="json"
)
print("Comparative Report:", report)
```

## 4. Comprehensive Report Example

```python
from agents.presentation import ReportGeneratorAgent
import pandas as pd

# Initialize the agent
report_generator = ReportGeneratorAgent()

# Example data from different sources
website_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02'],
    'Visitors': [1000, 1200],
    'Pageviews': [2000, 2400]
})

analytics_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02'],
    'Users': [950, 1150],
    'Sessions': [1800, 2200]
})

twitter_data = pd.DataFrame({
    'created_at': ['2024-01-01', '2024-01-02'],
    'engagement': [350, 400],
    'reach': [5000, 6000]
})

# Generate comprehensive report
report = report_generator.generate_comprehensive_report(
    website_data,
    analytics_data,
    twitter_data,
    report_type="daily",
    output_format="html"
)
print("Comprehensive Report:", report)
```

## 5. Error Handling Example

```python
from agents.presentation import ReportGeneratorAgent
from agents.error_handler import ErrorHandler
import pandas as pd

# Initialize agents
report_generator = ReportGeneratorAgent()
error_handler = ErrorHandler()

try:
    # Attempt to generate report with invalid data
    invalid_data = pd.DataFrame({
        'InvalidColumn': [1, 2, 3]
    })
    
    report = report_generator.generate_website_report(invalid_data)
    
except Exception as e:
    # Handle the error
    error_handler.handle_error(
        "ReportGenerationError",
        f"Failed to generate report: {str(e)}"
    )
```

## 6. Monitoring Example

```python
from agents.presentation import ReportGeneratorAgent
from agents.monitoring import MonitoringAgent
import pandas as pd

# Initialize agents
report_generator = ReportGeneratorAgent()
monitoring = MonitoringAgent()

# Example data
website_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02'],
    'Visitors': [1000, 1200],
    'Pageviews': [2000, 2400]
})

# Generate report with monitoring
def generate_report_with_monitoring():
    # Start monitoring
    monitoring.start_monitoring("report_generation")
    
    try:
        # Generate report
        report = report_generator.generate_website_report(website_data)
        
        # Log success
        monitoring.log_metric(
            "report_generated",
            1,
            {"visitor_count": len(website_data)}
        )
        
        return report
        
    except Exception as e:
        # Log error
        monitoring.log_error(
            "report_generation_failed",
            str(e),
            {"data_shape": website_data.shape}
        )
        raise
        
    finally:
        # Stop monitoring
        monitoring.stop_monitoring("report_generation")

# Execute monitored report generation
report = generate_report_with_monitoring()
print("Generated Report with Monitoring:", report)
``` 