"""
Report Generator Agent for creating and managing reports from analytics data.
"""

from typing import Dict, List, Any, Union, Optional
import pandas as pd
import numpy as np
from datetime import datetime
import json
import os
from pathlib import Path

from ..error_handler import ErrorHandler
from ..monitoring import MonitoringAgent
from ..config import Config
from ..analytics import (
    WebsiteAnalyticsAgent,
    SocialMediaAnalyticsAgent,
    ComparativeAnalyticsAgent
)

class ReportGeneratorAgent:
    """Agent responsible for generating reports and visualizations from analytics data."""
    
    def __init__(self):
        """Initialize the Report Generator Agent."""
        self.error_handler = ErrorHandler()
        self.monitoring = MonitoringAgent()
        self.website_analytics = WebsiteAnalyticsAgent()
        self.social_analytics = SocialMediaAnalyticsAgent()
        self.comparative_analytics = ComparativeAnalyticsAgent()
        
        # Create reports directory if it doesn't exist
        self.reports_dir = Path(Config.BASE_DIR) / "reports"
        self.reports_dir.mkdir(exist_ok=True)
    
    def generate_website_report(
        self,
        website_data: pd.DataFrame,
        report_type: str = "daily",
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Generate a website performance report.
        
        Args:
            website_data (pd.DataFrame): Raw website data
            report_type (str): Type of report (daily, weekly, monthly)
            output_format (str): Output format (json, html)
            
        Returns:
            Dict[str, Any]: Generated report
        """
        try:
            # Start monitoring
            self.monitoring.start_monitoring("website_report_generation")
            
            # Perform analysis
            performance = self.website_analytics.analyze_performance(website_data)
            behavior = self.website_analytics.analyze_user_behavior(website_data)
            traffic = self.website_analytics.analyze_traffic_sources(website_data)
            
            # Generate report
            report = {
                'report_type': report_type,
                'generated_at': datetime.now().isoformat(),
                'performance_metrics': performance,
                'user_behavior': behavior,
                'traffic_analysis': traffic,
                'insights': self._generate_website_insights(performance, behavior, traffic)
            }
            
            # Save report
            self._save_report(report, "website", report_type, output_format)
            
            # Log success
            self.monitoring.log_metric(
                "website_report_generated",
                1,
                {"report_type": report_type}
            )
            
            return report
            
        except Exception as e:
            self.error_handler.handle_error(
                "WebsiteReportError",
                f"Failed to generate website report: {str(e)}"
            )
            return {}
            
        finally:
            self.monitoring.stop_monitoring("website_report_generation")
    
    def generate_social_media_report(
        self,
        twitter_data: pd.DataFrame,
        report_type: str = "daily",
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Generate a social media performance report.
        
        Args:
            twitter_data (pd.DataFrame): Raw Twitter data
            report_type (str): Type of report (daily, weekly, monthly)
            output_format (str): Output format (json, html)
            
        Returns:
            Dict[str, Any]: Generated report
        """
        try:
            # Start monitoring
            self.monitoring.start_monitoring("social_media_report_generation")
            
            # Perform analysis
            performance = self.social_analytics.analyze_twitter_performance(twitter_data)
            engagement = self.social_analytics.analyze_engagement(twitter_data)
            content = self.social_analytics.analyze_content_performance(twitter_data)
            
            # Generate report
            report = {
                'report_type': report_type,
                'generated_at': datetime.now().isoformat(),
                'performance_metrics': performance,
                'engagement_analysis': engagement,
                'content_analysis': content,
                'insights': self._generate_social_media_insights(performance, engagement, content)
            }
            
            # Save report
            self._save_report(report, "social_media", report_type, output_format)
            
            # Log success
            self.monitoring.log_metric(
                "social_media_report_generated",
                1,
                {"report_type": report_type}
            )
            
            return report
            
        except Exception as e:
            self.error_handler.handle_error(
                "SocialMediaReportError",
                f"Failed to generate social media report: {str(e)}"
            )
            return {}
            
        finally:
            self.monitoring.stop_monitoring("social_media_report_generation")
    
    def generate_comparative_report(
        self,
        website_data: pd.DataFrame,
        analytics_data: pd.DataFrame,
        twitter_data: pd.DataFrame,
        report_type: str = "daily",
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Generate a comparative performance report.
        
        Args:
            website_data (pd.DataFrame): Raw website data
            analytics_data (pd.DataFrame): Raw Google Analytics data
            twitter_data (pd.DataFrame): Raw Twitter data
            report_type (str): Type of report (daily, weekly, monthly)
            output_format (str): Output format (json, html)
            
        Returns:
            Dict[str, Any]: Generated report
        """
        try:
            # Start monitoring
            self.monitoring.start_monitoring("comparative_report_generation")
            
            # Perform analysis
            comparison = self.comparative_analytics.compare_performance(
                website_data,
                analytics_data,
                twitter_data
            )
            impact = self.comparative_analytics.analyze_cross_channel_impact(
                website_data,
                analytics_data,
                twitter_data
            )
            
            # Generate report
            report = {
                'report_type': report_type,
                'generated_at': datetime.now().isoformat(),
                'performance_comparison': comparison,
                'cross_channel_impact': impact,
                'insights': self._generate_comparative_insights(comparison, impact)
            }
            
            # Save report
            self._save_report(report, "comparative", report_type, output_format)
            
            # Log success
            self.monitoring.log_metric(
                "comparative_report_generated",
                1,
                {"report_type": report_type}
            )
            
            return report
            
        except Exception as e:
            self.error_handler.handle_error(
                "ComparativeReportError",
                f"Failed to generate comparative report: {str(e)}"
            )
            return {}
            
        finally:
            self.monitoring.stop_monitoring("comparative_report_generation")
    
    def generate_comprehensive_report(
        self,
        website_data: pd.DataFrame,
        analytics_data: pd.DataFrame,
        twitter_data: pd.DataFrame,
        report_type: str = "daily",
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive report combining all analyses.
        
        Args:
            website_data (pd.DataFrame): Raw website data
            analytics_data (pd.DataFrame): Raw Google Analytics data
            twitter_data (pd.DataFrame): Raw Twitter data
            report_type (str): Type of report (daily, weekly, monthly)
            output_format (str): Output format (json, html)
            
        Returns:
            Dict[str, Any]: Generated report
        """
        try:
            # Start monitoring
            self.monitoring.start_monitoring("comprehensive_report_generation")
            
            # Generate individual reports
            website_report = self.generate_website_report(website_data, report_type, output_format)
            social_report = self.generate_social_media_report(twitter_data, report_type, output_format)
            comparative_report = self.generate_comparative_report(
                website_data,
                analytics_data,
                twitter_data,
                report_type,
                output_format
            )
            
            # Combine reports
            comprehensive_report = {
                'report_type': report_type,
                'generated_at': datetime.now().isoformat(),
                'website_analysis': website_report,
                'social_media_analysis': social_report,
                'comparative_analysis': comparative_report,
                'executive_summary': self._generate_executive_summary(
                    website_report,
                    social_report,
                    comparative_report
                )
            }
            
            # Save report
            self._save_report(comprehensive_report, "comprehensive", report_type, output_format)
            
            # Log success
            self.monitoring.log_metric(
                "comprehensive_report_generated",
                1,
                {"report_type": report_type}
            )
            
            return comprehensive_report
            
        except Exception as e:
            self.error_handler.handle_error(
                "ComprehensiveReportError",
                f"Failed to generate comprehensive report: {str(e)}"
            )
            return {}
            
        finally:
            self.monitoring.stop_monitoring("comprehensive_report_generation")
    
    def _save_report(
        self,
        report: Dict[str, Any],
        report_type: str,
        period: str,
        output_format: str
    ) -> None:
        """
        Save report to file.
        
        Args:
            report (Dict[str, Any]): Report data
            report_type (str): Type of report
            period (str): Report period
            output_format (str): Output format
        """
        try:
            # Create filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{report_type}_{period}_{timestamp}.{output_format}"
            filepath = self.reports_dir / filename
            
            # Save based on format
            if output_format == "json":
                with open(filepath, 'w') as f:
                    json.dump(report, f, indent=2)
            elif output_format == "html":
                html_content = self._generate_html_report(report)
                with open(filepath, 'w') as f:
                    f.write(html_content)
            
            # Log save
            self.monitoring.log_metric(
                "report_saved",
                1,
                {
                    "report_type": report_type,
                    "period": period,
                    "format": output_format
                }
            )
            
        except Exception as e:
            self.error_handler.handle_error(
                "ReportSaveError",
                f"Failed to save report: {str(e)}"
            )
    
    def _generate_html_report(self, report: Dict[str, Any]) -> str:
        """
        Generate HTML report from data.
        
        Args:
            report (Dict[str, Any]): Report data
            
        Returns:
            str: HTML content
        """
        try:
            # Start HTML content
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Analytics Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    .section { margin-bottom: 20px; }
                    .metric { margin-bottom: 10px; }
                    .insight { background-color: #f5f5f5; padding: 10px; margin: 10px 0; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
            """
            
            # Add report metadata
            html += f"""
            <h1>Analytics Report</h1>
            <p>Generated at: {report.get('generated_at', 'N/A')}</p>
            <p>Report Type: {report.get('report_type', 'N/A')}</p>
            """
            
            # Add performance metrics
            if 'performance_metrics' in report:
                html += """
                <div class="section">
                    <h2>Performance Metrics</h2>
                """
                for metric, value in report['performance_metrics'].items():
                    html += f"""
                    <div class="metric">
                        <strong>{metric}:</strong> {value}
                    </div>
                    """
                html += "</div>"
            
            # Add insights
            if 'insights' in report:
                html += """
                <div class="section">
                    <h2>Key Insights</h2>
                """
                for insight in report['insights']:
                    html += f"""
                    <div class="insight">
                        {insight}
                    </div>
                    """
                html += "</div>"
            
            # Close HTML
            html += """
            </body>
            </html>
            """
            
            return html
            
        except Exception as e:
            self.error_handler.handle_error(
                "HTMLGenerationError",
                f"Failed to generate HTML report: {str(e)}"
            )
            return ""
    
    def _generate_website_insights(
        self,
        performance: Dict[str, Any],
        behavior: Dict[str, Any],
        traffic: Dict[str, Any]
    ) -> List[str]:
        """
        Generate insights from website analysis.
        
        Args:
            performance (Dict[str, Any]): Performance metrics
            behavior (Dict[str, Any]): User behavior analysis
            traffic (Dict[str, Any]): Traffic analysis
            
        Returns:
            List[str]: List of insights
        """
        insights = []
        
        # Performance insights
        if performance.get('visitor_growth', 0) > 0:
            insights.append("Website is experiencing positive visitor growth")
        else:
            insights.append("Website visitor growth needs improvement")
        
        # Behavior insights
        if behavior.get('avg_session_duration', 0) > 180:
            insights.append("Users are spending significant time on the website")
        else:
            insights.append("Consider improving content to increase session duration")
        
        # Traffic insights
        if traffic.get('organic_traffic', 0) > traffic.get('direct_traffic', 0):
            insights.append("Organic traffic is the primary source of visitors")
        else:
            insights.append("Direct traffic is the primary source of visitors")
        
        return insights
    
    def _generate_social_media_insights(
        self,
        performance: Dict[str, Any],
        engagement: Dict[str, Any],
        content: Dict[str, Any]
    ) -> List[str]:
        """
        Generate insights from social media analysis.
        
        Args:
            performance (Dict[str, Any]): Performance metrics
            engagement (Dict[str, Any]): Engagement analysis
            content (Dict[str, Any]): Content analysis
            
        Returns:
            List[str]: List of insights
        """
        insights = []
        
        # Performance insights
        if performance.get('engagement_rate', 0) > 0.02:
            insights.append("Social media content is generating strong engagement")
        else:
            insights.append("Social media engagement needs improvement")
        
        # Engagement insights
        if engagement.get('total_engagement', 0) > 1000:
            insights.append("High level of social media engagement achieved")
        else:
            insights.append("Consider strategies to increase social media engagement")
        
        # Content insights
        if content.get('top_content_type', '') == 'video':
            insights.append("Video content is performing best on social media")
        else:
            insights.append(f"{content.get('top_content_type', 'content')} is performing best on social media")
        
        return insights
    
    def _generate_comparative_insights(
        self,
        comparison: Dict[str, Any],
        impact: Dict[str, Any]
    ) -> List[str]:
        """
        Generate insights from comparative analysis.
        
        Args:
            comparison (Dict[str, Any]): Performance comparison
            impact (Dict[str, Any]): Cross-channel impact
            
        Returns:
            List[str]: List of insights
        """
        insights = []
        
        # Comparison insights
        if comparison.get('website_growth', 0) > comparison.get('twitter_growth', 0):
            insights.append("Website growth is outpacing social media growth")
        else:
            insights.append("Social media growth is outpacing website growth")
        
        # Impact insights
        if impact.get('correlation', 0) > 0.5:
            insights.append("Strong correlation between website and social media performance")
        else:
            insights.append("Weak correlation between website and social media performance")
        
        return insights
    
    def _generate_executive_summary(
        self,
        website_report: Dict[str, Any],
        social_report: Dict[str, Any],
        comparative_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate executive summary from all reports.
        
        Args:
            website_report (Dict[str, Any]): Website analysis report
            social_report (Dict[str, Any]): Social media analysis report
            comparative_report (Dict[str, Any]): Comparative analysis report
            
        Returns:
            Dict[str, Any]: Executive summary
        """
        try:
            summary = {
                'overview': {
                    'website_performance': website_report.get('performance_metrics', {}),
                    'social_media_performance': social_report.get('performance_metrics', {}),
                    'cross_channel_impact': comparative_report.get('cross_channel_impact', {})
                },
                'key_metrics': {
                    'website_visitors': website_report.get('performance_metrics', {}).get('total_visitors', 0),
                    'social_engagement': social_report.get('performance_metrics', {}).get('total_engagement', 0),
                    'correlation': comparative_report.get('cross_channel_impact', {}).get('correlation', 0)
                },
                'recommendations': self._generate_recommendations(
                    website_report,
                    social_report,
                    comparative_report
                )
            }
            
            return summary
            
        except Exception as e:
            self.error_handler.handle_error(
                "SummaryGenerationError",
                f"Failed to generate executive summary: {str(e)}"
            )
            return {}
    
    def _generate_recommendations(
        self,
        website_report: Dict[str, Any],
        social_report: Dict[str, Any],
        comparative_report: Dict[str, Any]
    ) -> List[str]:
        """
        Generate recommendations based on analysis.
        
        Args:
            website_report (Dict[str, Any]): Website analysis report
            social_report (Dict[str, Any]): Social media analysis report
            comparative_report (Dict[str, Any]): Comparative analysis report
            
        Returns:
            List[str]: List of recommendations
        """
        recommendations = []
        
        # Website recommendations
        if website_report.get('performance_metrics', {}).get('bounce_rate', 0) > 0.5:
            recommendations.append("Improve website content to reduce bounce rate")
        
        # Social media recommendations
        if social_report.get('performance_metrics', {}).get('engagement_rate', 0) < 0.02:
            recommendations.append("Enhance social media content strategy to increase engagement")
        
        # Cross-channel recommendations
        if comparative_report.get('cross_channel_impact', {}).get('correlation', 0) < 0.3:
            recommendations.append("Develop integrated marketing strategy to improve cross-channel performance")
        
        return recommendations 