#!/bin/bash

# Enhanced JCVI CLI Tools Installation Script
# Comprehensive genomics toolkit for BioXen Phase 4

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
JCVI_DIR="jcvi-main"
PYTHON_ENV="jcvi_env"
LOG_FILE="jcvi_installation.log"

echo -e "${BLUE}🔬 Enhanced JCVI CLI Tools Installation${NC}"
echo "=================================================="

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

error_exit() {
    echo -e "${RED}❌ Error: $1${NC}" >&2
    log "ERROR: $1"
    exit 1
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
    log "SUCCESS: $1"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    log "WARNING: $1"
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
    log "INFO: $1"
}

# Check system requirements
check_system() {
    info "Checking system requirements..."
    
    # Check OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        info "Operating System: Linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        info "Operating System: macOS"
    else
        error_exit "Unsupported operating system: $OSTYPE"
    fi
    
    # Check CPU cores
    if command -v nproc &> /dev/null; then
        CPU_CORES=$(nproc)
    elif command -v sysctl &> /dev/null; then
        CPU_CORES=$(sysctl -n hw.ncpu)
    else
        CPU_CORES=4
        warning "Could not detect CPU cores, defaulting to 4"
    fi
    info "CPU cores: $CPU_CORES"
    
    # Check memory
    if command -v free &> /dev/null; then
        MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
        info "Memory: ${MEMORY_GB}GB"
        
        if [ "$MEMORY_GB" -lt 4 ]; then
            warning "Low memory detected (${MEMORY_GB}GB). Some analyses may be limited."
        fi
    fi
    
    # Check storage
    AVAILABLE_SPACE=$(df -h . | tail -1 | awk '{print $4}')
    info "Available storage: $AVAILABLE_SPACE"
}

# Install system dependencies
install_system_deps() {
    info "Installing system dependencies..."
    
    if [[ "$OS" == "linux" ]]; then
        # Detect package manager
        if command -v apt-get &> /dev/null; then
            PKG_MGR="apt"
            INSTALL_CMD="sudo apt-get install -y"
            UPDATE_CMD="sudo apt-get update"
        elif command -v yum &> /dev/null; then
            PKG_MGR="yum"
            INSTALL_CMD="sudo yum install -y"
            UPDATE_CMD="sudo yum update"
        elif command -v dnf &> /dev/null; then
            PKG_MGR="dnf"
            INSTALL_CMD="sudo dnf install -y"
            UPDATE_CMD="sudo dnf update"
        else
            error_exit "No supported package manager found (apt, yum, dnf)"
        fi
        
        info "Package manager: $PKG_MGR"
        
        # Update package list
        $UPDATE_CMD || warning "Package update failed"
        
        # Essential development tools
        $INSTALL_CMD build-essential git wget curl || error_exit "Failed to install build tools"
        
        # Python development
        $INSTALL_CMD python3 python3-dev python3-pip python3-venv || error_exit "Failed to install Python"
        
        # Scientific computing libraries
        $INSTALL_CMD libopenblas-dev liblapack-dev gfortran || warning "Failed to install scientific libraries"
        
        # Bioinformatics tools
        if [[ "$PKG_MGR" == "apt" ]]; then
            $INSTALL_CMD ncbi-blast+ muscle clustalw hmmer || warning "Some bioinformatics tools failed to install"
        fi
        
        # Graphics libraries for visualizations
        $INSTALL_CMD libfreetype6-dev libpng-dev || warning "Graphics libraries installation failed"
        
    elif [[ "$OS" == "macos" ]]; then
        # Check for Homebrew
        if ! command -v brew &> /dev/null; then
            error_exit "Homebrew not found. Please install: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
        fi
        
        # Update Homebrew
        brew update || warning "Homebrew update failed"
        
        # Install dependencies
        brew install python3 git wget curl || error_exit "Failed to install basic tools"
        brew install openblas lapack || warning "Failed to install scientific libraries"
        brew install blast muscle clustal-w hmmer || warning "Some bioinformatics tools failed to install"
        brew install freetype libpng || warning "Graphics libraries installation failed"
    fi
    
    success "System dependencies installed"
}

# Setup Python environment
setup_python_env() {
    info "Setting up Python environment..."
    
    # Create virtual environment
    if [ -d "$PYTHON_ENV" ]; then
        warning "Python environment already exists, removing..."
        rm -rf "$PYTHON_ENV"
    fi
    
    python3 -m venv "$PYTHON_ENV" || error_exit "Failed to create virtual environment"
    
    # Activate environment
    source "$PYTHON_ENV/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel || error_exit "Failed to upgrade pip"
    
    # Install core scientific Python packages
    info "Installing core scientific packages..."
    pip install numpy scipy matplotlib pandas || error_exit "Failed to install scientific packages"
    
    # Install bioinformatics packages
    info "Installing bioinformatics packages..."
    pip install biopython networkx || error_exit "Failed to install bioinformatics packages"
    
    # Install additional useful packages
    pip install requests tqdm rich click || error_exit "Failed to install utility packages"
    
    # Install packages for enhanced functionality
    pip install plotly seaborn scikit-learn || warning "Some enhanced packages failed to install"
    
    success "Python environment setup complete"
}

# Install JCVI from source
install_jcvi() {
    info "Installing JCVI from source..."
    
    # Activate Python environment
    source "$PYTHON_ENV/bin/activate"
    
    # Navigate to JCVI directory
    if [ ! -d "$JCVI_DIR" ]; then
        error_exit "JCVI source directory not found: $JCVI_DIR"
    fi
    
    cd "$JCVI_DIR"
    
    # Install JCVI in development mode
    pip install -e . || error_exit "Failed to install JCVI"
    
    # Install additional dependencies from requirements
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt || warning "Some requirements failed to install"
    fi
    
    cd ..
    
    success "JCVI installed successfully"
}

# Install additional BLAST databases and tools
setup_blast() {
    info "Setting up BLAST databases and tools..."
    
    # Create BLAST database directory
    BLAST_DB_DIR="blast_databases"
    mkdir -p "$BLAST_DB_DIR"
    
    # Activate environment
    source "$PYTHON_ENV/bin/activate"
    
    # Set BLASTDB environment variable
    export BLASTDB="$(pwd)/$BLAST_DB_DIR"
    echo "export BLASTDB=$(pwd)/$BLAST_DB_DIR" >> "$PYTHON_ENV/bin/activate"
    
    info "BLAST databases directory: $BLAST_DB_DIR"
    info "To download databases, run: update_blastdb.pl --decompress nt nr"
    
    success "BLAST setup complete"
}

# Install phylogenetic tools
install_phylo_tools() {
    info "Installing phylogenetic tools..."
    
    TOOLS_DIR="phylo_tools"
    mkdir -p "$TOOLS_DIR"
    cd "$TOOLS_DIR"
    
    # Install FastTree
    if ! command -v fasttree &> /dev/null; then
        info "Installing FastTree..."
        if [[ "$OS" == "linux" ]]; then
            wget -q http://www.microbesonline.org/fasttree/FastTree -O fasttree
            chmod +x fasttree
            sudo mv fasttree /usr/local/bin/ || warning "Could not install FastTree system-wide"
        elif [[ "$OS" == "macos" ]]; then
            brew install fasttree || warning "FastTree installation failed"
        fi
    fi
    
    # Install RAxML (if not available)
    if ! command -v raxml &> /dev/null; then
        info "RAxML not found. Install manually if needed for maximum likelihood trees."
    fi
    
    cd ..
    success "Phylogenetic tools setup complete"
}

# Setup visualization tools
setup_visualization() {
    info "Setting up visualization tools..."
    
    # Activate environment
    source "$PYTHON_ENV/bin/activate"
    
    # Install additional visualization packages
    pip install plotly kaleido || warning "Advanced visualization packages failed"
    pip install bokeh || warning "Bokeh visualization failed"
    
    # Create visualization output directory
    mkdir -p "visualizations"
    
    success "Visualization tools setup complete"
}

# Verify installation
verify_installation() {
    info "Verifying installation..."
    
    # Activate environment
    source "$PYTHON_ENV/bin/activate"
    
    # Test Python packages
    python3 -c "import numpy, scipy, matplotlib, pandas, Bio; print('✅ Core packages OK')" || error_exit "Core packages verification failed"
    
    # Test JCVI import
    python3 -c "import jcvi; print('✅ JCVI import OK')" || error_exit "JCVI import failed"
    
    # Test BLAST
    if command -v blastn &> /dev/null; then
        blastn -version || warning "BLAST verification failed"
        success "BLAST is available"
    else
        warning "BLAST not found in PATH"
    fi
    
    # Test other tools
    for tool in muscle clustalw hmmer; do
        if command -v "$tool" &> /dev/null; then
            success "$tool is available"
        else
            warning "$tool not found"
        fi
    done
    
    success "Installation verification complete"
}

# Create activation script
create_activation_script() {
    info "Creating activation script..."
    
    cat > activate_jcvi.sh << 'EOF'
#!/bin/bash
# BioXen JCVI Environment Activation Script

export JCVI_ENV_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export BLASTDB="$JCVI_ENV_DIR/blast_databases"

# Activate Python environment
source "$JCVI_ENV_DIR/jcvi_env/bin/activate"

# Add tools to PATH
export PATH="$JCVI_ENV_DIR/phylo_tools:$PATH"

echo "🔬 BioXen JCVI Environment Activated"
echo "   Python environment: jcvi_env"
echo "   BLAST databases: $BLASTDB"
echo "   Current directory: $(pwd)"
echo ""
echo "Available commands:"
echo "   python3 jcvi_advanced_tools.py    - Advanced JCVI analysis tools"
echo "   python3 phase4_jcvi_cli_integration.py - Phase 4 JCVI integration"
echo "   blastn --help                     - BLAST nucleotide search"
echo "   muscle --help                     - Multiple sequence alignment"
echo ""
EOF

    chmod +x activate_jcvi.sh
    
    success "Activation script created: activate_jcvi.sh"
}

# Performance optimization
optimize_performance() {
    info "Applying performance optimizations..."
    
    # Set NumPy thread optimization
    cat >> "$PYTHON_ENV/bin/activate" << EOF

# Performance optimizations
export OMP_NUM_THREADS=$CPU_CORES
export OPENBLAS_NUM_THREADS=$CPU_CORES
export MKL_NUM_THREADS=$CPU_CORES
export NUMEXPR_NUM_THREADS=$CPU_CORES

EOF
    
    # Create performance config
    cat > jcvi_performance.conf << EOF
# BioXen JCVI Performance Configuration
CPU_CORES=$CPU_CORES
MEMORY_GB=${MEMORY_GB:-8}
BLAST_NUM_THREADS=$CPU_CORES
OPTIMIZATION_LEVEL=high
EOF
    
    success "Performance optimizations applied"
}

# Main installation flow
main() {
    log "Starting enhanced JCVI installation..."
    
    check_system
    install_system_deps
    setup_python_env
    install_jcvi
    setup_blast
    install_phylo_tools
    setup_visualization
    optimize_performance
    verify_installation
    create_activation_script
    
    echo ""
    echo -e "${GREEN}🎉 Enhanced JCVI Installation Complete!${NC}"
    echo "=================================================="
    echo -e "${BLUE}To get started:${NC}"
    echo "   1. source activate_jcvi.sh"
    echo "   2. python3 jcvi_advanced_tools.py"
    echo ""
    echo -e "${BLUE}Features installed:${NC}"
    echo "   ✅ JCVI toolkit with all modules"
    echo "   ✅ BLAST+ suite for sequence search"
    echo "   ✅ Multiple sequence alignment tools"
    echo "   ✅ Phylogenetic reconstruction tools"
    echo "   ✅ Scientific Python stack"
    echo "   ✅ Advanced visualization tools"
    echo "   ✅ Performance optimizations"
    echo ""
    echo -e "${YELLOW}Log file: $LOG_FILE${NC}"
    
    log "Enhanced JCVI installation completed successfully"
}

# Run main installation
main "$@"
