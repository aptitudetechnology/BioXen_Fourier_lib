#!/usr/bin/env python3
"""
Setup script for BioXen biological hypervisor
"""

from setuptools import setup, find_packages

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bioxen",
    version="1.0.0",
    author="BioXen Project",
    author_email="contact@bioxen.bio",
    description="Biological hypervisor for JCVI-Syn3A minimal genomes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aptitudetechnology/bioxen",
    project_urls={
        "Bug Tracker": "https://github.com/aptitudetechnology/bioxen/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies for the basic proof of concept
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
    },
    entry_points={
        "console_scripts": [
            "bioxen=cli.main:main",
        ],
    },
)
