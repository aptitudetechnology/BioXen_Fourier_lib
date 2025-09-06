# Phase 1.4 Import Fix Implementation

## Problem Analysis
Current setup.py uses `find_packages()` from root, but source is in `src/`
This causes package structure mismatch between development and installed package.

## Solution: Update setup.py for src-layout

```python
from setuptools import setup, find_packages

setup(
    name="bioxen_jcvi_vm_lib",
    version="0.0.5",
    author="aptitudetechnology",
    author_email="support@aptitudetechnology.com", 
    description="BioXen Hypervisor-focused biological VM management library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aptitudetechnology/BioXen_jcvi_vm_lib",
    
    # Fix: Specify src layout
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Fix: Ensure API modules are discoverable
    package_data={
        "": ["*.md", "*.txt", "*.yml", "*.yaml"],
    },
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent", 
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: System :: Distributed Computing",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pylua-bioxen-vm-lib>=0.1.22",
        "questionary>=2.1.0", 
        "rich>=13.0.0",
    ],
    
    # Fix: Entry points for CLI
    entry_points={
        "console_scripts": [
            "bioxen=bioxen_jcvi_vm_lib.cli.main:main",
        ],
    },
)
```

## Result After Fix
✅ `import bioxen_jcvi_vm_lib` will work
✅ `from bioxen_jcvi_vm_lib.api import create_bio_vm` will work  
✅ `pip install bioxen-jcvi-vm-lib` → functional API imports
✅ CLI command `bioxen` will be available
