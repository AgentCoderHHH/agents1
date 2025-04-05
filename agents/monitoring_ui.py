from flask import Flask, render_template, jsonify, redirect, url_for
import psutil
import time
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from .monitoring import API_CALLS, API_ERRORS, OPERATION_DURATION, ACTIVE_OPERATIONS, metrics_app
import os
from pathlib import Path
from loguru import logger
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple

# Use the same port as the Prometheus server
DASHBOARD_PORT = 8000

# Get the absolute path to the templates directory
TEMPLATES_DIR = Path(__file__).parent.parent / 'templates'

app = Flask(
    __name__,
    template_folder=str(TEMPLATES_DIR),
    static_folder=str(TEMPLATES_DIR)
)

@app.route('/test')
def test():
    """Test endpoint to verify template rendering"""
    return "<h1>Test Page</h1><p>If you can see this, the server is working.</p>"

def get_system_metrics():
    """Get current system metrics"""
    try:
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'memory_available': psutil.virtual_memory().available / (1024 * 1024 * 1024),  # GB
            'disk_usage': psutil.disk_usage('/').percent
        }
    except Exception as e:
        logger.error(f"Failed to get system metrics: {e}")
        return {
            'cpu_percent': 0,
            'memory_percent': 0,
            'memory_available': 0,
            'disk_usage': 0
        }

@app.route('/')
def index():
    """Redirect to the dashboard"""
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    """Render the monitoring dashboard"""
    try:
        template_path = TEMPLATES_DIR / 'dashboard.html'
        if not template_path.exists():
            logger.error(f"Dashboard template not found at {template_path}")
            return "Dashboard template not found", 500
        return render_template('dashboard.html')
    except Exception as e:
        logger.error(f"Failed to render dashboard: {e}")
        return "Error loading dashboard", 500

@app.route('/api/system_metrics')
def system_metrics():
    """Return current system metrics"""
    try:
        return jsonify(get_system_metrics())
    except Exception as e:
        logger.error(f"Failed to get system metrics: {e}")
        return "Error getting system metrics", 500

@app.route('/api/agent_metrics')
def agent_metrics():
    """Return agent-specific metrics"""
    try:
        metrics = {
            'api_calls': {},
            'api_errors': {},
            'operation_duration': {},
            'active_operations': {}
        }
        
        # Collect metrics from Prometheus collectors
        for sample in API_CALLS.collect():
            for s in sample.samples:
                metrics['api_calls'][f"{s.labels['agent']}_{s.labels['operation']}"] = s.value
        
        for sample in API_ERRORS.collect():
            for s in sample.samples:
                metrics['api_errors'][f"{s.labels['agent']}_{s.labels['operation']}_{s.labels['error_type']}"] = s.value
        
        for sample in OPERATION_DURATION.collect():
            for s in sample.samples:
                metrics['operation_duration'][f"{s.labels['agent']}_{s.labels['operation']}"] = s.value
        
        for sample in ACTIVE_OPERATIONS.collect():
            for s in sample.samples:
                metrics['active_operations'][s.labels['agent']] = s.value
        
        return jsonify(metrics)
    except Exception as e:
        logger.error(f"Failed to get agent metrics: {e}")
        return "Error getting agent metrics", 500

def start_monitoring(host='0.0.0.0', port=DASHBOARD_PORT):
    """Start the monitoring dashboard server"""
    try:
        logger.info(f"Starting monitoring dashboard on {host}:{port}")
        # Create a WSGI app that serves metrics on /metrics and the Flask app on all other paths
        app_dispatch = DispatcherMiddleware(app, {
            '/metrics': metrics_app
        })
        run_simple(host, port, app_dispatch, threaded=True)
    except Exception as e:
        logger.error(f"Failed to start monitoring dashboard: {e}")
        raise

# Only run if this file is executed directly
if __name__ == '__main__':
    start_monitoring() 