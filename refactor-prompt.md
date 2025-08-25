# BioXen Interactive Refactoring Prompt

Please refactor the attached `interactive_bioxen.py` file to properly use `pylua_bioxen_vm_lib` v0.1.6 instead of the old `pylua_vm` library.

## Current Issues to Fix:

1. **Inconsistent Import**: Using old `from pylua_vm import VMManager` instead of new library
2. **Duplicate `create_lua_vm()` Methods**: Two different implementations causing conflicts
3. **Old VM Management Pattern**: Using outdated VMManager API calls
4. **Missing Modern Features**: No curator system, interactive sessions, or persistent VMs
5. **Missing Package Management**: No integration of the full package management system from the library

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

# REQUIRED: Full Package Management System
from pylua_bioxen_vm_lib.utils.curator import (
    Curator, get_curator, bootstrap_lua_environment, Package,
    PackageRegistry, DependencyResolver, PackageInstaller,
    PackageValidator, get_available_packages, search_packages
)
from pylua_bioxen_vm_lib.env import EnvironmentManager, LuaEnvironment
from pylua_bioxen_vm_lib.package_manager import (
    PackageManager, InstallationManager, RepositoryManager
)
```

### 2. **MANDATORY: Integrate Full Package Management System**

The curator and package management system from `pylua_bioxen_vm_lib` must be fully integrated into BioXen. This includes:

#### A. Add Package Management to Main Menu
**UPDATE the main menu to include comprehensive package management:**
```python
choices = [
    # Existing BioXen choices...
    Choice("🌙 Interactive Lua VM (One-shot)", "create_lua_vm"),
    Choice("🖥️  Persistent Lua VM", "create_persistent_vm"),
    Choice("🔗 Attach to Lua VM", "attach_lua_vm"),
    
    # REQUIRED: Package Management Menu Section
    Choice("📦 Package Management", "package_management_menu"),
    Choice("🔍 Search Lua Packages", "search_lua_packages"),
    Choice("📋 List Installed Packages", "list_installed_packages"),
    Choice("⬇️  Install Lua Package", "install_lua_package"),
    Choice("⬆️  Update Lua Package", "update_lua_package"),
    Choice("🗑️  Remove Lua Package", "remove_lua_package"),
    Choice("🔧 Manage Lua Environments", "manage_lua_environments"),
    Choice("🏗️  Bootstrap Lua Environment", "bootstrap_lua_environment"),
    
    # Existing choices...
]
```

#### B. Initialize Package Management in `__init__`
**MODIFY the `__init__` method:**
```python
def __init__(self):
    # Existing code...
    
    # REQUIRED: Initialize VM and Package Management
    self.vm_manager = VMManager()
    
    # Full Package Management System
    self.curator = get_curator()
    self.env_manager = EnvironmentManager()
    self.package_manager = PackageManager()
    self.installation_manager = InstallationManager()
    self.repository_manager = RepositoryManager()
    
    # Initialize package registry
    self.package_registry = PackageRegistry()
    self.dependency_resolver = DependencyResolver()
    self.package_installer = PackageInstaller()
    self.package_validator = PackageValidator()
```

#### C. **REQUIRED: Implement All Package Management Methods**

**ADD these comprehensive package management methods:**

```python
def package_management_menu(self):
    """Comprehensive package management menu"""
    choices = [
        Choice("🔍 Search Packages", "search_lua_packages"),
        Choice("📋 List Installed", "list_installed_packages"),
        Choice("⬇️  Install Package", "install_lua_package"),
        Choice("⬆️  Update Package", "update_lua_package"),
        Choice("🗑️  Remove Package", "remove_lua_package"),
        Choice("📊 Package Info", "package_info"),
        Choice("🔄 Update All Packages", "update_all_packages"),
        Choice("🏗️  Bootstrap Environment", "bootstrap_lua_environment"),
        Choice("🔧 Manage Environments", "manage_lua_environments"),
        Choice("⚙️  Package Settings", "package_settings"),
        Choice("🔙 Back to Main Menu", "main_menu")
    ]
    
    choice = questionary.select(
        "📦 Package Management",
        choices=choices
    ).ask()
    
    if choice and choice != "main_menu":
        getattr(self, choice)()

def search_lua_packages(self):
    """Search for available Lua packages"""
    query = questionary.text("🔍 Enter search query:").ask()
    if not query:
        return
    
    try:
        packages = search_packages(query)
        if packages:
            print(f"\n📦 Found {len(packages)} packages:")
            for pkg in packages:
                print(f"  • {pkg.name} ({pkg.version}) - {pkg.description}")
        else:
            print("❌ No packages found")
    except Exception as e:
        print(f"❌ Search error: {e}")

def install_lua_package(self):
    """Install a Lua package with dependency resolution"""
    package_name = questionary.text("📦 Package name to install:").ask()
    if not package_name:
        return
    
    # Optional version specification
    version = questionary.text("🏷️  Version (leave empty for latest):").ask()
    
    try:
        # Use the full package installation system
        if version:
            success = self.package_installer.install_package(package_name, version=version)
        else:
            success = self.package_installer.install_package(package_name)
        
        if success:
            print(f"✅ Package '{package_name}' installed successfully!")
        else:
            print(f"❌ Failed to install package '{package_name}'")
    except Exception as e:
        print(f"❌ Installation error: {e}")

def list_installed_packages(self):
    """List all installed packages"""
    try:
        packages = self.package_registry.get_installed_packages()
        if packages:
            print(f"\n📋 Installed Packages ({len(packages)}):")
            for pkg in packages:
                print(f"  • {pkg.name} ({pkg.version}) - {pkg.description}")
        else:
            print("📦 No packages installed")
    except Exception as e:
        print(f"❌ Error listing packages: {e}")

def update_lua_package(self):
    """Update a specific Lua package"""
    # Implementation for package updates
    # Show installed packages and allow selection for update
    pass

def remove_lua_package(self):
    """Remove an installed Lua package"""
    try:
        installed = self.package_registry.get_installed_packages()
        if not installed:
            print("📦 No packages installed")
            return
        
        choices = [Choice(f"{pkg.name} ({pkg.version})", pkg.name) for pkg in installed]
        package_name = questionary.select(
            "🗑️  Select package to remove:",
            choices=choices
        ).ask()
        
        if package_name:
            success = self.package_installer.remove_package(package_name)
            if success:
                print(f"✅ Package '{package_name}' removed successfully!")
            else:
                print(f"❌ Failed to remove package '{package_name}'")
    except Exception as e:
        print(f"❌ Error removing package: {e}")

def bootstrap_lua_environment(self):
    """Bootstrap a new Lua environment with essential packages"""
    env_name = questionary.text("🏗️  Environment name:").ask()
    if not env_name:
        return
    
    try:
        # Use the curator system to bootstrap
        success = bootstrap_lua_environment(env_name)
        if success:
            print(f"✅ Lua environment '{env_name}' bootstrapped successfully!")
        else:
            print(f"❌ Failed to bootstrap environment '{env_name}'")
    except Exception as e:
        print(f"❌ Bootstrap error: {e}")

def manage_lua_environments(self):
    """Manage Lua environments"""
    try:
        environments = self.env_manager.list_environments()
        
        choices = [
            Choice("🆕 Create New Environment", "create_env"),
            Choice("🔄 Switch Environment", "switch_env"),
            Choice("📋 List Environments", "list_env"),
            Choice("🗑️  Delete Environment", "delete_env"),
            Choice("🔙 Back", "back")
        ]
        
        action = questionary.select(
            "🔧 Environment Management:",
            choices=choices
        ).ask()
        
        # Implement environment management actions
        # (Full implementation would include create, switch, list, delete)
        
    except Exception as e:
        print(f"❌ Environment management error: {e}")
```

### 3. Consolidate Duplicate `create_lua_vm()` Methods
There are TWO different `create_lua_vm()` methods in the file:
- One at line ~47 (using old vm_manager import)
- One at line ~567 (using VMManager context manager)

**SOLUTION**: Keep only ONE method and update it to use the new library patterns with package management integration.

### 4. **Enhanced VM Creation with Package Management**

**REPLACE the entire `create_lua_vm()` method with this implementation:**
```python
def create_lua_vm(self):
    """Create a one-shot interactive Lua VM with package management (modernized for v0.1.6)"""
    print("\n🌙 Interactive Lua VM (One-shot)")
    print("💡 Creates a temporary VM that exits when you're done")
    print("💡 For persistent VMs, use 'Persistent Lua VM' option")
    print("📦 All installed packages are available in this session")
    print("-" * 70)
    
    # REQUIRED: Ask about package environment
    use_packages = questionary.confirm(
        "📦 Load installed packages in this VM?"
    ).ask()
    
    try:
        with self.vm_manager.create_interactive_session() as session:
            # REQUIRED: Initialize package environment if requested
            if use_packages:
                try:
                    # Load all installed packages into the VM
                    installed_packages = self.package_registry.get_installed_packages()
                    for package in installed_packages:
                        session.load_package(package.name)
                    print(f"📦 Loaded {len(installed_packages)} packages")
                except Exception as e:
                    print(f"⚠️ Warning: Could not load some packages: {e}")
            
            print("✅ Lua VM created successfully!")
            print("💡 Type 'exit' or press Ctrl+D to end session")
            print("💡 All standard Lua libraries available")
            if use_packages:
                print("📦 Installed packages loaded and ready to use")
            print("-" * 50)
            session.interactive_loop()
            print("👋 Lua session ended")
            
    except KeyboardInterrupt:
        print("\n⚠️ Session interrupted by user")
    except Exception as e:
        print(f"❌ Error in Lua session: {e}")
```

### 5. Update VM Lifecycle Patterns

**REPLACE the old patterns:**
```python
vm_manager = VMManager()
output, error = vm_manager.run_server(port=int(port))
output, error = vm_manager.run_code(lua_code)
```

**WITH new patterns that include package management:**
```python
# For one-shot VMs with packages:
with self.vm_manager.create_interactive_session() as session:
    # Load required packages
    for package in self.package_registry.get_installed_packages():
        session.load_package(package.name)
    session.interactive_loop()

# For persistent VMs with package environments:
session = self.vm_manager.create_interactive_vm(vm_id)
session.set_environment(environment_name)

# For networked VMs:
net_vm = NetworkedLuaVM(name=f"{vm_id}_net")
net_vm.load_packages_from_environment(env_name)
```

## Requirements Summary:
1. ✅ Fix inconsistent VMManager imports
2. ✅ Remove duplicate `create_lua_vm()` methods
3. ✅ Update to new library API patterns
4. ✅ **MANDATORY: Integrate complete package management system**
5. ✅ **MANDATORY: Add all curator and package manager features**
6. ✅ **MANDATORY: Provide comprehensive package management UI**
7. ✅ Maintain existing BioXen functionality
8. ✅ Keep questionary-based interactive UI
9. ✅ Add modern VM management capabilities
10. ✅ Proper error handling with new exception types
11. ✅ **MANDATORY: Package-aware VM sessions**
12. ✅ **MANDATORY: Environment management integration**

## CRITICAL: Package Management Integration is Required, Not Optional

The package management system is a core feature that must be fully integrated:

- **Search and Discovery**: Users must be able to search for available Lua packages
- **Installation Management**: Full install/update/remove functionality with dependency resolution
- **Environment Management**: Create, switch, and manage different Lua environments
- **Package Registry**: Track installed packages and their dependencies
- **VM Integration**: Load packages automatically in VM sessions
- **Bootstrap Capabilities**: Set up complete Lua environments with essential packages

## Additional Requirements:

### Error Handling
**USE the new exception types throughout:**
```python
except (VMManagerError, LuaVMError) as e:
    print(f"❌ VM Error: {e}")
except InteractiveSessionError as e:
    print(f"❌ Session Error: {e}")
except (PackageInstaller.InstallationError, PackageValidator.ValidationError) as e:
    print(f"📦 Package Error: {e}")
```

### Preserve All Existing BioXen Functionality
- Keep all hypervisor methods unchanged
- Keep all genome management methods unchanged  
- Keep all questionary-based UI interactions
- Only enhance with modern VM and package management

The refactored code should maintain the exact same user experience for BioXen features while providing modern, robust Lua VM management AND comprehensive package management using the new `pylua_bioxen_vm_lib` v0.1.6.