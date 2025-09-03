#!/usr/bin/env python3
"""
BioXen Factory Pattern API - Phase 1 Demonstration Script

This script demonstrates the basic functionality of the Phase 1 implementation.
"""

import sys
import os

# Add the src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from src.api import create_bio_vm, get_supported_biological_types, get_supported_vm_types
    from src.api import BioResourceManager, ConfigManager
    print("✅ Successfully imported BioXen Factory Pattern API")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("Note: This is expected if hypervisor dependencies are not available")
    sys.exit(1)

def demonstrate_api():
    """Demonstrate Phase 1 API functionality"""
    
    print("\n🧬 BioXen Factory Pattern API - Phase 1 Demo")
    print("=" * 50)
    
    # Show supported types
    print(f"Supported biological types: {get_supported_biological_types()}")
    print(f"Supported VM types: {get_supported_vm_types()}")
    
    print("\n📋 Configuration Examples:")
    
    # Show default configurations
    for bio_type in get_supported_biological_types():
        config = ConfigManager.load_defaults(bio_type)
        print(f"{bio_type}: {config}")
    
    print("\n🔧 Basic VM Creation Demo:")
    
    try:
        # Create basic VMs for each biological type
        for bio_type in get_supported_biological_types():
            print(f"\nCreating basic {bio_type} VM...")
            vm = create_bio_vm(f"demo_{bio_type}", bio_type, "basic")
            print(f"  ✅ Created VM: {vm.vm_id}")
            print(f"  📊 VM Type: {vm.get_vm_type()}")
            print(f"  🧬 Biological Type: {vm.get_biological_type()}")
            
            # Demonstrate resource manager
            rm = BioResourceManager(vm)
            print(f"  💾 Resource Manager attached")
            
    except Exception as e:
        print(f"  ❌ VM creation failed: {e}")
        print("  Note: This is expected without hypervisor backend")
    
    print("\n🔒 XCP-ng VM Demo (Placeholder):")
    
    try:
        # Demonstrate XCP-ng VM creation
        xcpng_config = {
            "xcpng_config": {
                "xapi_url": "https://demo-xcpng:443",
                "username": "root",
                "password": "demo_password",
                "ssh_user": "bioxen"
            }
        }
        
        vm = create_bio_vm("demo_xcpng", "syn3a", "xcpng", xcpng_config)
        print(f"  ✅ Created XCP-ng VM: {vm.vm_id}")
        print(f"  📊 VM Type: {vm.get_vm_type()}")
        print(f"  🧬 Biological Type: {vm.get_biological_type()}")
        
        # Try to start (should raise NotImplementedError in Phase 1)
        try:
            vm.start()
        except NotImplementedError as e:
            print(f"  ⏸️ Start method: {e}")
        
    except Exception as e:
        print(f"  ❌ XCP-ng VM creation failed: {e}")
    
    print("\n✅ Phase 1 API demonstration complete!")
    print("🔄 Ready for Phase 2 (XCP-ng integration) implementation")

if __name__ == "__main__":
    demonstrate_api()
