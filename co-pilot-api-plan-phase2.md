# BioXen_jcvi_vm_lib Factory Pattern API - Phase 2: Advanced Integration

## Phase 2 Overview: XCP-ng Integration & Advanced Features (Weeks 3-4)

**Objective**: Complete XCP-ng virtualization support, advanced resource management, and robust configuration validation.

**Duration**: 2 weeks
**Priority**: Core feature completion
**Dependencies**: Phase 1 foundation complete

---

## Week 3: XCP-ng Complete Integration

### Day 15-17: XCP-ng Implementation Completion

#### Complete `XCPngBiologicalVM` Implementation

**XCP-ng XAPI Client Integration**:
```python
# src/api/xcp_ng_integration.py
import requests
import paramiko
import json
from typing import Dict, Any, Optional

class XAPIClient:
    """XAPI client for XCP-ng communication following pylua patterns."""
    
    def __init__(self, url: str, username: str, password: str):
        self.url = url
        self.username = username
        self.password = password
        self.session_id = None
    
    def login(self) -> bool:
        """Login to XAPI and establish session."""
        try:
            response = requests.post(f"{self.url}/session.login_with_password", {
                'username': self.username,
                'password': self.password
            })
            self.session_id = response.json().get('Value')
            return True
        except Exception as e:
            print(f"XAPI login failed: {e}")
            return False
    
    def create_vm_from_template(self, template_name: str, vm_name: str) -> str:
        """Create VM from template and return VM UUID."""
        # Implementation for VM creation from template
        pass
    
    def start_vm(self, vm_uuid: str) -> bool:
        """Start VM by UUID."""
        # Implementation for starting VM
        pass
    
    def get_vm_ip(self, vm_uuid: str) -> str:
        """Get VM IP address."""
        # Implementation for getting VM IP
        pass
    
    def shutdown_vm(self, vm_uuid: str) -> bool:
        """Shutdown VM by UUID."""
        # Implementation for VM shutdown
        pass
    
    def get_vm_status(self, vm_uuid: str) -> Dict[str, Any]:
        """Get VM status information."""
        # Implementation for VM status
        pass

class SSHSession:
    """SSH session management for remote VM execution."""
    
    def __init__(self, user: str, key_path: Optional[str] = None):
        self.user = user
        self.key_path = key_path
        self.client = None
    
    def connect(self, host: str) -> bool:
        """Connect to remote host via SSH."""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            if self.key_path:
                self.client.connect(host, username=self.user, key_filename=self.key_path)
            else:
                # Password authentication would be implemented here
                pass
            return True
        except Exception as e:
            print(f"SSH connection failed: {e}")
            return False
    
    def execute_command(self, host: str, command: str) -> Dict[str, Any]:
        """Execute command on remote host."""
        if not self.connect(host):
            raise ConnectionError(f"Failed to connect to {host}")
        
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            return {
                'stdout': stdout.read().decode(),
                'stderr': stderr.read().decode(),
                'exit_code': stdout.channel.recv_exit_status()
            }
        finally:
            self.client.close()
```

**Complete XCPngBiologicalVM Methods**:
```python
# Update to src/api/biological_vm.py - XCPngBiologicalVM class
from .xcp_ng_integration import XAPIClient, SSHSession

class XCPngBiologicalVM(BiologicalVM):
    # ... existing code ...
    
    def _create_xcpng_vm(self) -> str:
        """Create XCP-ng VM from template (following pylua XAPI pattern)."""
        xapi_client = XAPIClient(
            url=self.xapi_config.get('xapi_url'),
            username=self.xapi_config.get('username'),
            password=self.xapi_config.get('password')
        )
        
        if not xapi_client.login():
            raise ConnectionError("Failed to login to XAPI")
        
        template_name = self.xapi_config.get('template_name', 'bioxen-bio-template')
        vm_name = f"bioxen-{self.biological_type}-{self.vm_id}"
        
        return xapi_client.create_vm_from_template(template_name, vm_name)
    
    def _start_xcpng_vm(self) -> bool:
        """Start the XCP-ng VM."""
        xapi_client = XAPIClient(
            url=self.xapi_config.get('xapi_url'),
            username=self.xapi_config.get('username'),
            password=self.xapi_config.get('password')
        )
        
        if not xapi_client.login():
            raise ConnectionError("Failed to login to XAPI")
        
        return xapi_client.start_vm(self.xcpng_vm_uuid)
    
    def _get_vm_ip(self) -> str:
        """Get IP address of started XCP-ng VM."""
        xapi_client = XAPIClient(
            url=self.xapi_config.get('xapi_url'),
            username=self.xapi_config.get('username'),
            password=self.xapi_config.get('password')
        )
        
        if not xapi_client.login():
            raise ConnectionError("Failed to login to XAPI")
        
        return xapi_client.get_vm_ip(self.xcpng_vm_uuid)
    
    def _start_biological_vm_via_ssh(self) -> bool:
        """Start biological VM inside XCP-ng VM via SSH."""
        ssh_session = SSHSession(
            user=self.xapi_config.get('ssh_user', 'root'),
            key_path=self.xapi_config.get('ssh_key_path')
        )
        
        # Start BioXen hypervisor inside XCP-ng VM
        start_command = f"bioxen_hypervisor start --type {self.biological_type} --vm-id {self.vm_id}"
        result = ssh_session.execute_command(self.vm_ip, start_command)
        
        return result['exit_code'] == 0
    
    def _execute_via_ssh(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process via SSH."""
        ssh_session = SSHSession(
            user=self.xapi_config.get('ssh_user', 'root'),
            key_path=self.xapi_config.get('ssh_key_path')
        )
        
        # Execute biological process command
        exec_command = f"bioxen_hypervisor execute --vm-id {self.vm_id} --code '{process_code}'"
        result = ssh_session.execute_command(self.vm_ip, exec_command)
        
        return {
            'stdout': result['stdout'],
            'stderr': result['stderr'],
            'success': result['exit_code'] == 0
        }
    
    def _install_package_via_ssh(self, package_name: str) -> Dict[str, Any]:
        """Install package via SSH."""
        ssh_session = SSHSession(
            user=self.xapi_config.get('ssh_user', 'root'),
            key_path=self.xapi_config.get('ssh_key_path')
        )
        
        # Install biological package command
        install_command = f"bioxen_hypervisor install --vm-id {self.vm_id} --package {package_name}"
        result = ssh_session.execute_command(self.vm_ip, install_command)
        
        return {
            'stdout': result['stdout'],
            'stderr': result['stderr'],
            'success': result['exit_code'] == 0
        }
    
    def _parse_biological_metrics(self, ssh_result: Dict[str, Any]) -> Dict[str, Any]:
        """Parse SSH result into biological metrics based on organism type."""
        if not ssh_result.get('success'):
            return {}
        
        try:
            # Parse JSON output from SSH command
            metrics = json.loads(ssh_result['stdout'])
            
            # Add biological type specific processing
            if self.biological_type == "syn3a":
                return self._process_syn3a_metrics(metrics)
            elif self.biological_type == "ecoli":
                return self._process_ecoli_metrics(metrics)
            elif self.biological_type == "minimal_cell":
                return self._process_minimal_cell_metrics(metrics)
            
            return metrics
        except json.JSONDecodeError:
            return {'error': 'Failed to parse metrics from SSH result'}
    
    def _process_syn3a_metrics(self, raw_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Process Syn3A specific metrics."""
        return {
            'atp_level': raw_metrics.get('atp_percent', 0.0),
            'essential_genes_active': raw_metrics.get('essential_genes_count', 0),
            'minimal_functions_status': raw_metrics.get('minimal_status', 'unknown')
        }
    
    def _process_ecoli_metrics(self, raw_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Process E.coli specific metrics."""
        return {
            'growth_rate': raw_metrics.get('growth_rate', 0.0),
            'plasmid_count': raw_metrics.get('plasmids', 0),
            'operon_activity': raw_metrics.get('operons_active', {})
        }
    
    def _process_minimal_cell_metrics(self, raw_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Process minimal cell specific metrics."""
        return {
            'basic_functions': raw_metrics.get('basic_functions', []),
            'function_efficiency': raw_metrics.get('efficiency', 0.0),
            'resource_utilization': raw_metrics.get('resource_usage', {})
        }
```

### Day 18-19: Advanced Resource Management

#### Enhanced `BioResourceManager` Implementation
```python
# Enhanced src/api/resource_manager.py
from typing import Dict, Any, Optional, List
from .biological_vm import BiologicalVM
import threading
import time

class BioResourceManager:
    """
    Advanced resource management wrapper for biological VMs.
    Supports both basic and XCP-ng VMs with monitoring.
    """
    
    def __init__(self, vm: BiologicalVM, enable_monitoring: bool = False):
        self.vm = vm
        self.hypervisor = vm.hypervisor
        self.enable_monitoring = enable_monitoring
        self._monitoring_thread = None
        self._monitoring_active = False
        self._resource_history = []
    
    def start_monitoring(self, interval_seconds: int = 30) -> bool:
        """Start resource monitoring thread."""
        if self.enable_monitoring and not self._monitoring_active:
            self._monitoring_active = True
            self._monitoring_thread = threading.Thread(
                target=self._monitor_resources,
                args=(interval_seconds,),
                daemon=True
            )
            self._monitoring_thread.start()
            return True
        return False
    
    def stop_monitoring(self) -> bool:
        """Stop resource monitoring."""
        if self._monitoring_active:
            self._monitoring_active = False
            if self._monitoring_thread:
                self._monitoring_thread.join(timeout=5)
            return True
        return False
    
    def _monitor_resources(self, interval: int) -> None:
        """Background resource monitoring."""
        while self._monitoring_active:
            try:
                usage = self.get_resource_usage()
                usage['timestamp'] = time.time()
                self._resource_history.append(usage)
                
                # Keep only last 100 readings
                if len(self._resource_history) > 100:
                    self._resource_history.pop(0)
                
                # Check for resource alerts
                self._check_resource_alerts(usage)
                
            except Exception as e:
                print(f"Resource monitoring error: {e}")
            
            time.sleep(interval)
    
    def _check_resource_alerts(self, usage: Dict[str, Any]) -> None:
        """Check for resource usage alerts."""
        atp_level = usage.get('atp_percent', 0)
        ribosome_usage = usage.get('ribosome_utilization', 0)
        
        if atp_level < 20:
            print(f"WARNING: Low ATP level in VM {self.vm.vm_id}: {atp_level}%")
        
        if ribosome_usage > 90:
            print(f"WARNING: High ribosome utilization in VM {self.vm.vm_id}: {ribosome_usage}%")
    
    def get_resource_history(self) -> List[Dict[str, Any]]:
        """Get resource usage history."""
        return self._resource_history.copy()
    
    def auto_optimize_resources(self) -> bool:
        """Automatically optimize resources based on VM type and usage patterns."""
        current_usage = self.get_resource_usage()
        biological_type = self.vm.get_biological_type()
        
        if biological_type == "syn3a":
            return self._auto_optimize_syn3a(current_usage)
        elif biological_type == "ecoli":
            return self._auto_optimize_ecoli(current_usage)
        elif biological_type == "minimal_cell":
            return self._auto_optimize_minimal_cell(current_usage)
        
        return False
    
    def _auto_optimize_syn3a(self, usage: Dict[str, Any]) -> bool:
        """Auto-optimize resources for Syn3A."""
        atp_level = usage.get('atp_percent', 0)
        
        if atp_level < 50:
            # Increase ATP allocation for minimal genome
            return self.allocate_atp(65.0)
        elif atp_level > 80:
            # Conserve ATP for essential functions only
            return self.allocate_atp(55.0)
        
        return True
    
    def _auto_optimize_ecoli(self, usage: Dict[str, Any]) -> bool:
        """Auto-optimize resources for E.coli."""
        growth_phase = usage.get('growth_phase', 'stationary')
        
        if growth_phase == 'exponential':
            # High resource allocation for rapid growth
            return (self.allocate_atp(85.0) and 
                   self.allocate_ribosomes(28))
        elif growth_phase == 'stationary':
            # Maintenance resource allocation
            return (self.allocate_atp(70.0) and 
                   self.allocate_ribosomes(20))
        
        return True
    
    def _auto_optimize_minimal_cell(self, usage: Dict[str, Any]) -> bool:
        """Auto-optimize resources for minimal cell."""
        function_efficiency = usage.get('function_efficiency', 0)
        
        if function_efficiency < 0.6:
            # Increase resources for basic functions
            return (self.allocate_atp(55.0) and 
                   self.allocate_ribosomes(10))
        
        return True
    
    def get_optimization_recommendations(self) -> List[str]:
        """Get resource optimization recommendations."""
        recommendations = []
        usage = self.get_resource_usage()
        biological_type = self.vm.get_biological_type()
        
        # General recommendations
        atp_level = usage.get('atp_percent', 0)
        if atp_level < 30:
            recommendations.append("Consider increasing ATP allocation")
        elif atp_level > 90:
            recommendations.append("ATP allocation may be excessive")
        
        # Biological type specific recommendations
        if biological_type == "syn3a":
            essential_genes = usage.get('essential_genes_active', 0)
            if essential_genes < 400:  # Syn3A has ~400 essential genes
                recommendations.append("Some essential genes may be inactive")
        
        elif biological_type == "ecoli":
            plasmid_count = usage.get('plasmid_count', 0)
            if plasmid_count > 5:
                recommendations.append("High plasmid count may impact performance")
        
        return recommendations
    
    def create_resource_snapshot(self) -> Dict[str, Any]:
        """Create a complete resource snapshot for backup/restore."""
        return {
            'vm_id': self.vm.vm_id,
            'biological_type': self.vm.get_biological_type(),
            'vm_type': self.vm.get_vm_type(),
            'timestamp': time.time(),
            'resource_usage': self.get_resource_usage(),
            'available_resources': self.get_available_resources(),
            'configuration': self.vm.config
        }
    
    def restore_from_snapshot(self, snapshot: Dict[str, Any]) -> bool:
        """Restore resource state from snapshot."""
        try:
            usage = snapshot.get('resource_usage', {})
            
            # Restore ATP allocation
            atp_level = usage.get('atp_percent', 50.0)
            if not self.allocate_atp(atp_level):
                return False
            
            # Restore ribosome allocation
            ribosome_count = usage.get('allocated_ribosomes', 10)
            if not self.allocate_ribosomes(ribosome_count):
                return False
            
            return True
        except Exception as e:
            print(f"Failed to restore from snapshot: {e}")
            return False
```

### Day 20-21: Advanced Configuration Management

#### Enhanced `ConfigManager` Implementation
```python
# Enhanced src/api/config_manager.py
from typing import Dict, Any, Optional, List
import json
import os
import yaml
from pathlib import Path

class ConfigManager:
    """
    Advanced configuration management for biological VMs.
    Supports multiple formats and environment-specific configs.
    """
    
    DEFAULT_CONFIG_PATHS = [
        "bioxen_config.json",
        "bioxen_config.yaml", 
        "~/.bioxen/config.json",
        "/etc/bioxen/config.json"
    ]
    
    @staticmethod
    def load_defaults(biological_type: str) -> Dict[str, Any]:
        """Load enhanced default configuration for biological type."""
        default_configs = {
            "syn3a": {
                "resource_limits": {
                    "max_atp": 70.0,
                    "max_ribosomes": 15,
                    "memory_limit": "512MB"
                },
                "biological_settings": {
                    "genome_optimization": True,
                    "minimal_mode": True,
                    "essential_genes_only": True
                },
                "performance": {
                    "enable_monitoring": True,
                    "optimization_interval": 60
                }
            },
            "ecoli": {
                "resource_limits": {
                    "max_atp": 90.0,
                    "max_ribosomes": 30,
                    "memory_limit": "1GB"
                },
                "biological_settings": {
                    "operon_management": True,
                    "plasmid_support": True,
                    "growth_optimization": True
                },
                "performance": {
                    "enable_monitoring": True,
                    "optimization_interval": 30
                }
            },
            "minimal_cell": {
                "resource_limits": {
                    "max_atp": 60.0,
                    "max_ribosomes": 12,
                    "memory_limit": "256MB"
                },
                "biological_settings": {
                    "basic_functions_only": True,
                    "function_validation": True,
                    "strict_mode": True
                },
                "performance": {
                    "enable_monitoring": False,
                    "optimization_interval": 120
                }
            }
        }
        return default_configs.get(biological_type, {})
    
    @staticmethod
    def auto_discover_config() -> Optional[str]:
        """Auto-discover configuration file from standard locations."""
        for config_path in ConfigManager.DEFAULT_CONFIG_PATHS:
            expanded_path = os.path.expanduser(config_path)
            if os.path.exists(expanded_path):
                return expanded_path
        return None
    
    @staticmethod
    def load_from_file(config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from file with auto-discovery."""
        if not config_path:
            config_path = ConfigManager.auto_discover_config()
            if not config_path:
                raise FileNotFoundError("No configuration file found in standard locations")
        
        config_path = os.path.expanduser(config_path)
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        file_ext = Path(config_path).suffix.lower()
        
        with open(config_path, 'r') as f:
            if file_ext in ['.yaml', '.yml']:
                return yaml.safe_load(f)
            elif file_ext == '.json':
                return json.load(f)
            else:
                # Try JSON first, then YAML
                try:
                    f.seek(0)
                    return json.load(f)
                except json.JSONDecodeError:
                    f.seek(0)
                    return yaml.safe_load(f)
    
    @staticmethod
    def save_to_file(config: Dict[str, Any], config_path: str, format: str = "json") -> bool:
        """Save configuration to file."""
        try:
            config_path = os.path.expanduser(config_path)
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            with open(config_path, 'w') as f:
                if format.lower() == "yaml":
                    yaml.dump(config, f, default_flow_style=False)
                else:
                    json.dump(config, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Failed to save config: {e}")
            return False
    
    @staticmethod
    def validate_config(config: Dict[str, Any], vm_type: str, biological_type: str) -> Tuple[bool, List[str]]:
        """Enhanced configuration validation with detailed error reporting."""
        errors = []
        
        # VM type specific validation
        if vm_type == "xcpng":
            xcpng_errors = ConfigManager._validate_xcpng_config(config)
            errors.extend(xcpng_errors)
        elif vm_type == "basic":
            basic_errors = ConfigManager._validate_basic_config(config)
            errors.extend(basic_errors)
        
        # Biological type specific validation
        bio_errors = ConfigManager._validate_biological_config(config, biological_type)
        errors.extend(bio_errors)
        
        # Resource limit validation
        resource_errors = ConfigManager._validate_resource_limits(config)
        errors.extend(resource_errors)
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _validate_xcpng_config(config: Dict[str, Any]) -> List[str]:
        """Validate XCP-ng specific configuration."""
        errors = []
        xcpng_config = config.get('xcpng_config', {})
        
        required_fields = {
            'xapi_url': 'XAPI URL',
            'username': 'Username', 
            'password': 'Password',
            'ssh_user': 'SSH User'
        }
        
        for field, description in required_fields.items():
            if field not in xcpng_config:
                errors.append(f"Missing required XCP-ng field: {description}")
            elif not xcpng_config[field]:
                errors.append(f"Empty XCP-ng field: {description}")
        
        # Optional but recommended fields
        recommended_fields = ['template_name', 'ssh_key_path']
        for field in recommended_fields:
            if field not in xcpng_config:
                errors.append(f"Recommended XCP-ng field missing: {field}")
        
        return errors
    
    @staticmethod
    def _validate_basic_config(config: Dict[str, Any]) -> List[str]:
        """Validate basic VM configuration."""
        errors = []
        
        # Basic VMs have minimal config requirements
        # Validate resource limits if present
        if 'resource_limits' in config:
            resource_limits = config['resource_limits']
            if 'max_atp' in resource_limits:
                max_atp = resource_limits['max_atp']
                if not 0 <= max_atp <= 100:
                    errors.append("max_atp must be between 0 and 100")
        
        return errors
    
    @staticmethod
    def _validate_biological_config(config: Dict[str, Any], biological_type: str) -> List[str]:
        """Validate biological type specific configuration."""
        errors = []
        
        bio_settings = config.get('biological_settings', {})
        
        if biological_type == "syn3a":
            if bio_settings.get('minimal_mode') is False:
                errors.append("Syn3A requires minimal_mode to be enabled")
        
        elif biological_type == "ecoli":
            if bio_settings.get('operon_management') is False:
                errors.append("E.coli configuration should enable operon_management")
        
        elif biological_type == "minimal_cell":
            if bio_settings.get('basic_functions_only') is False:
                errors.append("Minimal cell requires basic_functions_only mode")
        
        return errors
    
    @staticmethod
    def _validate_resource_limits(config: Dict[str, Any]) -> List[str]:
        """Validate resource limit configuration."""
        errors = []
        
        resource_limits = config.get('resource_limits', {})
        
        # ATP validation
        if 'max_atp' in resource_limits:
            max_atp = resource_limits['max_atp']
            if not isinstance(max_atp, (int, float)) or not 0 <= max_atp <= 100:
                errors.append("max_atp must be a number between 0 and 100")
        
        # Ribosome validation
        if 'max_ribosomes' in resource_limits:
            max_ribosomes = resource_limits['max_ribosomes']
            if not isinstance(max_ribosomes, int) or max_ribosomes < 1:
                errors.append("max_ribosomes must be a positive integer")
        
        # Memory validation
        if 'memory_limit' in resource_limits:
            memory_limit = resource_limits['memory_limit']
            if not isinstance(memory_limit, str):
                errors.append("memory_limit must be a string (e.g., '1GB', '512MB')")
        
        return errors
    
    @staticmethod
    def generate_template_config(biological_type: str, vm_type: str) -> Dict[str, Any]:
        """Generate a template configuration for given VM and biological types."""
        base_config = ConfigManager.load_defaults(biological_type)
        
        if vm_type == "xcpng":
            base_config['xcpng_config'] = {
                "xapi_url": "https://your-xcpng-host:443",
                "username": "root",
                "password": "your-secure-password",
                "template_name": "bioxen-bio-template",
                "ssh_user": "root",
                "ssh_key_path": "/path/to/ssh/key",
                "vm_memory": "2GB",
                "vm_vcpus": 2
            }
        
        return base_config
```

---

## Week 4: Integration Testing & Optimization

### Day 22-24: Comprehensive Testing

#### Enhanced Test Suite
```python
# tests/test_api/test_phase2.py
import pytest
import json
import tempfile
from unittest.mock import Mock, patch
from src.api import create_bio_vm, BasicBiologicalVM, XCPngBiologicalVM
from src.api.resource_manager import BioResourceManager
from src.api.config_manager import ConfigManager

class TestPhase2Integration:
    def test_basic_vm_complete_lifecycle(self):
        """Test complete lifecycle of basic VM."""
        vm = create_bio_vm("test_basic", "syn3a", "basic")
        
        # Test resource management
        resource_manager = BioResourceManager(vm)
        assert resource_manager.allocate_atp(75.0)
        assert resource_manager.allocate_ribosomes(12)
        
        # Test biological operations
        assert vm.start()
        
        # Test biological-specific methods
        if vm.get_biological_type() == "syn3a":
            genes = vm.get_essential_genes()
            assert isinstance(genes, list)
        
        # Test metrics
        metrics = vm.get_biological_metrics()
        assert isinstance(metrics, dict)
        
        assert vm.destroy()
    
    def test_xcpng_vm_with_valid_config(self):
        """Test XCP-ng VM creation with valid configuration."""
        xcpng_config = {
            "xcpng_config": {
                "xapi_url": "https://test-xcpng:443",
                "username": "root",
                "password": "test_password",
                "template_name": "bioxen-test-template",
                "ssh_user": "root",
                "ssh_key_path": "/tmp/test_key"
            }
        }
        
        vm = create_bio_vm("test_xcpng", "ecoli", "xcpng", xcpng_config)
        assert isinstance(vm, XCPngBiologicalVM)
        assert vm.get_vm_type() == "xcpng"
        assert vm.get_biological_type() == "ecoli"
    
    def test_resource_monitoring(self):
        """Test resource monitoring functionality."""
        vm = create_bio_vm("test_monitoring", "ecoli", "basic")
        resource_manager = BioResourceManager(vm, enable_monitoring=True)
        
        # Test monitoring start/stop
        assert resource_manager.start_monitoring(interval_seconds=1)
        
        import time
        time.sleep(2)  # Let monitoring collect some data
        
        history = resource_manager.get_resource_history()
        assert len(history) > 0
        
        assert resource_manager.stop_monitoring()
    
    def test_auto_optimization(self):
        """Test automatic resource optimization."""
        vm = create_bio_vm("test_optimization", "syn3a", "basic")
        resource_manager = BioResourceManager(vm)
        
        # Test auto-optimization
        result = resource_manager.auto_optimize_resources()
        assert isinstance(result, bool)
        
        # Test recommendations
        recommendations = resource_manager.get_optimization_recommendations()
        assert isinstance(recommendations, list)
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test valid basic config
        basic_config = ConfigManager.load_defaults("syn3a")
        is_valid, errors = ConfigManager.validate_config(basic_config, "basic", "syn3a")
        assert is_valid
        assert len(errors) == 0
        
        # Test invalid XCP-ng config
        invalid_xcpng_config = {"xcpng_config": {}}
        is_valid, errors = ConfigManager.validate_config(invalid_xcpng_config, "xcpng", "ecoli")
        assert not is_valid
        assert len(errors) > 0
    
    def test_config_file_operations(self):
        """Test configuration file save/load operations."""
        config = ConfigManager.load_defaults("ecoli")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_path = f.name
        
        # Test save
        assert ConfigManager.save_to_file(config, config_path, "json")
        
        # Test load
        loaded_config = ConfigManager.load_from_file(config_path)
        assert loaded_config == config
        
        # Cleanup
        import os
        os.unlink(config_path)
    
    def test_resource_snapshots(self):
        """Test resource snapshot and restore functionality."""
        vm = create_bio_vm("test_snapshot", "minimal_cell", "basic")
        resource_manager = BioResourceManager(vm)
        
        # Set initial state
        resource_manager.allocate_atp(60.0)
        resource_manager.allocate_ribosomes(8)
        
        # Create snapshot
        snapshot = resource_manager.create_resource_snapshot()
        assert 'vm_id' in snapshot
        assert 'timestamp' in snapshot
        assert 'resource_usage' in snapshot
        
        # Modify state
        resource_manager.allocate_atp(80.0)
        
        # Restore from snapshot
        assert resource_manager.restore_from_snapshot(snapshot)
    
    def test_biological_type_specific_methods(self):
        """Test biological type specific method routing."""
        # Test Syn3A specific methods
        syn3a_vm = create_bio_vm("test_syn3a_methods", "syn3a", "basic")
        genes = syn3a_vm.get_essential_genes()
        assert isinstance(genes, list)
        
        # Test E.coli specific methods
        ecoli_vm = create_bio_vm("test_ecoli_methods", "ecoli", "basic")
        plasmid_count = ecoli_vm.get_plasmid_count()
        assert isinstance(plasmid_count, int)
        
        # Test cross-type method calls should fail appropriately
        with pytest.raises(ValueError):
            ecoli_vm.start_transcription(["gene1"])  # Should fail for non-syn3a
```

### Day 25-26: Performance Optimization

#### Performance Monitoring and Optimization
```python
# src/api/performance.py
import time
import functools
from typing import Dict, Any, Callable

class PerformanceMonitor:
    """Performance monitoring for API operations."""
    
    def __init__(self):
        self.metrics = {}
    
    def time_operation(self, operation_name: str):
        """Decorator to time operations."""
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    duration = time.time() - start_time
                    self._record_metric(operation_name, duration, True)
                    return result
                except Exception as e:
                    duration = time.time() - start_time
                    self._record_metric(operation_name, duration, False)
                    raise
            return wrapper
        return decorator
    
    def _record_metric(self, operation: str, duration: float, success: bool):
        """Record performance metric."""
        if operation not in self.metrics:
            self.metrics[operation] = {
                'calls': 0,
                'total_time': 0,
                'successes': 0,
                'failures': 0,
                'avg_time': 0
            }
        
        metric = self.metrics[operation]
        metric['calls'] += 1
        metric['total_time'] += duration
        metric['avg_time'] = metric['total_time'] / metric['calls']
        
        if success:
            metric['successes'] += 1
        else:
            metric['failures'] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all performance metrics."""
        return self.metrics.copy()
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary."""
        summary = {
            'total_operations': sum(m['calls'] for m in self.metrics.values()),
            'total_time': sum(m['total_time'] for m in self.metrics.values()),
            'success_rate': 0,
            'slowest_operations': []
        }
        
        if summary['total_operations'] > 0:
            total_successes = sum(m['successes'] for m in self.metrics.values())
            summary['success_rate'] = total_successes / summary['total_operations']
        
        # Find slowest operations
        sorted_ops = sorted(
            self.metrics.items(),
            key=lambda x: x[1]['avg_time'],
            reverse=True
        )
        summary['slowest_operations'] = sorted_ops[:5]
        
        return summary

# Global performance monitor instance
performance_monitor = PerformanceMonitor()
```

#### Integration with API Classes
```python
# Update to src/api/biological_vm.py - add performance monitoring
from .performance import performance_monitor

class BiologicalVM(ABC):
    # ... existing code ...
    
    @performance_monitor.time_operation("vm_start")
    def start(self) -> bool:
        """Start the biological VM - mirrors pylua VM.start()."""
        return self.hypervisor.start_vm(self.vm_id)
    
    @performance_monitor.time_operation("vm_execute_biological_process") 
    def execute_biological_process(self, process_code: str) -> Dict[str, Any]:
        """Execute biological process - equivalent to pylua execute_string()."""
        return self._execute_biological_process_impl(process_code)
    
    # ... rest of the methods with performance monitoring ...
```

### Day 27-28: Documentation & Integration Validation

#### API Documentation
```markdown
# docs/api/phase2-advanced-features.md

## Advanced BioXen API Features

### XCP-ng Integration

The XCP-ng integration provides enhanced isolation by running BioXen VMs inside full virtual machines.

#### Configuration
```python
xcpng_config = {
    "xcpng_config": {
        "xapi_url": "https://xcpng-host:443",
        "username": "root",
        "password": "secure_password",
        "template_name": "bioxen-bio-template",
        "ssh_user": "root",
        "ssh_key_path": "/path/to/ssh/key",
        "vm_memory": "4GB",
        "vm_vcpus": 4
    }
}

vm = create_bio_vm("isolated_vm", "ecoli", "xcpng", xcpng_config)
```

### Advanced Resource Management

#### Monitoring
```python
from src.api import BioResourceManager

vm = create_bio_vm("monitored_vm", "syn3a", "basic")
manager = BioResourceManager(vm, enable_monitoring=True)

# Start monitoring
manager.start_monitoring(interval_seconds=30)

# Get historical data
history = manager.get_resource_history()

# Get optimization recommendations
recommendations = manager.get_optimization_recommendations()
```

#### Auto-Optimization
```python
# Automatic resource optimization
result = manager.auto_optimize_resources()

# Manual optimization with snapshots
snapshot = manager.create_resource_snapshot()
# ... make changes ...
manager.restore_from_snapshot(snapshot)
```

### Configuration Management

#### Multi-Format Support
```python
from src.api import ConfigManager

# Auto-discover configuration
config = ConfigManager.load_from_file()  # Auto-discovers from standard locations

# Validate configuration
is_valid, errors = ConfigManager.validate_config(config, "xcpng", "ecoli")

# Generate template
template = ConfigManager.generate_template_config("syn3a", "xcpng")
```
```

---

## Phase 2 Success Criteria

### Week 3 Deliverables
- [ ] Complete XCP-ng VM implementation with XAPI integration
- [ ] SSH execution for remote biological processes
- [ ] Advanced resource monitoring and auto-optimization
- [ ] Enhanced configuration management with validation
- [ ] Multi-format configuration file support (JSON/YAML)

### Week 4 Deliverables
- [ ] Comprehensive integration test suite
- [ ] Performance monitoring and optimization
- [ ] Complete API documentation for advanced features
- [ ] Resource snapshot and restore functionality
- [ ] Cross-VM type compatibility validation

### Critical Validation Points
1. **XCP-ng Integration**: Full lifecycle of virtualized biological VMs
2. **Remote Execution**: SSH-based biological process execution working
3. **Resource Monitoring**: Background monitoring with alerting
4. **Configuration Validation**: Robust validation with detailed error reporting
5. **Performance**: Minimal overhead for wrapper operations
6. **Compatibility**: All biological types work with both VM infrastructures

---

## Next Phase Preview

**Phase 3 (Weeks 5-6)**: CLI integration, production deployment features, comprehensive documentation, and final validation.

---

## Notes

- **XCP-ng Testing**: Requires actual XCP-ng environment for full validation
- **SSH Security**: Ensure proper key management and secure communication
- **Resource Monitoring**: Balance monitoring frequency with performance impact
- **Error Handling**: Comprehensive error handling for remote operations
- **Documentation**: Focus on practical examples and troubleshooting guides
