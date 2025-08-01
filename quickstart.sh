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

# Install pytest if not available
echo ""
echo "Installing pytest for testing..."
python3 -m pip install pytest --user --quiet 2>/dev/null || {
    echo "⚠️  Could not install pytest, skipping tests"
    SKIP_TESTS=1
}

# Run quick tests
if [ -z "$SKIP_TESTS" ]; then
    echo ""
    echo "Running basic functionality tests..."
    python3 -m pytest tests/ -v --tb=short 2>/dev/null || {
        echo "⚠️  Some tests failed, but continuing with demo"
    }
else
    echo "⚠️  Skipping tests (pytest not available)"
fi

echo ""
echo "🚀 Running BioXen test suite..."
echo ""

# Run our custom test script
python3 test_bioxen.py

echo ""
echo "🎬 Running simple demo..."
echo ""

# Run the simple demo
python3 simple_demo.py

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
