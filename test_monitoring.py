import sys
import os
from pathlib import Path
import subprocess
import time
import requests

def test_monitoring():
    """Test the monitoring system"""
    try:
        # Start the monitoring server
        process = subprocess.Popen(
            [sys.executable, "-m", "agents.monitoring_ui"],
            cwd=Path(__file__).parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        time.sleep(2)
        
        # Test the dashboard
        response = requests.get("http://localhost:8000")
        if response.status_code != 200:
            raise Exception(f"Dashboard returned status code {response.status_code}")
        
        # Test the metrics endpoint
        response = requests.get("http://localhost:8000/metrics")
        if response.status_code != 200:
            raise Exception(f"Metrics endpoint returned status code {response.status_code}")
        
        # Test the system metrics API
        response = requests.get("http://localhost:8000/api/system_metrics")
        if response.status_code != 200:
            raise Exception(f"System metrics API returned status code {response.status_code}")
        
        # Test the agent metrics API
        response = requests.get("http://localhost:8000/api/agent_metrics")
        if response.status_code != 200:
            raise Exception(f"Agent metrics API returned status code {response.status_code}")
        
        print("All tests passed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")
        return False
    finally:
        # Stop the server
        process.terminate()
        process.wait()
    
    return True

if __name__ == "__main__":
    test_monitoring() 