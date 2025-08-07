# test_installation.py
from pylua_vm import VMManager, create_vm

print("Testing py-lua-vm installation...")

# Test basic VM creation
try:
    vm = create_vm("test_vm")
    result = vm.execute_string('print("Hello from Lua!")')
    print("✅ Basic VM:", result['stdout'])
except Exception as e:
    print("❌ Basic VM failed:", e)

# Test networked VM
try:
    net_vm = create_vm("net_vm", networked=True)
    print("✅ Networked VM created successfully")
except Exception as e:
    print("❌ Networked VM failed:", e)

# Test VM Manager
try:
    with VMManager() as manager:
        vm = manager.create_vm("managed_vm")
        result = manager.execute_vm_sync("managed_vm", 'return math.sqrt(16)')
        print("✅ VM Manager:", result['stdout'])
except Exception as e:
    print("❌ VM Manager failed:", e)

print("Installation test complete!")