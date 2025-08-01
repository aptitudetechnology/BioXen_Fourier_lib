#!/bin/bash
# Quick start script for BioXen

echo "🧬 BioXen Biological Hypervisor - Quick Start 🧬"
echo "================================================"

# Check Python version
python3 --version || {
    echo "❌ Python 3 is required but not found"
    exit 1
}

echo "✅ Python 3 found"

# Run quick tests
echo ""
echo "Running basic functionality tests..."
python3 -m pytest tests/ -v --tb=short || {
    echo "⚠️  Some tests failed, but continuing with demo"
}

echo ""
echo "🚀 Starting BioXen demo..."
echo ""

# Run the demo
python3 demo.py

echo ""
echo "🎉 BioXen demo completed!"
echo ""
echo "Next steps:"
echo "  - Review the code in src/ directory"
echo "  - Check out the genetic circuits in src/genetics/"
echo "  - Explore VM image building in src/genome/"
echo "  - Run 'make help' to see all available commands"
echo ""
echo "For development:"
echo "  make dev-install  # Install development dependencies"
echo "  make test         # Run full test suite"
echo "  make lint         # Check code quality"
echo ""
