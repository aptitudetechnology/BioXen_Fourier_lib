#!/bin/bash
# BioXen-JCVI Dependencies Check Script
# Shows what packages need to be installed without requiring sudo

echo "🚀 BioXen-JCVI Dependencies Check"
echo "=============================================="
echo "Checking current installation status..."
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "📦 Detected Linux system"
    
    # Check for package manager
    if command -v apt-get &> /dev/null; then
        echo "📦 Package manager: apt-get (Ubuntu/Debian)"
        echo ""
        echo "To install all dependencies, run:"
        echo "  sudo ./install_dependencies.sh"
        echo ""
    elif command -v yum &> /dev/null; then
        echo "📦 Package manager: yum (CentOS/RHEL/Fedora)"
        echo ""
        echo "To install all dependencies, run:"
        echo "  sudo ./install_dependencies.sh"
        echo ""
    fi
fi

echo "🔍 Current installation status:"
echo ""

# Check BLAST+ tools
echo "📋 Required BLAST+ tools:"
blast_tools=("makeblastdb" "blastp" "blastn" "blastx" "tblastn")
for tool in "${blast_tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "  ✅ $tool: installed"
    else
        echo "  ❌ $tool: not found"
    fi
done

echo ""
echo "📋 Optional bioinformatics tools:"
tools=("fasttree" "raxmlHPC" "muscle" "clustalw" "mafft" "bedtools" "samtools")
for tool in "${tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "  ✅ $tool: installed"
    else
        echo "  ⚠️  $tool: not found (optional)"
    fi
done

echo ""
echo "🐍 Python packages:"
python3 -c "
import sys
packages = ['jcvi', 'matplotlib', 'numpy', 'scipy', 'biopython', 'questionary']
for pkg in packages:
    try:
        __import__(pkg)
        print(f'  ✅ {pkg}: installed')
    except ImportError:
        print(f'  ❌ {pkg}: not found')
"

echo ""
echo "📊 Installation commands for missing packages:"
echo ""

# Check what's missing and show commands
missing_blast=false
for tool in "${blast_tools[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        missing_blast=true
        break
    fi
done

if [ "$missing_blast" = true ]; then
    echo "🧬 Install BLAST+ tools:"
    if command -v apt-get &> /dev/null; then
        echo "  sudo apt-get install ncbi-blast+"
    elif command -v yum &> /dev/null; then
        echo "  sudo yum install ncbi-blast+"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  brew install blast"
    fi
    echo ""
fi

echo "🔬 Install optional tools (Ubuntu/Debian):"
echo "  sudo apt-get install fasttree raxml muscle clustalw mafft bedtools samtools"
echo ""

echo "🐍 Install Python packages:"
echo "  pip3 install -r requirements.txt"
echo ""

echo "📊 Summary:"
blast_count=0
for tool in "${blast_tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        ((blast_count++))
    fi
done

echo "  BLAST+ tools: $blast_count/5 installed"

optional_count=0
for tool in "${tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        ((optional_count++))
    fi
done

echo "  Optional tools: $optional_count/7 installed"

if [ $blast_count -eq 5 ]; then
    echo "  ✅ Ready for full JCVI functionality!"
else
    echo "  ⚠️  Some BLAST+ tools missing - will run in simulation mode"
fi
