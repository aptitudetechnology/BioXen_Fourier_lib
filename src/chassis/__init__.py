"""
BioXen Chassis Management - Support for different cellular platforms

This module implements support for different cellular chassis platforms
including E. coli (prokaryotic) and Yeast (eukaryotic) for biological virtualization.
"""

from .base import ChassisType, BaseChassis
from .ecoli import EcoliChassis
from .yeast import YeastChassis

__all__ = ['ChassisType', 'BaseChassis', 'EcoliChassis', 'YeastChassis']
