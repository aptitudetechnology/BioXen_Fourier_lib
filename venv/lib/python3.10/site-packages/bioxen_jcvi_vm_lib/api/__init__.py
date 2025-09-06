"""
BioXen Factory Pattern API

Hypervisor-focused biological VM management following pylua_bioxen_vm_lib patterns.
Phase 1.3: Hypervisor-only implementation excluding JCVI dependencies.
"""

from typing import Optional
from .biological_vm import BiologicalVM, BasicBiologicalVM, XCPngBiologicalVM
from .factory import create_bio_vm, create_biological_vm, get_supported_biological_types, get_supported_vm_types, validate_biological_type, validate_vm_type
from .resource_manager import BioResourceManager
from .config_manager import ConfigManager

# Public API exports (mirrors pylua exports)
__all__ = [
    # Core VM classes
    'BiologicalVM',
    'BasicBiologicalVM', 
    'XCPngBiologicalVM',
    
    # Factory functions
    'create_bio_vm',
    'create_biological_vm',  # Simplified interface
    'get_supported_biological_types',
    'get_supported_vm_types',
    'validate_biological_type',
    'validate_vm_type',
    
    # Management classes
    'BioResourceManager',
    'ConfigManager'
]

# Convenience functions (mirrors pylua convenience patterns)
def quick_start_vm(biological_type: str, vm_id: Optional[str] = None) -> BiologicalVM:
    """Quick start a basic biological VM with default settings."""
    vm_id = vm_id or f"quick_{biological_type}"
    return create_bio_vm(vm_id, biological_type)

# Alias for pylua compatibility
create_vm = create_bio_vm  # Alias for pylua compatibility
