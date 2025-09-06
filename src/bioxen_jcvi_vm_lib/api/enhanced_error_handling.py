"""
Enhanced Error Handling and Logging for BioXen Production

This module provides production-ready error handling, standardized error codes,
and comprehensive logging for BioXen biological VM operations.
"""

import logging
import time
from typing import Optional, Dict, Any
from enum import Enum
from dataclasses import dataclass


class BioXenErrorCode(Enum):
    """Standardized error codes for BioXen operations"""
    VM_CREATION_FAILED = "BX001"
    RESOURCE_ALLOCATION_ERROR = "BX002"
    CHASSIS_INITIALIZATION_ERROR = "BX003"
    HYPERVISOR_OVERLOAD = "BX004"
    INVALID_CONFIGURATION = "BX005"
    VM_STATE_ERROR = "BX006"
    IMPORT_MODULE_ERROR = "BX007"
    API_VALIDATION_ERROR = "BX008"
    RESOURCE_EXHAUSTION = "BX009"
    VM_NOT_FOUND = "BX010"


class BioXenException(Exception):
    """Base exception for BioXen operations with structured error reporting"""
    
    def __init__(self, code: BioXenErrorCode, message: str, details: Optional[Dict] = None):
        self.code = code
        self.message = message
        self.details = details or {}
        self.timestamp = time.time()
        super().__init__(f"[{code.value}] {message}")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for logging/serialization"""
        return {
            "error_code": self.code.value,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp
        }


class ProductionLogger:
    """Production-ready logging for BioXen operations"""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(f"bioxen.{name}")
        self._setup_production_logging()
    
    def _setup_production_logging(self):
        """Configure production logging standards"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def log_vm_operation(self, operation: str, vm_id: str, success: bool, 
                        details: Dict = None, duration: float = None):
        """Log VM operations with structured data"""
        log_data = {
            "operation": operation,
            "vm_id": vm_id,
            "success": success,
            "timestamp": time.time()
        }
        if details:
            log_data.update(details)
        if duration is not None:
            log_data["duration_ms"] = duration * 1000
        
        if success:
            self.logger.info(f"VM operation successful: {operation} on {vm_id}", extra=log_data)
        else:
            self.logger.error(f"VM operation failed: {operation} on {vm_id}", extra=log_data)
    
    def log_resource_allocation(self, vm_id: str, resources: Dict, success: bool):
        """Log resource allocation operations"""
        log_data = {
            "vm_id": vm_id,
            "resources": resources,
            "success": success,
            "operation": "resource_allocation"
        }
        
        if success:
            self.logger.info(f"Resources allocated to VM {vm_id}: {resources}", extra=log_data)
        else:
            self.logger.error(f"Resource allocation failed for VM {vm_id}: {resources}", extra=log_data)
    
    def log_error(self, error: BioXenException, context: Dict = None):
        """Log BioXen exceptions with full context"""
        log_data = error.to_dict()
        if context:
            log_data["context"] = context
        
        self.logger.error(f"BioXen error: {error.message}", extra=log_data)
    
    def log_performance_metric(self, metric_name: str, value: float, unit: str = ""):
        """Log performance metrics"""
        log_data = {
            "metric": metric_name,
            "value": value,
            "unit": unit,
            "timestamp": time.time()
        }
        self.logger.info(f"Performance metric: {metric_name} = {value} {unit}", extra=log_data)


def handle_vm_operation(operation_name: str):
    """Decorator for VM operations with automatic error handling and logging"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = ProductionLogger("vm_operations")
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                
                # Extract VM ID if available
                vm_id = "unknown"
                if args and hasattr(args[0], 'vm_id'):
                    vm_id = args[0].vm_id
                elif 'vm_id' in kwargs:
                    vm_id = kwargs['vm_id']
                
                logger.log_vm_operation(operation_name, vm_id, True, duration=duration)
                return result
                
            except Exception as e:
                duration = time.time() - start_time
                vm_id = "unknown"
                if args and hasattr(args[0], 'vm_id'):
                    vm_id = args[0].vm_id
                elif 'vm_id' in kwargs:
                    vm_id = kwargs['vm_id']
                
                # Convert to BioXen exception if not already
                if not isinstance(e, BioXenException):
                    bx_error = BioXenException(
                        BioXenErrorCode.VM_STATE_ERROR,
                        f"{operation_name} failed: {str(e)}",
                        {"original_error": str(e), "operation": operation_name}
                    )
                else:
                    bx_error = e
                
                logger.log_vm_operation(operation_name, vm_id, False, 
                                      details=bx_error.details, duration=duration)
                logger.log_error(bx_error, {"operation": operation_name, "args": str(args)})
                raise bx_error
                
        return wrapper
    return decorator


@dataclass
class ErrorRecoveryAction:
    """Defines recovery actions for specific error scenarios"""
    error_code: BioXenErrorCode
    action_type: str  # "retry", "fallback", "abort", "cleanup"
    max_attempts: int = 1
    delay_seconds: float = 0.0
    fallback_params: Optional[Dict] = None


class ErrorRecoveryManager:
    """Manages error recovery strategies for production environments"""
    
    def __init__(self):
        self.recovery_strategies = {
            BioXenErrorCode.RESOURCE_ALLOCATION_ERROR: ErrorRecoveryAction(
                BioXenErrorCode.RESOURCE_ALLOCATION_ERROR,
                "retry",
                max_attempts=3,
                delay_seconds=1.0
            ),
            BioXenErrorCode.VM_CREATION_FAILED: ErrorRecoveryAction(
                BioXenErrorCode.VM_CREATION_FAILED,
                "fallback",
                fallback_params={"use_minimal_resources": True}
            ),
            BioXenErrorCode.HYPERVISOR_OVERLOAD: ErrorRecoveryAction(
                BioXenErrorCode.HYPERVISOR_OVERLOAD,
                "cleanup",
                fallback_params={"free_unused_resources": True}
            )
        }
        self.logger = ProductionLogger("error_recovery")
    
    def handle_error(self, error: BioXenException, context: Dict = None) -> bool:
        """Handle error with appropriate recovery strategy"""
        strategy = self.recovery_strategies.get(error.code)
        if not strategy:
            self.logger.log_error(error, context)
            return False
        
        self.logger.logger.info(f"Attempting recovery for {error.code.value}: {strategy.action_type}")
        
        if strategy.action_type == "retry":
            return self._handle_retry(error, strategy, context)
        elif strategy.action_type == "fallback":
            return self._handle_fallback(error, strategy, context)
        elif strategy.action_type == "cleanup":
            return self._handle_cleanup(error, strategy, context)
        
        return False
    
    def _handle_retry(self, error: BioXenException, strategy: ErrorRecoveryAction, context: Dict) -> bool:
        """Handle retry strategy"""
        self.logger.logger.info(f"Retry strategy: waiting {strategy.delay_seconds}s before retry")
        time.sleep(strategy.delay_seconds)
        return True  # Signal that retry should be attempted
    
    def _handle_fallback(self, error: BioXenException, strategy: ErrorRecoveryAction, context: Dict) -> bool:
        """Handle fallback strategy"""
        self.logger.logger.info(f"Fallback strategy: {strategy.fallback_params}")
        # Implementation would depend on specific fallback requirements
        return True
    
    def _handle_cleanup(self, error: BioXenException, strategy: ErrorRecoveryAction, context: Dict) -> bool:
        """Handle cleanup strategy"""
        self.logger.logger.info(f"Cleanup strategy: {strategy.fallback_params}")
        # Implementation would trigger resource cleanup
        return True


# Global error recovery manager instance
error_recovery = ErrorRecoveryManager()
