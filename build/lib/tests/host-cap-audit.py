#!/usr/bin/env python3
"""
BioXen Host Capability Audit
============================

Comprehensive system analysis for bare metal BioXen deployment.
Audits OS, hardware, and computational capabilities for biological hypervisor workloads.

Usage:
    python3 tests/host-cap-audit.py [--verbose] [--json] [--benchmark]
"""

import sys
import os
import platform
import subprocess
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Any
import argparse


@dataclass
class SystemCapabilities:
    """System capability assessment results"""
    os_info: Dict[str, str]
    hardware: Dict[str, Any]
    compute: Dict[str, Any]
    memory: Dict[str, Any]
    storage: Dict[str, Any]
    network: Dict[str, Any]
    specialized: Dict[str, Any]
    bioxen_readiness: Dict[str, Any]


class HostCapabilityAuditor:
    """Main system capability auditor for BioXen deployment"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {}
        self.test_dir = Path(__file__).parent
        
    def log(self, message: str, level: str = "INFO"):
        """Logging with optional verbosity"""
        if self.verbose or level in ["ERROR", "CRITICAL"]:
            print(f"[{level}] {message}")
    
    def run_command(self, cmd: List[str], timeout: int = 30) -> Optional[str]:
        """Safely execute system commands"""
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                check=False
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.log(f"Command failed: {' '.join(cmd)} - {e}", "WARNING")
            return None
    
    def audit_os_info(self) -> Dict[str, str]:
        """Audit operating system and kernel information"""
        self.log("Auditing OS and kernel...")
        
        info = {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "architecture": platform.architecture()[0],
            "python_version": platform.python_version(),
            "hostname": platform.node()
        }
        
        # Linux-specific kernel info
        if info["system"] == "Linux":
            kernel_version = self.run_command(["uname", "-r"])
            if kernel_version:
                info["kernel_version"] = kernel_version
                
            # Distribution info
            dist_info = self.run_command(["lsb_release", "-d"])
            if dist_info:
                info["distribution"] = dist_info.replace("Description:", "").strip()
            else:
                # Fallback to /etc/os-release
                try:
                    with open("/etc/os-release", "r") as f:
                        for line in f:
                            if line.startswith("PRETTY_NAME="):
                                info["distribution"] = line.split("=")[1].strip('"')
                                break
                except FileNotFoundError:
                    info["distribution"] = "Unknown Linux"
        
        return info
    
    def audit_cpu_info(self) -> Dict[str, Any]:
        """Audit CPU capabilities and features"""
        self.log("Auditing CPU capabilities...")
        
        cpu_info = {
            "cores_physical": os.cpu_count(),
            "cores_logical": len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else os.cpu_count(),
            "features": []
        }
        
        # Linux CPU info
        if platform.system() == "Linux":
            try:
                with open("/proc/cpuinfo", "r") as f:
                    cpuinfo = f.read()
                    
                # Extract CPU model
                for line in cpuinfo.split('\n'):
                    if line.startswith("model name"):
                        cpu_info["model"] = line.split(":")[1].strip()
                        break
                    
                # Extract CPU features/flags
                for line in cpuinfo.split('\n'):
                    if line.startswith("flags"):
                        cpu_info["features"] = line.split(":")[1].strip().split()
                        break
                        
            except FileNotFoundError:
                self.log("Could not read /proc/cpuinfo", "WARNING")
        
        # Cross-platform CPU frequency (if available)
        cpu_freq = self.run_command(["lscpu"])
        if cpu_freq:
            cpu_info["lscpu_output"] = cpu_freq
            
        return cpu_info
    
    def audit_memory_info(self) -> Dict[str, Any]:
        """Audit system memory capabilities"""
        self.log("Auditing memory subsystem...")
        
        memory_info = {}
        
        # Linux memory info
        if platform.system() == "Linux":
            try:
                with open("/proc/meminfo", "r") as f:
                    meminfo = {}
                    for line in f:
                        if ":" in line:
                            key, value = line.split(":", 1)
                            meminfo[key.strip()] = value.strip()
                    
                    # Convert key metrics to MB
                    memory_info["total_ram_mb"] = int(meminfo.get("MemTotal", "0").split()[0]) // 1024
                    memory_info["available_ram_mb"] = int(meminfo.get("MemAvailable", "0").split()[0]) // 1024
                    memory_info["free_ram_mb"] = int(meminfo.get("MemFree", "0").split()[0]) // 1024
                    memory_info["swap_total_mb"] = int(meminfo.get("SwapTotal", "0").split()[0]) // 1024
                    memory_info["swap_free_mb"] = int(meminfo.get("SwapFree", "0").split()[0]) // 1024
                    
            except FileNotFoundError:
                self.log("Could not read /proc/meminfo", "WARNING")
        
        # Cross-platform memory using psutil if available
        try:
            import psutil
            mem = psutil.virtual_memory()
            memory_info["psutil_total_gb"] = round(mem.total / (1024**3), 2)
            memory_info["psutil_available_gb"] = round(mem.available / (1024**3), 2)
            memory_info["psutil_percent_used"] = mem.percent
        except ImportError:
            self.log("psutil not available for cross-platform memory info", "WARNING")
            
        return memory_info
    
    def audit_gpu_info(self) -> Dict[str, Any]:
        """Audit GPU capabilities"""
        self.log("Auditing GPU capabilities...")
        
        gpu_info = {
            "nvidia_gpus": [],
            "amd_gpus": [],
            "intel_gpus": [],
            "cuda_available": False,
            "opencl_available": False
        }
        
        # NVIDIA GPU detection
        nvidia_smi = self.run_command(["nvidia-smi", "--query-gpu=name,memory.total,compute_cap", "--format=csv,noheader,nounits"])
        if nvidia_smi:
            for line in nvidia_smi.split('\n'):
                if line.strip():
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) >= 3:
                        gpu_info["nvidia_gpus"].append({
                            "name": parts[0],
                            "memory_mb": parts[1],
                            "compute_capability": parts[2]
                        })
        
        # Check for CUDA toolkit
        nvcc_version = self.run_command(["nvcc", "--version"])
        if nvcc_version:
            gpu_info["cuda_available"] = True
            gpu_info["cuda_version"] = nvcc_version
            
        # Check for OpenCL
        try:
            import pyopencl as cl
            platforms = cl.get_platforms()
            gpu_info["opencl_available"] = True
            gpu_info["opencl_platforms"] = len(platforms)
        except ImportError:
            self.log("PyOpenCL not available", "WARNING")
            
        return gpu_info
    
    def audit_storage_info(self) -> Dict[str, Any]:
        """Audit storage subsystem"""
        self.log("Auditing storage capabilities...")
        
        storage_info = {}
        
        # Disk space for current directory
        try:
            import shutil
            total, used, free = shutil.disk_usage(Path.cwd())
            storage_info["current_dir"] = {
                "total_gb": round(total / (1024**3), 2),
                "used_gb": round(used / (1024**3), 2),
                "free_gb": round(free / (1024**3), 2)
            }
        except Exception as e:
            self.log(f"Could not get disk usage: {e}", "WARNING")
            
        # Linux-specific storage info
        if platform.system() == "Linux":
            df_output = self.run_command(["df", "-h"])
            if df_output:
                storage_info["df_output"] = df_output
                
        return storage_info
    
    def audit_network_info(self) -> Dict[str, Any]:
        """Audit network capabilities"""
        self.log("Auditing network capabilities...")
        
        network_info = {}
        
        # Basic connectivity test
        ping_result = self.run_command(["ping", "-c", "1", "8.8.8.8"])
        network_info["internet_connectivity"] = ping_result is not None
        
        # Network interfaces (Linux)
        if platform.system() == "Linux":
            ip_output = self.run_command(["ip", "addr", "show"])
            if ip_output:
                network_info["interfaces"] = ip_output
                
        return network_info
    
    def run_specialized_tests(self) -> Dict[str, Any]:
        """Run specialized capability tests"""
        self.log("Running specialized capability tests...")
        
        specialized = {}
        
        # SIMD extensions test
        simd_script = self.test_dir / "simd" / "test_simd.py"
        if simd_script.exists():
            self.log("Running SIMD capability test...")
            simd_result = self.run_command([sys.executable, str(simd_script)])
            specialized["simd"] = simd_result
        else:
            self.log("SIMD test script not found", "WARNING")
            specialized["simd"] = "test_not_available"
            
        # GPU compute test
        gpu_script = self.test_dir / "gpu" / "test_gpu.py"
        if gpu_script.exists():
            self.log("Running GPU compute test...")
            gpu_result = self.run_command([sys.executable, str(gpu_script)])
            specialized["gpu_compute"] = gpu_result
        else:
            self.log("GPU test script not found", "WARNING")
            specialized["gpu_compute"] = "test_not_available"
            
        return specialized
    
    def assess_bioxen_readiness(self, capabilities: Dict[str, Any]) -> Dict[str, Any]:
        """Assess system readiness for BioXen workloads"""
        self.log("Assessing BioXen deployment readiness...")
        
        readiness = {
            "overall_score": 0,
            "recommendations": [],
            "warnings": [],
            "blocking_issues": []
        }
        
        # Memory assessment
        if "memory" in capabilities and "total_ram_mb" in capabilities["memory"]:
            ram_gb = capabilities["memory"]["total_ram_mb"] / 1024
            if ram_gb >= 32:
                readiness["overall_score"] += 25
                readiness["recommendations"].append(f"Excellent: {ram_gb:.1f}GB RAM available")
            elif ram_gb >= 16:
                readiness["overall_score"] += 20
                readiness["recommendations"].append(f"Good: {ram_gb:.1f}GB RAM available")
            elif ram_gb >= 8:
                readiness["overall_score"] += 15
                readiness["warnings"].append(f"Moderate: {ram_gb:.1f}GB RAM - consider 16GB+ for large genomes")
            else:
                readiness["warnings"].append(f"Low: {ram_gb:.1f}GB RAM - may limit concurrent VMs")
        
        # CPU assessment
        if "hardware" in capabilities and "cores_physical" in capabilities["hardware"]:
            cores = capabilities["hardware"]["cores_physical"]
            if cores >= 16:
                readiness["overall_score"] += 25
                readiness["recommendations"].append(f"Excellent: {cores} CPU cores for parallel VM execution")
            elif cores >= 8:
                readiness["overall_score"] += 20
                readiness["recommendations"].append(f"Good: {cores} CPU cores available")
            elif cores >= 4:
                readiness["overall_score"] += 15
                readiness["warnings"].append(f"Moderate: {cores} cores - parallel VM performance may be limited")
            else:
                readiness["warnings"].append(f"Low: {cores} cores - sequential VM execution recommended")
        
        # GPU assessment
        if "hardware" in capabilities and "cuda_available" in capabilities["hardware"]:
            if capabilities["hardware"]["cuda_available"]:
                readiness["overall_score"] += 25
                readiness["recommendations"].append("Excellent: CUDA GPU available for protein folding acceleration")
            elif capabilities["hardware"]["opencl_available"]:
                readiness["overall_score"] += 15
                readiness["recommendations"].append("Good: OpenCL GPU available for compute acceleration")
            else:
                readiness["warnings"].append("No GPU acceleration - CPU-only molecular simulations")
        
        # Operating system assessment
        if "os_info" in capabilities:
            if capabilities["os_info"]["system"] == "Linux":
                readiness["overall_score"] += 25
                readiness["recommendations"].append("Excellent: Linux OS optimal for BioXen deployment")
            elif capabilities["os_info"]["system"] in ["Darwin", "Windows"]:
                readiness["overall_score"] += 15
                readiness["warnings"].append(f"Moderate: {capabilities['os_info']['system']} OS - Linux recommended for production")
        
        # Final assessment
        if readiness["overall_score"] >= 80:
            readiness["status"] = "EXCELLENT - Ready for production BioXen deployment"
        elif readiness["overall_score"] >= 60:
            readiness["status"] = "GOOD - Suitable for BioXen development and testing"
        elif readiness["overall_score"] >= 40:
            readiness["status"] = "MODERATE - Basic BioXen functionality available"
        else:
            readiness["status"] = "LIMITED - Significant performance constraints expected"
            
        return readiness
    
    def run_full_audit(self) -> SystemCapabilities:
        """Execute complete system capability audit"""
        self.log("Starting BioXen Host Capability Audit...")
        start_time = time.time()
        
        # Core system audits
        os_info = self.audit_os_info()
        cpu_info = self.audit_cpu_info()
        memory_info = self.audit_memory_info()
        gpu_info = self.audit_gpu_info()
        storage_info = self.audit_storage_info()
        network_info = self.audit_network_info()
        
        # Combine hardware info
        hardware = {**cpu_info, **gpu_info}
        
        # Specialized tests
        specialized = self.run_specialized_tests()
        
        # Create capability summary
        capabilities = {
            "os_info": os_info,
            "hardware": hardware,
            "memory": memory_info,
            "storage": storage_info,
            "network": network_info,
            "specialized": specialized
        }
        
        # Assess BioXen readiness
        bioxen_readiness = self.assess_bioxen_readiness(capabilities)
        
        audit_time = time.time() - start_time
        self.log(f"Audit completed in {audit_time:.2f} seconds")
        
        return SystemCapabilities(
            os_info=os_info,
            hardware=hardware,
            compute=specialized,
            memory=memory_info,
            storage=storage_info,
            network=network_info,
            specialized=specialized,
            bioxen_readiness=bioxen_readiness
        )


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description="BioXen Host Capability Audit")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", "-j", action="store_true", help="Output results as JSON")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Run performance benchmarks")
    
    args = parser.parse_args()
    
    # Initialize auditor
    auditor = HostCapabilityAuditor(verbose=args.verbose)
    
    # Run audit
    try:
        capabilities = auditor.run_full_audit()
        
        if args.json:
            # JSON output
            print(json.dumps(asdict(capabilities), indent=2))
        else:
            # Human-readable output
            print("\n" + "="*60)
            print("BioXen Host Capability Audit Results")
            print("="*60)
            
            print(f"\n🖥️  System: {capabilities.os_info['system']} {capabilities.os_info['release']}")
            print(f"🏗️  Architecture: {capabilities.os_info['architecture']}")
            print(f"🐍 Python: {capabilities.os_info['python_version']}")
            
            if "model" in capabilities.hardware:
                print(f"\n🔧 CPU: {capabilities.hardware['model']}")
            print(f"⚙️  Cores: {capabilities.hardware.get('cores_physical', 'Unknown')}")
            
            if "total_ram_mb" in capabilities.memory:
                ram_gb = capabilities.memory["total_ram_mb"] / 1024
                print(f"💾 RAM: {ram_gb:.1f} GB")
            
            if capabilities.hardware.get("nvidia_gpus"):
                print(f"🎮 NVIDIA GPUs: {len(capabilities.hardware['nvidia_gpus'])}")
                for gpu in capabilities.hardware["nvidia_gpus"]:
                    print(f"   - {gpu['name']} ({gpu['memory_mb']} MB)")
            
            print(f"\n🧬 BioXen Readiness: {capabilities.bioxen_readiness['status']}")
            print(f"📊 Score: {capabilities.bioxen_readiness['overall_score']}/100")
            
            if capabilities.bioxen_readiness.get("recommendations"):
                print("\n✅ Recommendations:")
                for rec in capabilities.bioxen_readiness["recommendations"]:
                    print(f"   • {rec}")
                    
            if capabilities.bioxen_readiness.get("warnings"):
                print("\n⚠️  Warnings:")
                for warning in capabilities.bioxen_readiness["warnings"]:
                    print(f"   • {warning}")
            
            print("\n" + "="*60)
            print("Audit complete. System ready for BioXen deployment assessment.")
            
    except KeyboardInterrupt:
        print("\nAudit interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Audit failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()