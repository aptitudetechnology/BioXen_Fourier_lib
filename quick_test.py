#!/usr/bin/env python3
"""
Quick test to isolate the .name attribute error
"""

import sys
sys.path.insert(0, 'src')

try:
    print("Testing imports...")
    from src.api import create_biological_vm
    print("✅ Imports successful")
    
    print("Testing VM creation...")
    vm = create_biological_vm(vm_type="basic")
    print("✅ VM creation successful")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
