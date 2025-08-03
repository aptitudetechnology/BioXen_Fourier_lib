#!/bin/bash
# BioXen Terminal Visualization Setup Script

echo "🧬 Setting up BioXen Terminal DNA Transcription Monitor..."

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r terminal_requirements.txt

# Make scripts executable
chmod +x terminal_biovis.py
chmod +x generate_biodata.py

echo "✅ Setup complete!"
echo ""
echo "🚀 Usage:"
echo "  1. Generate test data: python3 generate_biodata.py"
echo "  2. Run monitor: python3 terminal_biovis.py"
echo "  3. Run with live data: python3 generate_biodata.py --continuous &"
echo "     python3 terminal_biovis.py"
echo ""
echo "📋 Command options:"
echo "  terminal_biovis.py --data=custom.json --refresh=1.0"
echo "  generate_biodata.py --vms=6 --continuous --interval=0.5"
