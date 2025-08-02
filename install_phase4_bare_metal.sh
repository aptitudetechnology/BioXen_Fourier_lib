#!/bin/bash
# BioXen-JCVI Phase 4 Bare Metal Installation Script
# Sets up JCVI toolkit with hardware optimization for maximum genomics performance

set -e  # Exit on any error

echo "🚀 BioXen-JCVI Phase 4: Bare Metal Installation"
echo "=============================================="

# Detect system information
echo "🔍 Detecting system configuration..."
CPU_CORES=$(nproc)
MEMORY_GB=$(free -g | awk '/^Mem:/{print $2}')
OS_DISTRO=$(lsb_release -si 2>/dev/null || echo "Unknown")

echo "   CPU Cores: $CPU_CORES"
echo "   Memory: ${MEMORY_GB} GB"
echo "   OS: $OS_DISTRO"

# Check if we're running with sufficient privileges
if [[ $EUID -eq 0 ]]; then
    echo "⚠️  Running as root - be careful with system modifications"
    SUDO=""
else
    echo "📋 Will use sudo for system package installation"
    SUDO="sudo"
fi

# Function to install system packages
install_system_packages() {
    echo ""
    echo "📦 Installing system dependencies..."
    
    if command -v apt-get >/dev/null 2>&1; then
        # Ubuntu/Debian
        echo "   Detected apt package manager (Ubuntu/Debian)"
        $SUDO apt-get update
        $SUDO apt-get install -y \
            python3-dev \
            python3-pip \
            build-essential \
            ncbi-blast+ \
            imagemagick \
            git \
            wget \
            curl \
            libblas-dev \
            liblapack-dev \
            gfortran \
            cmake
            
    elif command -v yum >/dev/null 2>&1; then
        # CentOS/RHEL/Fedora
        echo "   Detected yum package manager (CentOS/RHEL/Fedora)"
        $SUDO yum update -y
        $SUDO yum install -y \
            python3-devel \
            python3-pip \
            gcc \
            gcc-c++ \
            ncbi-blast+ \
            ImageMagick \
            git \
            wget \
            curl \
            blas-devel \
            lapack-devel \
            gcc-gfortran \
            cmake
            
    elif command -v pacman >/dev/null 2>&1; then
        # Arch Linux
        echo "   Detected pacman package manager (Arch Linux)"
        $SUDO pacman -Syu --noconfirm
        $SUDO pacman -S --noconfirm \
            python \
            python-pip \
            base-devel \
            blast+ \
            imagemagick \
            git \
            wget \
            curl \
            blas \
            lapack \
            gcc-fortran \
            cmake
    else
        echo "⚠️  Unknown package manager - you may need to install dependencies manually"
        echo "   Required: python3-dev, build-essential, ncbi-blast+, imagemagick"
    fi
}

# Function to optimize Python environment
setup_python_environment() {
    echo ""
    echo "🐍 Setting up optimized Python environment..."
    
    # Upgrade pip with user install to avoid permission issues
    python3 -m pip install --user --upgrade pip setuptools wheel
    
    # Install numpy with hardware optimization
    echo "   Installing hardware-optimized NumPy..."
    python3 -m pip install --user numpy==1.24.3
    
    # Install scientific computing stack
    echo "   Installing scientific computing dependencies..."
    python3 -m pip install --user \
        scipy \
        matplotlib \
        biopython>=1.80 \
        natsort \
        more-itertools \
        questionary
    
    # Install JCVI toolkit
    echo "   Installing JCVI toolkit..."
    python3 -m pip install --user jcvi>=1.4.15
    
    echo "✅ Python environment setup complete"
}

# Function to verify installation
verify_installation() {
    echo ""
    echo "🔍 Verifying installation..."
    
    # Test Python imports
    python3 -c "import jcvi; print('✅ JCVI imported successfully')" || echo "❌ JCVI import failed"
    python3 -c "from jcvi.formats.fasta import Fasta; print('✅ JCVI FASTA parser available')" || echo "❌ JCVI FASTA parser failed"
    python3 -c "import numpy; print('✅ NumPy available:', numpy.__version__)" || echo "❌ NumPy failed"
    python3 -c "import questionary; print('✅ Questionary available')" || echo "❌ Questionary failed"
    
    # Test BLAST
    if command -v makeblastdb >/dev/null 2>&1; then
        echo "✅ BLAST+ makeblastdb available"
    else
        echo "❌ BLAST+ makeblastdb not found"
    fi
    
    if command -v blastn >/dev/null 2>&1; then
        echo "✅ BLAST+ blastn available"
    else
        echo "❌ BLAST+ blastn not found"
    fi
}

# Function to test with sample data
test_installation() {
    echo ""
    echo "🧪 Testing installation with sample data..."
    
    if [[ -f "genomes/syn3A.fasta" ]]; then
        echo "   Testing JCVI FASTA parsing..."
        python3 -c "
from jcvi.formats.fasta import Fasta
f = Fasta('genomes/syn3A.fasta')
print(f'✅ Successfully parsed {len(f)} sequences from syn3A.fasta')
" || echo "❌ FASTA parsing test failed"
    else
        echo "⚠️  No test FASTA files found - run bioxen_to_jcvi_converter.py --batch first"
    fi
}

# Function to set up performance optimizations
setup_performance_optimizations() {
    echo ""
    echo "⚡ Setting up bare metal performance optimizations..."
    
    # Check for CPU optimization flags
    if grep -q "avx2" /proc/cpuinfo; then
        echo "✅ AVX2 instruction set detected - can use vectorized operations"
        export NUMPY_OPT_FLAGS="-march=native -O3"
    fi
    
    if grep -q "avx512" /proc/cpuinfo; then
        echo "✅ AVX-512 instruction set detected - maximum vectorization available"
        export NUMPY_OPT_FLAGS="-march=native -mavx512f -O3"
    fi
    
    # Set optimal thread counts
    echo "🔧 Setting optimal threading for $CPU_CORES cores"
    export OMP_NUM_THREADS=$CPU_CORES
    export MKL_NUM_THREADS=$CPU_CORES
    export OPENBLAS_NUM_THREADS=$CPU_CORES
    
    # NUMA optimization if multiple nodes detected
    NUMA_NODES=$(ls -1d /sys/devices/system/node/node* 2>/dev/null | wc -l)
    if [[ $NUMA_NODES -gt 1 ]]; then
        echo "✅ NUMA topology detected: $NUMA_NODES nodes - can optimize memory locality"
        echo "   Consider using numactl for large genomics workloads"
    fi
    
    # GPU detection
    if command -v nvidia-smi >/dev/null 2>&1; then
        echo "✅ NVIDIA GPU detected - can accelerate genomics computations"
        nvidia-smi --query-gpu=name,memory.total --format=csv,noheader,nounits | head -1
    else
        echo "ℹ️  No NVIDIA GPU detected - using CPU-only optimizations"
    fi
}

# Function to create performance monitoring script
create_monitoring_script() {
    echo ""
    echo "📊 Creating performance monitoring script..."
    
    cat > monitor_genomics_performance.sh << 'EOF'
#!/bin/bash
# BioXen-JCVI Performance Monitor
# Monitor system performance during genomics workloads

echo "📊 BioXen-JCVI Performance Monitor"
echo "=================================="
echo "Monitoring system performance for genomics workloads..."
echo "Press Ctrl+C to stop monitoring"
echo ""

while true; do
    # CPU usage
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//')
    
    # Memory usage
    MEMORY_INFO=$(free -h | grep "Mem:")
    MEMORY_USED=$(echo $MEMORY_INFO | awk '{print $3}')
    MEMORY_TOTAL=$(echo $MEMORY_INFO | awk '{print $2}')
    
    # Load average
    LOAD_AVG=$(uptime | awk -F'load average:' '{print $2}')
    
    # GPU usage if available
    if command -v nvidia-smi >/dev/null 2>&1; then
        GPU_USAGE=$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits)
        GPU_MEMORY=$(nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader,nounits)
        echo "$(date '+%H:%M:%S') CPU: ${CPU_USAGE}% | Memory: ${MEMORY_USED}/${MEMORY_TOTAL} | Load:${LOAD_AVG} | GPU: ${GPU_USAGE}% (${GPU_MEMORY})"
    else
        echo "$(date '+%H:%M:%S') CPU: ${CPU_USAGE}% | Memory: ${MEMORY_USED}/${MEMORY_TOTAL} | Load:${LOAD_AVG}"
    fi
    
    sleep 5
done
EOF

    chmod +x monitor_genomics_performance.sh
    echo "✅ Performance monitor created: ./monitor_genomics_performance.sh"
}

# Main installation flow
main() {
    echo ""
    echo "🎯 Starting BioXen-JCVI Phase 4 installation..."
    echo ""
    
    # Ask user what to install
    echo "📋 Installation options:"
    echo "   1. Full installation (system packages + Python environment)"
    echo "   2. Python environment only (assume system packages installed)"
    echo "   3. Verification only (test existing installation)"
    echo ""
    
    read -p "Choose option (1-3): " INSTALL_OPTION
    
    case $INSTALL_OPTION in
        1)
            echo "🔧 Full installation selected"
            install_system_packages
            setup_python_environment
            setup_performance_optimizations
            create_monitoring_script
            verify_installation
            test_installation
            ;;
        2)
            echo "🐍 Python environment only"
            setup_python_environment
            setup_performance_optimizations
            create_monitoring_script
            verify_installation
            test_installation
            ;;
        3)
            echo "🔍 Verification only"
            verify_installation
            test_installation
            ;;
        *)
            echo "❌ Invalid option"
            exit 1
            ;;
    esac
    
    echo ""
    echo "🎉 BioXen-JCVI Phase 4 installation complete!"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Run: python3 phase4_jcvi_cli_integration.py"
    echo "   2. Monitor performance: ./monitor_genomics_performance.sh"
    echo "   3. For GPU acceleration, ensure CUDA toolkit is installed"
    echo ""
    echo "🚀 Ready for bare metal genomics performance!"
}

# Run main function
main
