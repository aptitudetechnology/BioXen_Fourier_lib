# BioXen Interactive Refactoring Prompt

Please refactor the attached `interactive_bioxen.py` file to properly use `pylua_bioxen_vm_lib` v0.1.6 instead of the old `pylua_vm` library.

## Current Issues to Fix:

1. **Inconsistent Import**: Using old `from pylua_vm import VMManager` instead of new library
2. **Duplicate `create_lua_vm()` Methods**: Two different implementations causing conflicts
3. **Old VM Management Pattern**: Using outdated VMManager API calls
4. **Missing Modern Features**: No curator system, interactive sessions, or persistent VMs

## Required Changes:

### 1. Update Import Section
**REPLACE this:**
```python
from pylua_vm import VMManager
```

**WITH this:**
```python
# New v0.1.6 imports
from pylua_bioxen_vm_lib import VMManager, InteractiveSession, SessionManager
from pylua_bioxen_vm_lib.vm_manager import VMCluster
from pylua_bioxen_vm_lib.networking import NetworkedLuaVM, validate_host, validate_port
from pylua_bioxen_vm_lib.lua_process import LuaProcess
from pylua_bioxen_vm_lib.exceptions import (
    InteractiveSessionError, AttachError, DetachError, 
    SessionNotFoundError, SessionAlreadyExistsError, 
    VMManagerError, ProcessRegistryError, LuaProcessError,
    NetworkingError, LuaVMError
)
# Optional: Add curator system for package management
from pylua_bioxen_vm_lib.utils.curator import (
    Curator, get_curator, bootstrap_lua_environment, Package
)
from pylua_bioxen_vm_lib.env import EnvironmentManager
```

### 2. Consolidate Duplicate `create_lua_vm()` Methods
There are TWO different `create_lua_vm()` methods in the file:
- One at line ~47 (using old vm_manager import)
- One at line ~567 (using VMManager context manager)

**SOLUTION**: Keep only ONE method and update it to use the new library patterns.

### 3. Update VM Lifecycle Patterns

**REPLACE the old patterns:**
```python
vm_manager = VMManager()
output, error = vm_manager.run_server(port=int(port))
output, error = vm_manager.run_code(lua_code)
```

**WITH new patterns:**
```python
# For one-shot VMs:
with self.vm_manager.create_interactive_session() as session:
    session.interactive_loop()

# For persistent VMs:
session = self.vm_manager.create_interactive_vm(vm_id)

# For networked VMs:
net_vm = NetworkedLuaVM(name=f"{vm_id}_net")
```

### 4. Initialize VM Manager in `__init__`
**ADD to the `__init__` method:**
```python
def __init__(self):
    # Existing code...
    self.vm_manager = VMManager()  # Add this line
    
    # Optional: Add curator system
    self.curator = get_curator()
    self.env_manager = EnvironmentManager()
```

### 5. Update the Menu Choices
**MODIFY the main menu to include modern VM management options:**
```python
choices = [
    # Existing BioXen choices...
    Choice("🌙 Interactive Lua VM (One-shot)", "create_lua_vm"),
    Choice("🖥️  Persistent Lua VM", "create_persistent_vm"),  # New option
    Choice("🔗 Attach to Lua VM", "attach_lua_vm"),           # New option
    # Existing choices...
]
```

### 6. Refactor `create_lua_vm()` Method
**REPLACE the entire method with this modern implementation:**
```python
def create_lua_vm(self):
    """Create a one-shot interactive Lua VM (modernized for v0.1.6)"""
    print("\n🌙 Interactive Lua VM (One-shot)")
    print("💡 Creates a temporary VM that exits when you're done")
    print("💡 For persistent VMs, use 'Persistent Lua VM' option")
    print("-" * 70)
    
    try:
        with self.vm_manager.create_interactive_session() as session:
            print("✅ Lua VM created successfully!")
            print("💡 Type 'exit' or press Ctrl+D to end session")
            print("💡 All standard Lua libraries available")
            print("-" * 50)
            session.interactive_loop()
            print("👋 Lua session ended")
    except KeyboardInterrupt:
        print("\n⚠️ Session interrupted by user")
    except Exception as e:
        print(f"❌ Error in Lua session: {e}")
```

### 7. Add New Persistent VM Methods
**ADD these new methods to the class:**
```python
def create_persistent_vm(self):
    """Create a persistent Lua VM"""
    vm_id = questionary.text("Enter VM ID:").ask()
    if not vm_id:
        return
        
    try:
        session = self.vm_manager.create_interactive_vm(vm_id)
        print(f"✅ Persistent VM '{vm_id}' created!")
        print("💡 Use 'Attach to Lua VM' to interact with it")
    except Exception as e:
        print(f"❌ Failed to create persistent VM: {e}")

def attach_lua_vm(self):
    """Attach to an existing persistent VM"""
    # Implementation for attaching to VMs
    # (You can reference the enhanced example for full implementation)
```

### 8. Remove Old VM Manager Import Reference
**DELETE or COMMENT OUT this import in the `create_lua_vm()` method:**
```python
# DELETE THIS LINE:
from vm_manager import VMManager
```

### 9. Update Error Handling
**USE the new exception types:**
```python
except (VMManagerError, LuaVMError) as e:
    print(f"❌ VM Error: {e}")
except InteractiveSessionError as e:
    print(f"❌ Session Error: {e}")
```

### 10. Preserve All Existing BioXen Functionality
- Keep all hypervisor methods unchanged
- Keep all genome management methods unchanged  
- Keep all questionary-based UI interactions
- Only modify the Lua VM portions

## Requirements Summary:
1. ✅ Fix inconsistent VMManager imports
2. ✅ Remove duplicate `create_lua_vm()` methods
3. ✅ Update to new library API patterns
4. ✅ Maintain existing BioXen functionality
5. ✅ Keep questionary-based interactive UI
6. ✅ Add modern VM management capabilities
7. ✅ Proper error handling with new exception types

## Optional Enhancements:
- Add curator system for Lua package management
- Add persistent VM tracking with status display
- Add VM attachment/detachment capabilities

The refactored code should maintain the exact same user experience for BioXen features while providing modern, robust Lua VM management using the new `pylua_bioxen_vm_lib` v0.1.6.