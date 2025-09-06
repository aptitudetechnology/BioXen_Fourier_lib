"""
Production Configuration Management for BioXen

This module provides comprehensive configuration management for production
deployments of BioXen biological VM systems.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field
import logging


@dataclass
class ProductionConfig:
    """Production configuration for BioXen hypervisor"""
    # Core hypervisor settings
    max_vms: int = 4
    total_ribosomes: int = 80
    hypervisor_overhead: float = 0.15
    scheduling_quantum_ms: int = 100
    
    # Monitoring and logging
    enable_monitoring: bool = True
    log_level: str = "INFO"
    metrics_collection: bool = True
    performance_monitoring_interval: float = 30.0
    
    # Resource limits and safety
    max_ribosome_allocation: int = 60
    max_atp_percentage: float = 90.0
    max_memory_kb: int = 1024
    emergency_ribosome_reserve: int = 10
    resource_warning_threshold: float = 0.85
    
    # API and networking
    api_timeout_seconds: float = 30.0
    max_concurrent_operations: int = 10
    enable_remote_api: bool = False
    api_port: int = 8080
    
    # Security and isolation
    enable_chassis_isolation: bool = True
    sandbox_mode: bool = True
    audit_logging: bool = True
    
    # Environment-specific settings
    environment: str = "production"  # development, staging, production
    deployment_id: str = field(default_factory=lambda: f"bioxen-{os.getpid()}")
    config_version: str = "1.0"


class ProductionConfigManager:
    """Comprehensive production configuration management"""
    
    CONFIG_LOCATIONS = [
        Path.cwd() / "bioxen.yml",
        Path.cwd() / "bioxen.json", 
        Path.home() / ".bioxen" / "config.yml",
        Path.home() / ".bioxen" / "config.json",
        Path("/etc/bioxen/config.yml"),
        Path("/etc/bioxen/config.json"),
    ]
    
    ENV_PREFIX = "BIOXEN_"
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = logging.getLogger("bioxen.config")
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging based on configuration"""
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def _load_config(self) -> ProductionConfig:
        """Load configuration from multiple sources with precedence"""
        # Start with defaults
        config_data = {}
        
        # Load from file (if specified or found)
        file_config = self._load_from_file()
        if file_config:
            config_data.update(file_config)
        
        # Load from environment variables (highest precedence)
        env_config = self._load_from_environment()
        config_data.update(env_config)
        
        # Create configuration object
        try:
            return ProductionConfig(**config_data)
        except TypeError as e:
            self.logger.warning(f"Invalid configuration parameters: {e}, using defaults")
            return ProductionConfig()
    
    def _load_from_file(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_path and self.config_path.exists():
            return self._parse_config_file(self.config_path)
        
        # Search for config files in standard locations
        for config_file in self.CONFIG_LOCATIONS:
            if config_file.exists():
                self.config_path = config_file
                return self._parse_config_file(config_file)
        
        return {}
    
    def _parse_config_file(self, config_path: Path) -> Dict[str, Any]:
        """Parse configuration file (JSON or YAML)"""
        try:
            with open(config_path, 'r') as f:
                if config_path.suffix.lower() in ['.yml', '.yaml']:
                    return yaml.safe_load(f) or {}
                else:
                    return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to parse config file {config_path}: {e}")
            return {}
    
    def _load_from_environment(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        config = {}
        
        env_mapping = {
            f"{self.ENV_PREFIX}MAX_VMS": ("max_vms", int),
            f"{self.ENV_PREFIX}TOTAL_RIBOSOMES": ("total_ribosomes", int),
            f"{self.ENV_PREFIX}HYPERVISOR_OVERHEAD": ("hypervisor_overhead", float),
            f"{self.ENV_PREFIX}SCHEDULING_QUANTUM_MS": ("scheduling_quantum_ms", int),
            f"{self.ENV_PREFIX}ENABLE_MONITORING": ("enable_monitoring", self._parse_bool),
            f"{self.ENV_PREFIX}LOG_LEVEL": ("log_level", str),
            f"{self.ENV_PREFIX}METRICS_COLLECTION": ("metrics_collection", self._parse_bool),
            f"{self.ENV_PREFIX}MAX_RIBOSOME_ALLOCATION": ("max_ribosome_allocation", int),
            f"{self.ENV_PREFIX}MAX_ATP_PERCENTAGE": ("max_atp_percentage", float),
            f"{self.ENV_PREFIX}MAX_MEMORY_KB": ("max_memory_kb", int),
            f"{self.ENV_PREFIX}EMERGENCY_RIBOSOME_RESERVE": ("emergency_ribosome_reserve", int),
            f"{self.ENV_PREFIX}RESOURCE_WARNING_THRESHOLD": ("resource_warning_threshold", float),
            f"{self.ENV_PREFIX}API_TIMEOUT_SECONDS": ("api_timeout_seconds", float),
            f"{self.ENV_PREFIX}MAX_CONCURRENT_OPERATIONS": ("max_concurrent_operations", int),
            f"{self.ENV_PREFIX}ENABLE_REMOTE_API": ("enable_remote_api", self._parse_bool),
            f"{self.ENV_PREFIX}API_PORT": ("api_port", int),
            f"{self.ENV_PREFIX}ENABLE_CHASSIS_ISOLATION": ("enable_chassis_isolation", self._parse_bool),
            f"{self.ENV_PREFIX}SANDBOX_MODE": ("sandbox_mode", self._parse_bool),
            f"{self.ENV_PREFIX}AUDIT_LOGGING": ("audit_logging", self._parse_bool),
            f"{self.ENV_PREFIX}ENVIRONMENT": ("environment", str),
            f"{self.ENV_PREFIX}DEPLOYMENT_ID": ("deployment_id", str),
        }
        
        for env_var, (config_key, converter) in env_mapping.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    config[config_key] = converter(value)
                except (ValueError, TypeError) as e:
                    self.logger.warning(f"Invalid value for {env_var}: {value}, error: {e}")
        
        return config
    
    def _parse_bool(self, value: str) -> bool:
        """Parse boolean values from strings"""
        return value.lower() in ['true', '1', 'yes', 'on', 'enabled']
    
    def save_config(self, config_path: Optional[Path] = None):
        """Save current configuration to file"""
        save_path = config_path or self.config_path or (Path.home() / ".bioxen" / "config.yml")
        save_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(save_path, 'w') as f:
            if save_path.suffix.lower() in ['.yml', '.yaml']:
                yaml.dump(asdict(self.config), f, indent=2, default_flow_style=False)
            else:
                json.dump(asdict(self.config), f, indent=2)
        
        self.logger.info(f"Configuration saved to {save_path}")
    
    def validate_production_requirements(self) -> Dict[str, bool]:
        """Validate configuration meets production requirements"""
        checks = {
            "resource_limits_safe": (
                self.config.max_ribosome_allocation <= 
                self.config.total_ribosomes * (1 - self.config.hypervisor_overhead)
            ),
            "emergency_reserve_adequate": (
                self.config.emergency_ribosome_reserve >= 
                self.config.total_ribosomes * 0.1
            ),
            "vm_limits_reasonable": self.config.max_vms <= 8,
            "monitoring_enabled": self.config.enable_monitoring,
            "logging_configured": self.config.log_level.upper() in ["DEBUG", "INFO", "WARNING", "ERROR"],
            "atp_limits_safe": self.config.max_atp_percentage <= 95.0,
            "memory_limits_reasonable": self.config.max_memory_kb >= 64,
            "api_timeout_reasonable": 5.0 <= self.config.api_timeout_seconds <= 300.0,
            "scheduling_quantum_valid": 10 <= self.config.scheduling_quantum_ms <= 1000,
            "environment_set": self.config.environment in ["development", "staging", "production"]
        }
        
        # Log validation results
        failed_checks = [check for check, passed in checks.items() if not passed]
        if failed_checks:
            self.logger.warning(f"Production validation failed for: {failed_checks}")
        else:
            self.logger.info("All production validation checks passed")
        
        return checks
    
    def get_environment_config(self) -> Dict[str, Any]:
        """Get environment-specific configuration adjustments"""
        environment_configs = {
            "development": {
                "log_level": "DEBUG",
                "enable_monitoring": True,
                "sandbox_mode": False,
                "audit_logging": False,
                "max_vms": 2,
            },
            "staging": {
                "log_level": "INFO", 
                "enable_monitoring": True,
                "sandbox_mode": True,
                "audit_logging": True,
                "max_vms": 3,
            },
            "production": {
                "log_level": "WARNING",
                "enable_monitoring": True,
                "sandbox_mode": True,
                "audit_logging": True,
                "max_vms": 4,
            }
        }
        
        return environment_configs.get(self.config.environment, {})
    
    def apply_environment_config(self):
        """Apply environment-specific configuration overrides"""
        env_config = self.get_environment_config()
        for key, value in env_config.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
                self.logger.info(f"Applied environment override: {key} = {value}")
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary for logging/monitoring"""
        return {
            "config_version": self.config.config_version,
            "environment": self.config.environment,
            "deployment_id": self.config.deployment_id,
            "config_source": str(self.config_path) if self.config_path else "defaults",
            "max_vms": self.config.max_vms,
            "total_ribosomes": self.config.total_ribosomes,
            "monitoring_enabled": self.config.enable_monitoring,
            "log_level": self.config.log_level,
        }


# Global configuration manager instance
_config_manager = None

def get_config_manager() -> ProductionConfigManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ProductionConfigManager()
    return _config_manager

def get_config() -> ProductionConfig:
    """Get current production configuration"""
    return get_config_manager().config
