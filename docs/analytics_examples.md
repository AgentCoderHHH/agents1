# Analytics Agents Examples

This document provides examples of how to use the analytics agents in the AgentOpenApi system.

## 1. Website Analytics Example

```python
from agents.analytics import WebsiteAnalyticsAgent

# Initialize the agent
website_analytics = WebsiteAnalyticsAgent()

# Example website data
website_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02'],
    'Visitors': [1000, 1200],
    'Pageviews': [2000, 2400],
    'BounceRate': [0.45, 0.42],
    'SessionDuration': [180, 190]
})

# Analyze website performance
performance_analysis = website_analytics.analyze_performance(website_data)
print("Performance Analysis:", performance_analysis)

# Analyze user behavior
behavior_analysis = website_analytics.analyze_user_behavior(website_data)
print("User Behavior Analysis:", behavior_analysis)

# Analyze traffic sources
traffic_analysis = website_analytics.analyze_traffic_sources(website_data)
print("Traffic Analysis:", traffic_analysis)
```

## 2. Social Media Analytics Example

```python
from agents.analytics import SocialMediaAnalyticsAgent

# Initialize the agent
social_analytics = SocialMediaAnalyticsAgent()

# Example Twitter data
twitter_data = pd.DataFrame({
    'created_at': ['2024-01-01', '2024-01-02'],
    'text': ['Sample tweet 1', 'Sample tweet 2'],
    'retweet_count': [100, 150],
    'favorite_count': [200, 250],
    'reply_count': [50, 60]
})

# Analyze Twitter performance
performance_analysis = social_analytics.analyze_twitter_performance(twitter_data)
print("Twitter Performance Analysis:", performance_analysis)

# Analyze engagement patterns
engagement_analysis = social_analytics.analyze_engagement(twitter_data)
print("Engagement Analysis:", engagement_analysis)

# Analyze content performance
content_analysis = social_analytics.analyze_content_performance(twitter_data)
print("Content Analysis:", content_analysis)
```

## 3. Comparative Analytics Example

```python
from agents.analytics import ComparativeAnalyticsAgent

# Initialize the agent
comparative_analytics = ComparativeAnalyticsAgent()

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

# Compare performance across channels
comparison = comparative_analytics.compare_performance(
    website_data,
    analytics_data,
    twitter_data
)
print("Performance Comparison:", comparison)

# Analyze cross-channel impact
impact_analysis = comparative_analytics.analyze_cross_channel_impact(
    website_data,
    analytics_data,
    twitter_data
)
print("Cross-Channel Impact Analysis:", impact_analysis)
```

## 4. Integrated Analysis Example

```python
from agents.analytics import (
    WebsiteAnalyticsAgent,
    SocialMediaAnalyticsAgent,
    ComparativeAnalyticsAgent
)

# Initialize all agents
website_analytics = WebsiteAnalyticsAgent()
social_analytics = SocialMediaAnalyticsAgent()
comparative_analytics = ComparativeAnalyticsAgent()

# Example data
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

# Perform comprehensive analysis
def perform_comprehensive_analysis():
    # Website analysis
    website_performance = website_analytics.analyze_performance(website_data)
    website_behavior = website_analytics.analyze_user_behavior(website_data)
    
    # Social media analysis
    twitter_performance = social_analytics.analyze_twitter_performance(twitter_data)
    engagement_patterns = social_analytics.analyze_engagement(twitter_data)
    
    # Comparative analysis
    cross_channel_impact = comparative_analytics.analyze_cross_channel_impact(
        website_data,
        analytics_data,
        twitter_data
    )
    
    # Combine results
    return {
        'website_analysis': {
            'performance': website_performance,
            'user_behavior': website_behavior
        },
        'social_media_analysis': {
            'performance': twitter_performance,
            'engagement': engagement_patterns
        },
        'cross_channel_analysis': cross_channel_impact
    }

# Execute analysis
results = perform_comprehensive_analysis()
print("Comprehensive Analysis Results:", results)
```

## 5. Error Handling Example

```python
from agents.analytics import WebsiteAnalyticsAgent
from agents.error_handler import ErrorHandler

# Initialize agents
website_analytics = WebsiteAnalyticsAgent()
error_handler = ErrorHandler()

try:
    # Attempt analysis with invalid data
    invalid_data = pd.DataFrame({
        'InvalidColumn': [1, 2, 3]
    })
    
    results = website_analytics.analyze_performance(invalid_data)
    
except Exception as e:
    # Handle the error
    error_handler.handle_error(
        "WebsiteAnalysisError",
        f"Failed to analyze website performance: {str(e)}"
    )
    
    # Log the error
    website_analytics.monitoring.log_error(
        "WebsiteAnalysisError",
        str(e),
        {"data_shape": invalid_data.shape}
    )
```

## 6. Monitoring Example

```python
from agents.analytics import WebsiteAnalyticsAgent
from agents.monitoring import MonitoringAgent

# Initialize agents
website_analytics = WebsiteAnalyticsAgent()
monitoring = MonitoringAgent()

# Example data
website_data = pd.DataFrame({
    'Date': ['2024-01-01', '2024-01-02'],
    'Visitors': [1000, 1200],
    'Pageviews': [2000, 2400]
})

# Perform analysis with monitoring
def analyze_with_monitoring():
    # Start monitoring
    monitoring.start_monitoring("website_analysis")
    
    try:
        # Perform analysis
        results = website_analytics.analyze_performance(website_data)
        
        # Log success
        monitoring.log_metric(
            "analysis_completed",
            1,
            {"visitor_count": len(website_data)}
        )
        
        return results
        
    except Exception as e:
        # Log error
        monitoring.log_error(
            "analysis_failed",
            str(e),
            {"data_shape": website_data.shape}
        )
        raise
        
    finally:
        # Stop monitoring
        monitoring.stop_monitoring("website_analysis")

# Execute monitored analysis
results = analyze_with_monitoring()
print("Analysis Results with Monitoring:", results)
``` 