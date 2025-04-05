#!/usr/bin/env python3
import sys
import subprocess
import argparse
from typing import List

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run tests for the Agent System")
    parser.add_argument(
        "--unit",
        action="store_true",
        help="Run only unit tests"
    )
    parser.add_argument(
        "--integration",
        action="store_true",
        help="Run only integration tests"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Increase verbosity"
    )
    parser.add_argument(
        "--failfast",
        action="store_true",
        help="Stop on first failure"
    )
    return parser.parse_args()

def build_command(args: argparse.Namespace) -> List[str]:
    cmd = ["pytest"]
    
    # Test selection
    if args.unit:
        cmd.append("-m unit")
    elif args.integration:
        cmd.append("-m integration")
    
    # Coverage
    if args.coverage:
        cmd.extend([
            "--cov=agents",
            "--cov-report=term-missing",
            "--cov-report=html"
        ])
    
    # Verbosity
    if args.verbose:
        cmd.append("-v")
    
    # Fail fast
    if args.failfast:
        cmd.append("-x")
    
    return cmd

def main():
    args = parse_args()
    cmd = build_command(args)
    
    try:
        subprocess.run(" ".join(cmd), shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Tests failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nTest run interrupted by user")
        sys.exit(1)

if __name__ == "__main__":
    main() 