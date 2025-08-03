#!/bin/bash
# BioXen-JCVI Dependencies Installation Script
# Installs all required system packages and Python dependencies

set -e  # Exit on any error

echo "🚀 BioXen-JCVI Dependencies Installation"
echo "=============================================="
echo "Installing system packages and Python dependencies..."
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        # Ubuntu/Debian
        echo "📦 Detected Ubuntu/Debian - using apt-get"
        
        # Update package lists
        echo "🔄 Updating package lists..."
        sudo apt-get update
        
        # Install BLAST+ (required for JCVI)
        echo "🧬 Installing BLAST+ tools..."
        sudo apt-get install -y ncbi-blast+
        
        # Install optional bioinformatics tools
        echo "🔬 Installing optional bioinformatics tools..."
        sudo apt-get install -y \
            fasttree \
            raxml \
            muscle \
            clustalw \
            mafft \
            bedtools \
            samtools \
            build-essential \
            python3-dev
            
        # Install Love2D and LuaRocks for visualization
        echo "🎮 Installing Love2D and LuaRocks for real-time visualization..."
        sudo apt-get install -y love2d luarocks lua5.1-dev
            
        # Install ImageMagick for JCVI graphics (optional)
        echo "🎨 Installing ImageMagick for graphics support..."
        sudo apt-get install -y libmagickwand-dev imagemagick
        
    elif command -v yum &> /dev/null; then
        # CentOS/RHEL/Fedora
        echo "📦 Detected CentOS/RHEL/Fedora - using yum"
        
        # Install BLAST+
        echo "🧬 Installing BLAST+ tools..."
        sudo yum install -y ncbi-blast+
        
        # Install optional tools
        echo "🔬 Installing optional bioinformatics tools..."
        sudo yum install -y \
            FastTree \
            raxml \
            muscle \
            clustalw \
            mafft \
            BEDTools \
            samtools \
            gcc \
            python3-devel
            
        # Install Love2D and LuaRocks for visualization
        echo "🎮 Installing Love2D and LuaRocks for real-time visualization..."
        sudo yum install -y love luarocks lua-devel
            
        # Install ImageMagick
        echo "🎨 Installing ImageMagick for graphics support..."
        sudo yum install -y ImageMagick-devel
        
    else
        echo "⚠️  Unsupported Linux distribution. Please install manually:"
        echo "   - ncbi-blast+ (BLAST+ tools)"
        echo "   - Optional: fasttree, raxml, muscle, clustalw, mafft, bedtools, samtools"
    fi
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "📦 Detected macOS - using Homebrew"
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "❌ Homebrew not found. Please install Homebrew first:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        exit 1
    fi
    
    # Install BLAST+
    echo "🧬 Installing BLAST+ tools..."
    brew install blast
    
    # Install optional tools
    echo "🔬 Installing optional bioinformatics tools..."
    brew install \
        fasttree \
        raxml \
        muscle \
        clustal-w \
        mafft \
        bedtools \
        samtools
    
    # Install Love2D and LuaRocks for visualization
    echo "🎮 Installing Love2D and LuaRocks for real-time visualization..."
    brew install love luarocks
    
    # Install ImageMagick
    echo "🎨 Installing ImageMagick for graphics support..."
    brew install imagemagick
    
else
    echo "⚠️  Unsupported operating system: $OSTYPE"
    echo "Please install dependencies manually:"
    echo "   - BLAST+ tools (makeblastdb, blastp, blastn, blastx, tblastn)"
    echo "   - Optional: FastTree, RAxML, MUSCLE, ClustalW, MAFFT, BEDTools, SAMTools"
    exit 1
fi

# Install Python dependencies
echo ""
echo "🐍 Installing Python dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
elif command -v pip &> /dev/null; then
    pip install -r requirements.txt
else
    echo "❌ pip not found. Please install pip and run: pip install -r requirements.txt"
    exit 1
fi

# Install optional Python packages
echo "📊 Installing optional Python packages..."
pip3 install --upgrade \
    wand \
    jupyter \
    notebook \
    ipywidgets

# Install BioLib2D Love2D module via LuaRocks
echo ""
echo "🎮 Installing BioLib2D Love2D visualization module..."
if command -v luarocks &> /dev/null; then
    echo "  📦 Installing BioLib2D from GitHub..."
    luarocks install --local https://raw.githubusercontent.com/aptitudetechnology/BioLib2D/main/biolib2d-1.0.0-1.rockspec || echo "  ⚠️  BioLib2D installation failed (optional - visualization may not work)"
else
    echo "  ⚠️  LuaRocks not found - BioLib2D Love2D module not installed"
    echo "  📝 To install manually: luarocks install https://raw.githubusercontent.com/aptitudetechnology/BioLib2D/main/biolib2d-1.0.0-1.rockspec"
fi

# Verify installations
echo ""
echo "✅ Verifying installations..."

# Check BLAST+
if command -v makeblastdb &> /dev/null; then
    echo "  ✅ makeblastdb: $(makeblastdb -version | head -n1)"
else
    echo "  ❌ makeblastdb not found"
fi

if command -v blastp &> /dev/null; then
    echo "  ✅ blastp: $(blastp -version | head -n1)"
else
    echo "  ❌ blastp not found"
fi

# Check optional tools
tools=("fasttree" "raxmlHPC" "muscle" "clustalw" "mafft" "bedtools" "samtools")
for tool in "${tools[@]}"; do
    if command -v "$tool" &> /dev/null; then
        echo "  ✅ $tool: installed"
    else
        echo "  ⚠️  $tool: not found (optional)"
    fi
done

# Check Love2D and LuaRocks
echo ""
echo "🎮 Verifying Love2D and LuaRocks..."
if command -v love &> /dev/null; then
    echo "  ✅ Love2D: $(love --version | head -n1)"
else
    echo "  ⚠️  Love2D: not found (real-time visualization unavailable)"
fi

if command -v luarocks &> /dev/null; then
    echo "  ✅ LuaRocks: $(luarocks --version | head -n1)"
    
    # Check if BioLib2D is installed
    if luarocks list --local | grep -q "biolib2d"; then
        echo "  ✅ BioLib2D: installed locally"
    else
        echo "  ⚠️  BioLib2D: not installed (run: luarocks install --local https://raw.githubusercontent.com/aptitudetechnology/BioLib2D/main/biolib2d-1.0.0-1.rockspec)"
    fi
else
    echo "  ⚠️  LuaRocks: not found (BioLib2D installation unavailable)"
fi

# Check Python packages
echo ""
echo "🐍 Verifying Python packages..."
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
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Test the installation: python3 tests/test_modular_circuits.py"
echo "  2. Run Phase 4 integration: python3 phase4_jcvi_cli_integration.py"
echo "  3. Start interactive interface: python3 interactive_bioxen.py"
echo "  4. Launch Love2D visualization: love2d libs/biolib2d/ (if BioLib2D installed)"
echo ""
echo "For full functionality, ensure all tools show ✅ above."
echo "Missing optional tools will not prevent BioXen from running."
echo "📊 Static diagrams use matplotlib, 🎮 real-time visualization uses Love2D+BioLib2D"
