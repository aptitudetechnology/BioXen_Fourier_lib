#!/usr/bin/env python3
"""
BioXen Host Audit Setup Script
==============================

Creates directory structure and sets up host capability audit system.
"""

import os
import stat
from pathlib import Path


def setup_test_directories():
    """Create required directory structure for host capability audit"""
    
    base_dir = Path("tests")
    
    # Create directories
    directories = [
        base_dir,
        base_dir / "simd",
        base_dir / "gpu",
        base_dir / "storage",
        base_dir / "network"
    ]
    
    for directory in directories:
        directory.mkdir(exist_ok=True)
        print(f"Created directory: {directory}")
        
        # Create __init__.py files
        init_file = directory / "__init__.py"
        if not init_file.exists():
            init_file.write_text("")
            print(f"Created: {init_file}")
    
    return base_dir


def make_scripts_executable(base_dir: Path):
    """Make Python scripts executable"""
    
    scripts = [
        base_dir / "host-cap-audit.py",
        base_dir / "simd" / "test_simd.py",
        base_dir / "gpu" / "test_gpu.py"
    ]
    
    for script in scripts:
        if script.exists():
            # Add executable permission
            current_permissions = script.stat().st_mode
            script.chmod(current_permissions | stat.S_IEXEC)
            print(f"Made executable: {script}")


def create_readme():
    """Create README for the host audit system"""
    
    readme_content = """# BioXen Host Capability Audit

Comprehensive system analysis for bare metal BioXen deployment.

## Usage

### Basic Audit
```bash
python3 tests/host-cap-audit.py
```

### Verbose Output
```bash
python3 tests/host-cap-audit.py --verbose
```

### JSON Output
```bash
python3 tests/host-cap-audit.py --json
```

## Test Components

- **host-cap-audit.py**: Main audit script
- **simd/test_simd.py**: SIMD extensions and vectorization tests
- **gpu/test_gpu.py**: GPU acceleration capabilities (CUDA, OpenCL)

## System Requirements

- Python 3.8+
- Optional: NumPy, SciPy for performance tests
- Optional: CUDA libraries for GPU tests
- Optional: PyOpenCL for OpenCL tests

## Output

The audit generates a comprehensive report including:
- OS and kernel information
- CPU capabilities and SIMD extensions
- Memory and storage analysis
- GPU acceleration support
- BioXen deployment readiness score

## BioXen Readiness Scoring

- **80-100**: Excellent - Production ready
- **60-79**: Good - Development and testing
- **40-59**: Moderate - Basic functionality
- **0-39**: Limited - Performance constraints expected
"""
    
    readme_path = Path("tests") / "README.md"
    readme_path.write_text(readme_content)
    print(f"Created: {readme_path}")


def main():
    """Main setup function"""
    print("Setting up BioXen Host Capability Audit system...")
    
    # Create directories
    base_dir = setup_test_directories()
    
    # Make scripts executable
    make_scripts_executable(base_dir)
    
    # Create documentation
    create_readme()
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Run the audit: python3 tests/host-cap-audit.py")
    print("2. For verbose output: python3 tests/host-cap-audit.py --verbose")
    print("3. For JSON output: python3 tests/host-cap-audit.py --json")
    
    print("\nOptional dependencies for enhanced testing:")
    print("- pip install numpy scipy  # For performance tests")
    print("- pip install cupy-cuda11x  # For CUDA acceleration")
    print("- pip install pyopencl     # For OpenCL support")
    print("- pip install tensorflow-gpu  # For ML acceleration")


if __name__ == "__main__":
    main()