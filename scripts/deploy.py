#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse
from pathlib import Path

def parse_args():
    parser = argparse.ArgumentParser(description="Deploy the Agent System")
    parser.add_argument(
        "--env",
        choices=["development", "staging", "production"],
        default="development",
        help="Deployment environment"
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Install system dependencies"
    )
    return parser.parse_args()

def create_virtualenv():
    """Create and activate virtual environment"""
    print("Creating virtual environment...")
    subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    
    # Get the activate script path based on OS
    if sys.platform == "win32":
        activate_script = "venv\\Scripts\\activate.bat"
    else:
        activate_script = "source venv/bin/activate"
    
    print(f"To activate the virtual environment, run: {activate_script}")

def install_dependencies():
    """Install Python dependencies"""
    print("Installing Python dependencies...")
    subprocess.run([
        "venv/bin/pip" if sys.platform != "win32" else "venv\\Scripts\\pip",
        "install",
        "-r",
        "requirements.txt"
    ], check=True)

def create_service_file():
    """Create systemd service file for Linux systems"""
    if sys.platform != "linux":
        print("Systemd service creation is only supported on Linux")
        return

    service_content = f"""[Unit]
Description=Agent System Service
After=network.target

[Service]
Type=simple
User={os.getenv('USER')}
WorkingDirectory={os.getcwd()}
Environment="PATH={os.getcwd()}/venv/bin:/usr/local/bin:/usr/bin:/bin"
Environment="PYTHONPATH={os.getcwd()}"
Environment="ENVIRONMENT=production"
ExecStart={os.getcwd()}/venv/bin/python -m agents.main
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
"""

    service_path = Path("/etc/systemd/system/agent-system.service")
    try:
        with open(service_path, "w") as f:
            f.write(service_content)
        print(f"Created service file at {service_path}")
    except PermissionError:
        print("Error: Need root permissions to create service file")
        print(f"Service content to create manually:\n{service_content}")

def setup_logging():
    """Create logging directory and set permissions"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Ensure log directory is writable
    if sys.platform != "win32":
        subprocess.run(["chmod", "755", "logs"], check=True)

def create_env_file(env: str):
    """Create environment-specific .env file"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if not env_example.exists():
        print("Error: .env.example file not found")
        return
    
    if not env_file.exists():
        print(f"Creating .env file for {env} environment...")
        env_file.write_text(env_example.read_text())
        print("Please update the .env file with your configuration")

def main():
    args = parse_args()
    
    try:
        # Create virtual environment
        create_virtualenv()
        
        # Install dependencies
        install_dependencies()
        
        # Setup logging
        setup_logging()
        
        # Create environment file
        create_env_file(args.env)
        
        # Create service file on Linux
        if sys.platform == "linux" and args.env == "production":
            create_service_file()
        
        print("\nDeployment completed successfully!")
        print("\nNext steps:")
        print("1. Update the .env file with your configuration")
        if sys.platform == "linux" and args.env == "production":
            print("2. Start the service: sudo systemctl start agent-system")
            print("3. Enable service on boot: sudo systemctl enable agent-system")
        else:
            print("2. Activate the virtual environment")
            print("3. Run the application: python -m agents.main")
            
    except subprocess.CalledProcessError as e:
        print(f"Error during deployment: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 