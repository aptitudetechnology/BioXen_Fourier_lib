# BioXen_jcvi_vm_lib Factory Pattern API - Phase 3: Production Readiness

## Phase 3 Overview: CLI Integration & Production Deployment (Weeks 5-6)

**Objective**: Complete CLI integration, production deployment features, comprehensive documentation, and final validation for production readiness.

**Duration**: 2 weeks
**Priority**: Production deployment preparation
**Dependencies**: Phase 1 & 2 complete

---

## Week 5: CLI Integration & Advanced Features

### Day 29-31: CLI Integration with Existing Tools

#### Enhanced CLI Integration
```python
# src/cli/bioxen_factory_cli.py
import argparse
import json
import sys
from typing import Dict, Any, Optional
from ..api import create_bio_vm, get_supported_biological_types, get_supported_vm_types
from ..api import BioResourceManager, ConfigManager
from ..api.performance import performance_monitor

class BioXenFactoryCLI:
    """
    Enhanced CLI for BioXen Factory Pattern API.
    Integrates with existing interactive_bioxen.py functionality.
    """
    
    def __init__(self):
        self.active_vms = {}
        self.config_manager = ConfigManager()
    
    def run(self, args: Optional[list] = None) -> int:
        """Main CLI entry point."""
        parser = self.create_parser()
        parsed_args = parser.parse_args(args)
        
        try:
            return parsed_args.func(parsed_args)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    def create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser for CLI."""
        parser = argparse.ArgumentParser(
            description="BioXen Factory Pattern API CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # VM creation commands
        self._add_create_parser(subparsers)
        self._add_list_parser(subparsers)
        self._add_start_parser(subparsers)
        self._add_stop_parser(subparsers)
        self._add_destroy_parser(subparsers)
        
        # Resource management commands
        self._add_resources_parser(subparsers)
        self._add_monitor_parser(subparsers)
        self._add_optimize_parser(subparsers)
        
        # Configuration commands
        self._add_config_parser(subparsers)
        self._add_validate_parser(subparsers)
        
        # Integration commands
        self._add_interactive_parser(subparsers)
        self._add_performance_parser(subparsers)
        
        return parser
    
    def _add_create_parser(self, subparsers):
        """Add VM creation command parser."""
        create_parser = subparsers.add_parser('create', help='Create a new biological VM')
        create_parser.add_argument('vm_id', help='Unique VM identifier')
        create_parser.add_argument('biological_type', 
                                 choices=get_supported_biological_types(),
                                 help='Biological organism type')
        create_parser.add_argument('--vm-type', '-t',
                                 choices=get_supported_vm_types(),
                                 default='basic',
                                 help='VM infrastructure type (default: basic)')
        create_parser.add_argument('--config', '-c',
                                 help='Configuration file path')
        create_parser.add_argument('--auto-start', action='store_true',
                                 help='Automatically start VM after creation')
        create_parser.set_defaults(func=self.cmd_create)
    
    def _add_interactive_parser(self, subparsers):
        """Add interactive mode parser."""
        interactive_parser = subparsers.add_parser('interactive', 
                                                 help='Start interactive session')
        interactive_parser.add_argument('--integrate-existing', action='store_true',
                                      help='Integrate with existing interactive_bioxen.py')
        interactive_parser.set_defaults(func=self.cmd_interactive)
    
    def cmd_create(self, args) -> int:
        """Create VM command implementation."""
        try:
            # Load configuration if provided
            config = {}
            if args.config:
                config = self.config_manager.load_from_file(args.config)
                
                # Validate configuration
                is_valid, errors = self.config_manager.validate_config(
                    config, args.vm_type, args.biological_type
                )
                if not is_valid:
                    print("Configuration validation failed:")
                    for error in errors:
                        print(f"  - {error}")
                    return 1
            
            # Create VM
            vm = create_bio_vm(args.vm_id, args.biological_type, args.vm_type, config)
            self.active_vms[args.vm_id] = vm
            
            print(f"Created {args.biological_type} VM '{args.vm_id}' with {args.vm_type} infrastructure")
            
            # Auto-start if requested
            if args.auto_start:
                if vm.start():
                    print(f"Started VM '{args.vm_id}'")
                else:
                    print(f"Failed to start VM '{args.vm_id}'")
                    return 1
            
            return 0
            
        except Exception as e:
            print(f"Failed to create VM: {e}")
            return 1
    
    def cmd_interactive(self, args) -> int:
        """Start interactive session."""
        if args.integrate_existing:
            return self._integrate_with_existing_interactive()
        else:
            return self._start_factory_interactive()
    
    def _integrate_with_existing_interactive(self) -> int:
        """Integrate with existing interactive_bioxen.py."""
        try:
            # Import existing interactive module
            from ..interactive_bioxen import InteractiveBioXen
            
            # Create enhanced interactive session
            interactive = EnhancedInteractiveBioXen()
            interactive.run()
            return 0
            
        except ImportError:
            print("Could not import existing interactive_bioxen module")
            return 1
    
    def _start_factory_interactive(self) -> int:
        """Start factory-specific interactive session."""
        print("BioXen Factory Pattern API - Interactive Mode")
        print("Type 'help' for available commands, 'exit' to quit")
        
        while True:
            try:
                command = input("bioxen-factory> ").strip()
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit']:
                    break
                elif command.lower() == 'help':
                    self._show_interactive_help()
                else:
                    self._execute_interactive_command(command)
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break
        
        return 0
    
    def _show_interactive_help(self):
        """Show interactive help."""
        help_text = """
Available commands:
  create <vm_id> <bio_type> [vm_type]  - Create new VM
  list                                 - List active VMs  
  start <vm_id>                       - Start VM
  stop <vm_id>                        - Stop VM
  status <vm_id>                      - Show VM status
  resources <vm_id>                   - Show resource usage
  execute <vm_id> <code>              - Execute biological process
  config template <bio_type> <vm_type> - Generate config template
  performance                         - Show performance metrics
  help                                - Show this help
  exit                                - Exit interactive mode
        """
        print(help_text)
    
    def _execute_interactive_command(self, command: str):
        """Execute interactive command."""
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        
        if cmd == 'create' and len(parts) >= 3:
            vm_id = parts[1]
            bio_type = parts[2]
            vm_type = parts[3] if len(parts) > 3 else 'basic'
            
            try:
                vm = create_bio_vm(vm_id, bio_type, vm_type)
                self.active_vms[vm_id] = vm
                print(f"Created {bio_type} VM '{vm_id}' ({vm_type})")
            except Exception as e:
                print(f"Error creating VM: {e}")
        
        elif cmd == 'list':
            if self.active_vms:
                for vm_id, vm in self.active_vms.items():
                    print(f"{vm_id}: {vm.get_biological_type()} ({vm.get_vm_type()})")
            else:
                print("No active VMs")
        
        elif cmd == 'start' and len(parts) >= 2:
            vm_id = parts[1]
            if vm_id in self.active_vms:
                if self.active_vms[vm_id].start():
                    print(f"Started VM '{vm_id}'")
                else:
                    print(f"Failed to start VM '{vm_id}'")
            else:
                print(f"VM '{vm_id}' not found")
        
        elif cmd == 'performance':
            metrics = performance_monitor.get_summary()
            print(f"Total operations: {metrics['total_operations']}")
            print(f"Success rate: {metrics['success_rate']:.2%}")
            print(f"Total time: {metrics['total_time']:.2f}s")
        
        else:
            print(f"Unknown command: {cmd}")

class EnhancedInteractiveBioXen:
    """
    Enhanced interactive BioXen that integrates factory pattern API
    with existing interactive_bioxen.py functionality.
    """
    
    def __init__(self):
        self.factory_cli = BioXenFactoryCLI()
        self.legacy_interactive = None
        
        # Try to import existing interactive module
        try:
            from ..interactive_bioxen import InteractiveBioXen
            self.legacy_interactive = InteractiveBioXen()
        except ImportError:
            print("Warning: Could not import existing interactive_bioxen module")
    
    def run(self):
        """Run enhanced interactive session."""
        print("Enhanced BioXen Interactive Session")
        print("Factory Pattern API + Legacy Functionality")
        print("Type 'help' for commands, 'factory' for factory commands, 'exit' to quit")
        
        while True:
            try:
                command = input("bioxen> ").strip()
                if not command:
                    continue
                
                if command.lower() in ['exit', 'quit']:
                    break
                elif command.lower() == 'factory':
                    print("Switching to factory mode (type 'back' to return)")
                    self._factory_mode()
                elif command.lower().startswith('factory '):
                    # Direct factory command
                    factory_command = command[8:]  # Remove 'factory '
                    self.factory_cli._execute_interactive_command(factory_command)
                elif self.legacy_interactive:
                    # Delegate to legacy interactive
                    self._execute_legacy_command(command)
                else:
                    print("Legacy interactive not available. Use 'factory' commands.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break
    
    def _factory_mode(self):
        """Enter factory-specific mode."""
        while True:
            try:
                command = input("bioxen-factory> ").strip()
                if command.lower() == 'back':
                    break
                elif command.lower() in ['exit', 'quit']:
                    return  # Exit entire session
                else:
                    self.factory_cli._execute_interactive_command(command)
            except KeyboardInterrupt:
                break
    
    def _execute_legacy_command(self, command: str):
        """Execute legacy interactive command."""
        # This would integrate with existing interactive_bioxen.py
        # Implementation depends on existing interactive module structure
        print(f"Legacy command: {command}")

# CLI entry point
def main():
    """Main CLI entry point."""
    cli = BioXenFactoryCLI()
    return cli.run()

if __name__ == "__main__":
    sys.exit(main())
```

#### Integration with Existing CLI
```python
# Update to existing interactive_bioxen.py
def integrate_factory_api():
    """Integration function to add factory API to existing interactive."""
    try:
        from .api import create_bio_vm, get_supported_biological_types
        from .cli.bioxen_factory_cli import BioXenFactoryCLI
        
        # Add factory commands to existing interactive
        print("Factory Pattern API integration available")
        print("Use 'factory <command>' to access new API")
        
        return BioXenFactoryCLI()
    except ImportError:
        return None

# Add to existing command handlers
def handle_factory_command(self, command_parts):
    """Handle factory pattern API commands in existing interactive."""
    if not hasattr(self, 'factory_cli'):
        self.factory_cli = integrate_factory_api()
        if not self.factory_cli:
            print("Factory API not available")
            return
    
    factory_command = ' '.join(command_parts[1:])  # Remove 'factory' prefix
    self.factory_cli._execute_interactive_command(factory_command)
```

### Day 32-33: Production Features

#### Production Configuration Management
```python
# src/api/production.py
import os
import logging
import json
from typing import Dict, Any, Optional
from pathlib import Path

class ProductionConfigManager:
    """Production-specific configuration management."""
    
    def __init__(self):
        self.environment = os.getenv('BIOXEN_ENV', 'development')
        self.config_dir = Path(os.getenv('BIOXEN_CONFIG_DIR', '/etc/bioxen'))
        self.log_dir = Path(os.getenv('BIOXEN_LOG_DIR', '/var/log/bioxen'))
        
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup production logging."""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        log_level = os.getenv('BIOXEN_LOG_LEVEL', 'INFO')
        log_file = self.log_dir / 'bioxen_api.log'
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('bioxen_api')
    
    def load_production_config(self) -> Dict[str, Any]:
        """Load production configuration."""
        config_file = self.config_dir / f'bioxen_{self.environment}.json'
        
        if not config_file.exists():
            self.logger.warning(f"Production config not found: {config_file}")
            return self._create_default_production_config()
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        # Validate production config
        self._validate_production_config(config)
        return config
    
    def _create_default_production_config(self) -> Dict[str, Any]:
        """Create default production configuration."""
        default_config = {
            "environment": self.environment,
            "api": {
                "max_concurrent_vms": 100,
                "default_vm_type": "basic",
                "enable_performance_monitoring": True,
                "enable_resource_monitoring": True
            },
            "security": {
                "enable_audit_logging": True,
                "require_authentication": True,
                "max_session_duration": 3600
            },
            "resources": {
                "global_atp_limit": 1000.0,
                "global_ribosome_limit": 500,
                "enable_resource_quotas": True
            },
            "xcpng": {
                "connection_pool_size": 10,
                "ssh_timeout": 30,
                "vm_creation_timeout": 300
            }
        }
        
        # Save default config
        self.config_dir.mkdir(parents=True, exist_ok=True)
        config_file = self.config_dir / f'bioxen_{self.environment}.json'
        with open(config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        self.logger.info(f"Created default production config: {config_file}")
        return default_config
    
    def _validate_production_config(self, config: Dict[str, Any]):
        """Validate production configuration."""
        required_sections = ['api', 'security', 'resources']
        for section in required_sections:
            if section not in config:
                raise ValueError(f"Missing required config section: {section}")
        
        # Validate API limits
        api_config = config['api']
        if api_config.get('max_concurrent_vms', 0) <= 0:
            raise ValueError("max_concurrent_vms must be positive")
        
        # Validate resource limits
        resources_config = config['resources']
        if resources_config.get('global_atp_limit', 0) <= 0:
            raise ValueError("global_atp_limit must be positive")

class ProductionVMManager:
    """Production VM management with quotas and monitoring."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.active_vms = {}
        self.vm_quotas = {}
        self.logger = logging.getLogger('bioxen_api.vm_manager')
        
        # Initialize resource tracking
        self.global_atp_used = 0.0
        self.global_ribosomes_used = 0
        self.max_concurrent_vms = config['api']['max_concurrent_vms']
        
    def create_vm_with_quotas(self, vm_id: str, biological_type: str, 
                            vm_type: str = "basic", config: Optional[Dict] = None,
                            user_id: Optional[str] = None) -> Dict[str, Any]:
        """Create VM with production quotas and limits."""
        
        # Check VM limits
        if len(self.active_vms) >= self.max_concurrent_vms:
            raise ValueError(f"Maximum concurrent VMs reached: {self.max_concurrent_vms}")
        
        # Check user quotas
        if user_id and self._check_user_quota(user_id):
            raise ValueError(f"User {user_id} has exceeded VM quota")
        
        # Create VM
        from ..api import create_bio_vm
        vm = create_bio_vm(vm_id, biological_type, vm_type, config)
        
        # Track VM
        self.active_vms[vm_id] = {
            'vm': vm,
            'user_id': user_id,
            'created_at': time.time(),
            'biological_type': biological_type,
            'vm_type': vm_type
        }
        
        # Update user quota
        if user_id:
            self._update_user_quota(user_id, 1)
        
        self.logger.info(f"Created VM {vm_id} for user {user_id}")
        
        return {
            'vm_id': vm_id,
            'status': 'created',
            'biological_type': biological_type,
            'vm_type': vm_type
        }
    
    def _check_user_quota(self, user_id: str) -> bool:
        """Check if user has exceeded VM quota."""
        user_vms = sum(1 for vm_info in self.active_vms.values() 
                      if vm_info['user_id'] == user_id)
        max_vms_per_user = self.config.get('security', {}).get('max_vms_per_user', 10)
        return user_vms >= max_vms_per_user
    
    def _update_user_quota(self, user_id: str, delta: int):
        """Update user quota tracking."""
        if user_id not in self.vm_quotas:
            self.vm_quotas[user_id] = 0
        self.vm_quotas[user_id] += delta
    
    def get_production_status(self) -> Dict[str, Any]:
        """Get production system status."""
        return {
            'active_vms': len(self.active_vms),
            'max_concurrent_vms': self.max_concurrent_vms,
            'global_atp_used': self.global_atp_used,
            'global_ribosomes_used': self.global_ribosomes_used,
            'vm_types': {
                'basic': sum(1 for vm in self.active_vms.values() if vm['vm_type'] == 'basic'),
                'xcpng': sum(1 for vm in self.active_vms.values() if vm['vm_type'] == 'xcpng')
            },
            'biological_types': {
                bio_type: sum(1 for vm in self.active_vms.values() 
                            if vm['biological_type'] == bio_type)
                for bio_type in ['syn3a', 'ecoli', 'minimal_cell']
            }
        }

class AuditLogger:
    """Audit logging for production deployments."""
    
    def __init__(self, log_dir: Path):
        self.log_dir = log_dir
        self.audit_file = log_dir / 'audit.log'
        
        # Setup audit logger
        self.audit_logger = logging.getLogger('bioxen_audit')
        handler = logging.FileHandler(self.audit_file)
        formatter = logging.Formatter(
            '%(asctime)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.audit_logger.addHandler(handler)
        self.audit_logger.setLevel(logging.INFO)
    
    def log_vm_creation(self, vm_id: str, user_id: str, biological_type: str, vm_type: str):
        """Log VM creation event."""
        self.audit_logger.info(
            f"VM_CREATE - vm_id:{vm_id} user_id:{user_id} "
            f"biological_type:{biological_type} vm_type:{vm_type}"
        )
    
    def log_vm_operation(self, vm_id: str, user_id: str, operation: str, success: bool):
        """Log VM operation event."""
        status = "SUCCESS" if success else "FAILURE"
        self.audit_logger.info(
            f"VM_OPERATION - vm_id:{vm_id} user_id:{user_id} "
            f"operation:{operation} status:{status}"
        )
    
    def log_resource_allocation(self, vm_id: str, user_id: str, resource_type: str, amount: float):
        """Log resource allocation event."""
        self.audit_logger.info(
            f"RESOURCE_ALLOC - vm_id:{vm_id} user_id:{user_id} "
            f"resource:{resource_type} amount:{amount}"
        )
```

### Day 34-35: Comprehensive Documentation

#### Complete API Documentation
```markdown
# docs/api/complete-reference.md

# BioXen Factory Pattern API - Complete Reference

## Overview

The BioXen Factory Pattern API provides a unified interface for creating and managing biological virtual machines with support for multiple infrastructure types and organism configurations.

## Quick Start

### Basic Usage
```python
from src.api import create_bio_vm

# Create basic VM
vm = create_bio_vm("my_vm", "syn3a", "basic")
vm.start()

# Execute biological process
result = vm.execute_biological_process("start_transcription(['gene1', 'gene2'])")
print(result)

vm.destroy()
```

### XCP-ng Usage
```python
xcpng_config = {
    "xcpng_config": {
        "xapi_url": "https://xcpng-host:443",
        "username": "root",
        "password": "secure_password",
        "ssh_user": "root",
        "ssh_key_path": "/path/to/key"
    }
}

vm = create_bio_vm("isolated_vm", "ecoli", "xcpng", xcpng_config)
vm.start()
```

## Core API Reference

### Factory Functions

#### `create_bio_vm(vm_id, biological_type, vm_type="basic", config=None)`

Creates a new biological VM instance.

**Parameters:**
- `vm_id` (str): Unique identifier for the VM
- `biological_type` (str): Organism type - "syn3a", "ecoli", "minimal_cell"
- `vm_type` (str): Infrastructure type - "basic" or "xcpng" (default: "basic")
- `config` (dict, optional): Configuration dictionary

**Returns:** BiologicalVM instance

**Raises:**
- `ValueError`: Invalid biological_type or vm_type
- `ValueError`: XCP-ng type requires config

**Example:**
```python
# Basic VM
vm = create_bio_vm("test_vm", "syn3a")

# XCP-ng VM with config
vm = create_bio_vm("xcpng_vm", "ecoli", "xcpng", xcpng_config)
```

### BiologicalVM Class

Base class for all biological VMs.

#### Common Methods

##### `start() -> bool`
Start the biological VM.

##### `pause() -> bool` 
Pause the biological VM.

##### `resume() -> bool`
Resume a paused VM.

##### `destroy() -> bool`
Destroy the VM and cleanup resources.

##### `get_status() -> Dict[str, Any]`
Get current VM status and metrics.

##### `execute_biological_process(process_code: str) -> Dict[str, Any]`
Execute biological process code.

**Parameters:**
- `process_code` (str): Biological process code to execute

**Returns:** Dictionary with execution results

##### `install_biological_package(package_name: str) -> Dict[str, Any]`
Install biological analysis package.

##### `get_biological_metrics() -> Dict[str, Any]`
Get biological-specific metrics based on organism type.

#### Organism-Specific Methods

##### `start_transcription(gene_ids: List[str]) -> bool`
Start transcription of genes (Syn3A only).

##### `get_essential_genes() -> List[str]`
Get essential genes list (Syn3A only).

##### `manage_operons(operon_ids: List[str], action: str) -> bool`
Manage bacterial operons (E.coli only).

##### `get_plasmid_count() -> int`
Get number of plasmids (E.coli only).

### Resource Management

#### BioResourceManager Class

```python
from src.api import BioResourceManager

vm = create_bio_vm("resource_vm", "syn3a")
manager = BioResourceManager(vm, enable_monitoring=True)
```

##### `allocate_atp(percentage: float) -> bool`
Allocate ATP resources (0-100%).

##### `allocate_ribosomes(count: int) -> bool`
Allocate ribosomes for protein synthesis.

##### `get_resource_usage() -> Dict[str, Any]`
Get current resource usage statistics.

##### `start_monitoring(interval_seconds: int = 30) -> bool`
Start background resource monitoring.

##### `auto_optimize_resources() -> bool`
Automatically optimize resources based on VM type.

##### `get_optimization_recommendations() -> List[str]`
Get resource optimization recommendations.

### Configuration Management

#### ConfigManager Class

```python
from src.api import ConfigManager

# Load defaults
config = ConfigManager.load_defaults("syn3a")

# Validate configuration
is_valid, errors = ConfigManager.validate_config(config, "basic", "syn3a")
```

##### `load_defaults(biological_type: str) -> Dict[str, Any]`
Load default configuration for biological type.

##### `load_from_file(config_path: str = None) -> Dict[str, Any]`
Load configuration from file (auto-discovers if path not provided).

##### `validate_config(config: Dict, vm_type: str, biological_type: str) -> Tuple[bool, List[str]]`
Validate configuration and return validation results.

##### `generate_template_config(biological_type: str, vm_type: str) -> Dict[str, Any]`
Generate template configuration for specific VM and biological types.

## Configuration Reference

### Basic VM Configuration
```json
{
  "resource_limits": {
    "max_atp": 70.0,
    "max_ribosomes": 15,
    "memory_limit": "512MB"
  },
  "biological_settings": {
    "genome_optimization": true,
    "minimal_mode": true
  },
  "performance": {
    "enable_monitoring": true,
    "optimization_interval": 60
  }
}
```

### XCP-ng VM Configuration
```json
{
  "xcpng_config": {
    "xapi_url": "https://xcpng-host:443",
    "username": "root",
    "password": "secure_password",
    "template_name": "bioxen-bio-template",
    "ssh_user": "root",
    "ssh_key_path": "/path/to/ssh/key",
    "vm_memory": "4GB",
    "vm_vcpus": 4
  },
  "resource_limits": {
    "max_atp": 90.0,
    "max_ribosomes": 30
  }
}
```

## CLI Reference

### Installation
```bash
# Install BioXen API
pip install -e .

# Run CLI
python -m src.cli.bioxen_factory_cli --help
```

### Commands

#### VM Management
```bash
# Create VM
bioxen-factory create my_vm syn3a --vm-type basic --auto-start

# List VMs
bioxen-factory list

# Start VM
bioxen-factory start my_vm

# Stop VM  
bioxen-factory stop my_vm

# Get status
bioxen-factory status my_vm
```

#### Resource Management
```bash
# Show resources
bioxen-factory resources my_vm

# Start monitoring
bioxen-factory monitor my_vm --interval 30

# Optimize resources
bioxen-factory optimize my_vm
```

#### Configuration
```bash
# Validate config
bioxen-factory validate --config config.json --vm-type xcpng --bio-type ecoli

# Generate template
bioxen-factory config template syn3a xcpng > template.json
```

#### Interactive Mode
```bash
# Start interactive session
bioxen-factory interactive

# Integrate with existing interactive
bioxen-factory interactive --integrate-existing
```

## Error Handling

### Common Exceptions

#### `ValueError`
- Invalid biological_type or vm_type
- Missing required configuration for XCP-ng
- Invalid resource allocation values

#### `ConnectionError`
- XCP-ng XAPI connection failures
- SSH connection failures

#### `FileNotFoundError`
- Configuration file not found
- SSH key file not found

### Error Handling Best Practices

```python
from src.api import create_bio_vm

try:
    vm = create_bio_vm("test_vm", "syn3a", "xcpng", config)
    vm.start()
except ValueError as e:
    print(f"Configuration error: {e}")
except ConnectionError as e:
    print(f"Connection error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if 'vm' in locals():
        vm.destroy()
```

## Performance Considerations

### Resource Monitoring
- Enable monitoring only when needed
- Use appropriate monitoring intervals (30-60 seconds)
- Monitor resource usage to prevent bottlenecks

### XCP-ng VMs
- XCP-ng VMs have higher overhead due to SSH communication
- Use connection pooling for multiple operations
- Consider basic VMs for development and testing

### Optimization Tips
- Use auto-optimization for production workloads
- Monitor ATP and ribosome allocation
- Use resource snapshots for backup/restore

## Integration Examples

### With Existing Interactive
```python
# In existing interactive_bioxen.py
from src.cli.bioxen_factory_cli import BioXenFactoryCLI

def add_factory_commands(self):
    self.factory_cli = BioXenFactoryCLI()
    
def handle_factory_command(self, command):
    self.factory_cli._execute_interactive_command(command)
```

### With External Scripts
```python
#!/usr/bin/env python3
"""Example external script using BioXen API."""

from src.api import create_bio_vm, BioResourceManager

def run_biological_workflow():
    # Create VMs for different organisms
    syn3a_vm = create_bio_vm("workflow_syn3a", "syn3a")
    ecoli_vm = create_bio_vm("workflow_ecoli", "ecoli")
    
    try:
        # Start VMs
        syn3a_vm.start()
        ecoli_vm.start()
        
        # Execute parallel processes
        syn3a_result = syn3a_vm.execute_biological_process("minimal_metabolism_analysis()")
        ecoli_result = ecoli_vm.execute_biological_process("operon_expression_analysis()")
        
        # Compare results
        return compare_results(syn3a_result, ecoli_result)
        
    finally:
        syn3a_vm.destroy()
        ecoli_vm.destroy()

if __name__ == "__main__":
    results = run_biological_workflow()
    print(f"Workflow results: {results}")
```

## Troubleshooting

### Common Issues

#### VM Creation Fails
- Check biological_type and vm_type values
- Verify configuration for XCP-ng VMs
- Check resource availability

#### XCP-ng Connection Issues
- Verify XAPI URL and credentials
- Check SSH key permissions
- Ensure XCP-ng template exists

#### Resource Allocation Failures
- Check global resource limits
- Verify VM is started
- Monitor resource usage

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# API operations will now show debug information
vm = create_bio_vm("debug_vm", "syn3a", "basic")
```

### Performance Monitoring
```python
from src.api.performance import performance_monitor

# Get performance metrics
metrics = performance_monitor.get_summary()
print(f"Operations: {metrics['total_operations']}")
print(f"Success rate: {metrics['success_rate']:.2%}")
```
```

---

## Week 6: Final Testing & Production Deployment

### Day 36-37: Comprehensive Testing

#### Integration Test Suite
```python
# tests/test_integration/test_complete_system.py
import pytest
import tempfile
import time
from unittest.mock import Mock, patch

from src.api import create_bio_vm, BioResourceManager, ConfigManager
from src.cli.bioxen_factory_cli import BioXenFactoryCLI

class TestCompleteSystem:
    """Complete system integration tests."""
    
    def test_complete_workflow_basic(self):
        """Test complete workflow with basic VMs."""
        # Create VM
        vm = create_bio_vm("workflow_test", "syn3a", "basic")
        
        # Resource management
        manager = BioResourceManager(vm, enable_monitoring=True)
        
        try:
            # Start VM
            assert vm.start()
            
            # Allocate resources
            assert manager.allocate_atp(70.0)
            assert manager.allocate_ribosomes(12)
            
            # Start monitoring
            assert manager.start_monitoring(interval_seconds=1)
            time.sleep(2)  # Let monitoring run
            
            # Execute biological process
            result = vm.execute_biological_process("test_process()")
            assert isinstance(result, dict)
            
            # Get metrics
            metrics = vm.get_biological_metrics()
            assert isinstance(metrics, dict)
            
            # Auto-optimize
            assert manager.auto_optimize_resources()
            
            # Check monitoring data
            history = manager.get_resource_history()
            assert len(history) > 0
            
            # Stop monitoring
            assert manager.stop_monitoring()
            
        finally:
            vm.destroy()
    
    @patch('src.api.xcp_ng_integration.XAPIClient')
    @patch('src.api.xcp_ng_integration.SSHSession')
    def test_complete_workflow_xcpng(self, mock_ssh, mock_xapi):
        """Test complete workflow with XCP-ng VMs."""
        # Mock XCP-ng components
        mock_xapi_instance = Mock()
        mock_xapi.return_value = mock_xapi_instance
        mock_xapi_instance.login.return_value = True
        mock_xapi_instance.create_vm_from_template.return_value = "test-uuid"
        mock_xapi_instance.start_vm.return_value = True
        mock_xapi_instance.get_vm_ip.return_value = "192.168.1.100"
        
        mock_ssh_instance = Mock()
        mock_ssh.return_value = mock_ssh_instance
        mock_ssh_instance.connect.return_value = True
        mock_ssh_instance.execute_command.return_value = {
            'stdout': '{"status": "success"}',
            'stderr': '',
            'exit_code': 0
        }
        
        # XCP-ng configuration
        xcpng_config = {
            "xcpng_config": {
                "xapi_url": "https://test-xcpng:443",
                "username": "root",
                "password": "test_password",
                "ssh_user": "root",
                "ssh_key_path": "/tmp/test_key"
            }
        }
        
        # Create XCP-ng VM
        vm = create_bio_vm("xcpng_workflow_test", "ecoli", "xcpng", xcpng_config)
        
        try:
            # Start VM (will create XCP-ng VM)
            assert vm.start()
            
            # Execute biological process via SSH
            result = vm.execute_biological_process("test_ecoli_process()")
            assert isinstance(result, dict)
            
            # Install package via SSH
            install_result = vm.install_biological_package("test_package")
            assert isinstance(install_result, dict)
            
            # Get metrics via SSH
            metrics = vm.get_biological_metrics()
            assert isinstance(metrics, dict)
            
        finally:
            vm.destroy()
    
    def test_cli_integration(self):
        """Test CLI integration."""
        cli = BioXenFactoryCLI()
        
        # Test VM creation via CLI
        args = ['create', 'cli_test_vm', 'syn3a', '--vm-type', 'basic', '--auto-start']
        result = cli.run(args)
        assert result == 0
        
        # Test VM listing
        args = ['list']
        result = cli.run(args)
        assert result == 0
        
        # Test VM status
        args = ['status', 'cli_test_vm']
        result = cli.run(args)
        assert result == 0
    
    def test_config_management_integration(self):
        """Test configuration management integration."""
        # Generate template config
        config = ConfigManager.generate_template_config("ecoli", "xcpng")
        assert isinstance(config, dict)
        assert 'xcpng_config' in config
        
        # Save and load config
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = f.name
        
        assert ConfigManager.save_to_file(config, config_path, "json")
        loaded_config = ConfigManager.load_from_file(config_path)
        assert loaded_config == config
        
        # Validate config
        is_valid, errors = ConfigManager.validate_config(config, "xcpng", "ecoli")
        # May not be valid due to mock values, but should not crash
        assert isinstance(is_valid, bool)
        assert isinstance(errors, list)
        
        # Cleanup
        import os
        os.unlink(config_path)
    
    def test_performance_monitoring(self):
        """Test performance monitoring integration."""
        from src.api.performance import performance_monitor
        
        # Create and use VM to generate metrics
        vm = create_bio_vm("perf_test", "minimal_cell", "basic")
        
        try:
            vm.start()
            vm.execute_biological_process("test_process()")
            vm.get_status()
            vm.destroy()
            
            # Check performance metrics
            metrics = performance_monitor.get_metrics()
            assert isinstance(metrics, dict)
            
            summary = performance_monitor.get_summary()
            assert 'total_operations' in summary
            assert 'success_rate' in summary
            
        except Exception:
            # Ensure cleanup even if test fails
            vm.destroy()
            raise
    
    def test_production_features(self):
        """Test production-specific features."""
        from src.api.production import ProductionConfigManager, ProductionVMManager
        
        # Test production config
        prod_config_manager = ProductionConfigManager()
        config = prod_config_manager.load_production_config()
        assert isinstance(config, dict)
        
        # Test production VM manager
        vm_manager = ProductionVMManager(config)
        
        # Test VM creation with quotas
        result = vm_manager.create_vm_with_quotas(
            "prod_test_vm", "syn3a", "basic", None, "test_user"
        )
        assert result['status'] == 'created'
        
        # Test status
        status = vm_manager.get_production_status()
        assert 'active_vms' in status
        assert status['active_vms'] == 1
```

#### Load Testing
```python
# tests/test_performance/test_load.py
import pytest
import concurrent.futures
import time
from src.api import create_bio_vm

class TestLoadPerformance:
    """Load testing for production readiness."""
    
    def test_concurrent_vm_creation(self):
        """Test concurrent VM creation."""
        def create_test_vm(vm_id):
            try:
                vm = create_bio_vm(f"load_test_{vm_id}", "syn3a", "basic")
                vm.start()
                time.sleep(1)  # Simulate work
                vm.destroy()
                return True
            except Exception as e:
                print(f"VM {vm_id} failed: {e}")
                return False
        
        # Test creating 10 VMs concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(create_test_vm, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.9  # 90% success rate minimum
    
    def test_resource_allocation_load(self):
        """Test resource allocation under load."""
        vm = create_bio_vm("resource_load_test", "ecoli", "basic")
        
        try:
            vm.start()
            
            def allocate_resources(iteration):
                from src.api import BioResourceManager
                manager = BioResourceManager(vm)
                
                success = (
                    manager.allocate_atp(50.0 + (iteration % 40)) and
                    manager.allocate_ribosomes(10 + (iteration % 20))
                )
                return success
            
            # Perform 100 resource allocations
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(allocate_resources, i) for i in range(100)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            success_rate = sum(results) / len(results)
            assert success_rate >= 0.95  # 95% success rate for resource allocation
            
        finally:
            vm.destroy()
```

### Day 38-42: Production Deployment Preparation

#### Deployment Configuration
```yaml
# deployment/docker-compose.yml
version: '3.8'

services:
  bioxen-api:
    build: .
    ports:
      - "8080:8080"
    environment:
      - BIOXEN_ENV=production
      - BIOXEN_CONFIG_DIR=/app/config
      - BIOXEN_LOG_DIR=/app/logs
      - BIOXEN_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    
  bioxen-monitor:
    build: 
      context: .
      dockerfile: Dockerfile.monitor
    depends_on:
      - bioxen-api
    environment:
      - BIOXEN_ENV=production
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

networks:
  bioxen-network:
    driver: bridge
```

#### Production Dockerfile
```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY setup.py .

# Install package
RUN pip install -e .

# Create directories
RUN mkdir -p /app/config /app/logs /app/data

# Create non-root user
RUN useradd -m -u 1000 bioxen && chown -R bioxen:bioxen /app
USER bioxen

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD python -c "from src.api import create_bio_vm; vm = create_bio_vm('health_check', 'syn3a'); vm.destroy()" || exit 1

# Start application
CMD ["python", "-m", "src.cli.bioxen_factory_cli", "interactive"]
```

#### Installation Script
```bash
#!/bin/bash
# install.sh - Production installation script

set -e

echo "Installing BioXen Factory Pattern API..."

# Check Python version
python3 -c "import sys; assert sys.version_info >= (3, 7)" || {
    echo "Error: Python 3.7+ required"
    exit 1
}

# Create directories
sudo mkdir -p /etc/bioxen /var/log/bioxen /opt/bioxen
sudo chown $USER:$USER /var/log/bioxen /opt/bioxen

# Install package
pip3 install -e .

# Install system service
cat > bioxen-api.service << EOF
[Unit]
Description=BioXen Factory Pattern API
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/bioxen
Environment=BIOXEN_ENV=production
Environment=BIOXEN_CONFIG_DIR=/etc/bioxen
Environment=BIOXEN_LOG_DIR=/var/log/bioxen
ExecStart=/usr/local/bin/python3 -m src.cli.bioxen_factory_cli interactive
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

sudo mv bioxen-api.service /etc/systemd/system/
sudo systemctl daemon-reload

# Generate default configuration
python3 -c "
from src.api.production import ProductionConfigManager
manager = ProductionConfigManager()
config = manager.load_production_config()
print('Production configuration created')
"

echo "Installation complete!"
echo "To start the service: sudo systemctl start bioxen-api"
echo "To enable auto-start: sudo systemctl enable bioxen-api"
echo "View logs: journalctl -u bioxen-api -f"
```

#### Production Testing Checklist
```markdown
# Production Readiness Checklist

## ✅ Core Functionality
- [ ] Basic VM creation and lifecycle
- [ ] XCP-ng VM creation and lifecycle  
- [ ] All biological types (syn3a, ecoli, minimal_cell)
- [ ] Resource allocation and monitoring
- [ ] Configuration management
- [ ] Error handling and recovery

## ✅ Performance
- [ ] Load testing (10+ concurrent VMs)
- [ ] Resource allocation under load
- [ ] Memory usage monitoring
- [ ] Response time benchmarks
- [ ] Performance monitoring integration

## ✅ Security
- [ ] Configuration validation
- [ ] Audit logging
- [ ] User quotas and limits
- [ ] SSH key management (XCP-ng)
- [ ] Error message sanitization

## ✅ Monitoring
- [ ] Health check endpoints
- [ ] Performance metrics collection
- [ ] Resource usage monitoring
- [ ] Log aggregation
- [ ] Alert thresholds

## ✅ Documentation
- [ ] API reference documentation
- [ ] Configuration examples
- [ ] Troubleshooting guide
- [ ] Installation instructions
- [ ] Migration guide

## ✅ Deployment
- [ ] Docker containerization
- [ ] Configuration management
- [ ] Service management
- [ ] Backup and restore procedures
- [ ] Rollback procedures
```

---

## Phase 3 Success Criteria

### Week 5 Deliverables
- [ ] Complete CLI integration with existing tools
- [ ] Production configuration management
- [ ] Enhanced interactive mode
- [ ] Production VM management with quotas
- [ ] Audit logging implementation

### Week 6 Deliverables
- [ ] Comprehensive integration test suite
- [ ] Load testing and performance validation
- [ ] Production deployment configuration
- [ ] Complete documentation
- [ ] Installation and deployment scripts

### Critical Validation Points
1. **CLI Integration**: Seamless integration with existing interactive tools
2. **Production Features**: Quotas, monitoring, audit logging working
3. **Load Testing**: System stable under concurrent load
4. **Documentation**: Complete and accurate documentation
5. **Deployment**: Ready for production deployment
6. **Monitoring**: Comprehensive monitoring and alerting

---

## Project Completion Summary

### Total Implementation: 6 Weeks
- **Phase 1 (Weeks 1-2)**: Foundation and core VM classes
- **Phase 2 (Weeks 3-4)**: XCP-ng integration and advanced features  
- **Phase 3 (Weeks 5-6)**: Production readiness and deployment

### Key Achievements
1. **Infrastructure-Focused Architecture**: Perfect pylua alignment
2. **Dual VM Support**: Basic (direct) and XCP-ng (virtualized)
3. **Biological Type Composition**: All organisms work with both infrastructures
4. **Production Ready**: Monitoring, quotas, audit logging
5. **Complete Integration**: CLI and existing tool compatibility
6. **Comprehensive Testing**: Unit, integration, and load testing

### Post-Deployment
- Monitor system performance and stability
- Collect user feedback for future enhancements
- Plan for additional biological types and VM infrastructures
- Consider advanced features like inter-VM communication

---

## Notes

- **Production Security**: Implement proper authentication in production
- **Monitoring**: Set up monitoring dashboards and alerting
- **Backup**: Implement backup procedures for configurations and data
- **Updates**: Plan for rolling updates and version management
- **Support**: Establish support procedures and documentation
