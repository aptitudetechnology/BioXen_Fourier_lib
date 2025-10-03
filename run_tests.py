#!/usr/bin/env python3
"""
Test runner for PyCWT-mod REST API.

Usage:
    python run_tests.py               # Run all tests
    python run_tests.py --fast        # Skip slow tests
    python run_tests.py --unit        # Run only unit tests
    python run_tests.py --integration # Run only integration tests
    python run_tests.py --hardware    # Run only hardware tests
    python run_tests.py --coverage    # Generate coverage report
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*70}")
    print(f"  {description}")
    print(f"{'='*70}\n")
    
    result = subprocess.run(cmd, shell=True)
    
    if result.returncode != 0:
        print(f"\n❌ {description} failed with exit code {result.returncode}")
        return False
    else:
        print(f"\n✅ {description} completed successfully")
        return True


def main():
    parser = argparse.ArgumentParser(description="PyCWT-mod API Test Runner")
    
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Skip slow tests"
    )
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
        "--hardware",
        action="store_true",
        help="Run only hardware tests (requires FPGA/GPU)"
    )
    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Run only benchmark tests"
    )
    parser.add_argument(
        "--coverage",
        action="store_true",
        help="Generate coverage report"
    )
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "test_file",
        nargs="?",
        help="Specific test file to run"
    )
    
    args = parser.parse_args()
    
    # Build pytest command
    cmd_parts = ["pytest"]
    
    # Add markers
    markers = []
    if args.fast:
        markers.append("not slow")
    if args.unit:
        markers.append("unit")
    if args.integration:
        markers.append("integration")
    if args.hardware:
        markers.append("hardware")
    if args.benchmark:
        markers.append("benchmark")
    
    if markers:
        cmd_parts.append(f'-m "{" and ".join(markers)}"')
    
    # Add options
    if args.coverage:
        cmd_parts.extend(["--cov=server", "--cov-report=html", "--cov-report=term"])
    
    if args.parallel:
        cmd_parts.append("-n auto")
    
    if args.verbose:
        cmd_parts.append("-vv")
    
    # Add specific test file if provided
    if args.test_file:
        cmd_parts.append(args.test_file)
    else:
        cmd_parts.append("server/tests/")
    
    # Run tests
    cmd = " ".join(cmd_parts)
    success = run_command(cmd, "Running Tests")
    
    # Print summary
    print(f"\n{'='*70}")
    print("  Test Summary")
    print(f"{'='*70}\n")
    
    if success:
        print("✅ All tests passed!")
        
        if args.coverage:
            print("\n📊 Coverage report generated:")
            print("   HTML: server/tests/htmlcov/index.html")
            print("   Terminal: see above")
    else:
        print("❌ Some tests failed. See output above for details.")
        sys.exit(1)


if __name__ == "__main__":
    main()
