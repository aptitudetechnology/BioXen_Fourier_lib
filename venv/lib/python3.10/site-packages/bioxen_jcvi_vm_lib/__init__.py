"""
BioXen JCVI VM Library - Production-ready biological VM management

This library provides a factory pattern API for creating and managing biological VMs,
following patterns from the successful pylua_bioxen_vm_lib implementation.
"""

__version__ = "0.0.07"
__author__ = "aptitudetechnology"
__email__ = "support@aptitudetechnology.com"

# Core API imports - following pylua_bioxen_vm_lib pattern
try:
    from .api.factory import create_bio_vm, get_supported_biological_types, get_supported_vm_types
    from .api.biological_vm import BiologicalVM
    from .api.resource_manager import BioResourceManager
    
    # Main factory function (mirrors pylua_bioxen_vm_lib.create_vm)
    create_vm = create_bio_vm
    
    __all__ = [
        'create_bio_vm',
        'create_vm',  # Alias for pylua compatibility
        'BiologicalVM', 
        'BioResourceManager',
        'get_supported_biological_types',
        'get_supported_vm_types'
    ]
    
except ImportError as e:
    # Graceful degradation when dependencies aren't available
    print(f"⚠️ BioXen JCVI VM library imports partially unavailable: {e}")
    print("💡 Some features may not work. Check installation.")
    
    # Provide minimal interface
    __all__ = []

# Version info
def get_version():
    """Get library version."""
    return __version__

def get_info():
    """Get library information."""
    return {
        'name': 'bioxen-jcvi-vm-lib',
        'version': __version__,
        'author': __author__,
        'email': __email__,
        'description': 'BioXen biological VM management library'
    }
