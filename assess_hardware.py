#!/usr/bin/env python3
"""
BioXen Hardware Assessment Tool

Analyzes current system capabilities and recommends optimizations
for BioXen-JCVI genomics workloads.
"""

import os
import sys
import subprocess
import platform
import psutil
import json
from pathlib import Path
from datetime import datetime

class BioXenHardwareAssessment:
    """Hardware assessment for BioXen-JCVI platform"""
    
    def __init__(self):
        self.system_info = {}
        self.assessment = {}
        self.recommendations = []
        
    def detect_hardware(self):
        """Comprehensive hardware detection"""
        print("🔍 BioXen Hardware Assessment")
        print("=" * 50)
        
        # Basic system information
        self.system_info['os'] = {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor()
        }
        
        # CPU information
        self.detect_cpu()
        
        # Memory information
        self.detect_memory()
        
        # Storage information
        self.detect_storage()
        
        # GPU information
        self.detect_gpu()
        
        # Network information
        self.detect_network()
        
    def detect_cpu(self):
        """Detect CPU specifications"""
        print("\n🖥️  CPU Analysis:")
        
        cpu_info = {
            'cores_physical': psutil.cpu_count(logical=False),
            'cores_logical': psutil.cpu_count(logical=True),
            'frequency_current': psutil.cpu_freq().current if psutil.cpu_freq() else 'Unknown',
            'frequency_max': psutil.cpu_freq().max if psutil.cpu_freq() else 'Unknown'
        }
        
        # Try to get more detailed CPU info on Linux
        if platform.system() == 'Linux':
            try:
                with open('/proc/cpuinfo', 'r') as f:
                    cpuinfo = f.read()
                    
                # Extract CPU model
                for line in cpuinfo.split('\n'):
                    if 'model name' in line:
                        cpu_info['model'] = line.split(':')[1].strip()
                        break
                
                # Check for instruction sets
                cpu_info['features'] = {
                    'avx': 'avx' in cpuinfo,
                    'avx2': 'avx2' in cpuinfo,
                    'avx512f': 'avx512f' in cpuinfo,
                    'sse4_2': 'sse4_2' in cpuinfo
                }
                        
            except Exception as e:
                cpu_info['model'] = 'Detection failed'
                cpu_info['features'] = {}
        
        self.system_info['cpu'] = cpu_info
        
        # Print CPU info
        print(f"   Model: {cpu_info.get('model', 'Unknown')}")
        print(f"   Physical cores: {cpu_info['cores_physical']}")
        print(f"   Logical cores: {cpu_info['cores_logical']}")
        
        if cpu_info['frequency_max'] != 'Unknown':
            print(f"   Max frequency: {cpu_info['frequency_max']:.0f} MHz")
        
        # Check instruction sets
        features = cpu_info.get('features', {})
        if features:
            print(f"   AVX support: {'✅' if features.get('avx') else '❌'}")
            print(f"   AVX2 support: {'✅' if features.get('avx2') else '❌'}")
            print(f"   AVX-512 support: {'✅' if features.get('avx512f') else '❌'}")
    
    def detect_memory(self):
        """Detect memory specifications"""
        print("\n🧠 Memory Analysis:")
        
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        memory_info = {
            'total_gb': round(memory.total / (1024**3), 1),
            'available_gb': round(memory.available / (1024**3), 1),
            'used_percent': memory.percent,
            'swap_total_gb': round(swap.total / (1024**3), 1) if swap.total > 0 else 0
        }
        
        self.system_info['memory'] = memory_info
        
        print(f"   Total RAM: {memory_info['total_gb']} GB")
        print(f"   Available: {memory_info['available_gb']} GB")
        print(f"   Current usage: {memory_info['used_percent']:.1f}%")
        
        if memory_info['swap_total_gb'] > 0:
            print(f"   Swap space: {memory_info['swap_total_gb']} GB")
    
    def detect_storage(self):
        """Detect storage specifications"""
        print("\n💾 Storage Analysis:")
        
        storage_info = []
        
        # Get disk usage for all mounted filesystems
        disk_partitions = psutil.disk_partitions()
        
        for partition in disk_partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                
                partition_info = {
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'filesystem': partition.fstype,
                    'total_gb': round(usage.total / (1024**3), 1),
                    'used_gb': round(usage.used / (1024**3), 1),
                    'free_gb': round(usage.free / (1024**3), 1),
                    'used_percent': round((usage.used / usage.total) * 100, 1)
                }
                
                storage_info.append(partition_info)
                
                print(f"   {partition.device}")
                print(f"      Mount: {partition.mountpoint}")
                print(f"      Type: {partition.fstype}")
                print(f"      Size: {partition_info['total_gb']} GB")
                print(f"      Free: {partition_info['free_gb']} GB ({100-partition_info['used_percent']:.1f}% free)")
                
            except PermissionError:
                continue
        
        self.system_info['storage'] = storage_info
    
    def detect_gpu(self):
        """Detect GPU specifications"""
        print("\n🎮 GPU Analysis:")
        
        gpu_info = []
        
        # Try nvidia-smi for NVIDIA GPUs
        try:
            result = subprocess.run(['nvidia-smi', '--query-gpu=name,memory.total,driver_version', 
                                   '--format=csv,noheader,nounits'], 
                                   capture_output=True, text=True, check=True)
            
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    parts = line.split(', ')
                    if len(parts) >= 3:
                        gpu_info.append({
                            'name': parts[0],
                            'memory_mb': int(parts[1]),
                            'driver': parts[2],
                            'type': 'NVIDIA'
                        })
                        
                        print(f"   NVIDIA GPU: {parts[0]}")
                        print(f"      Memory: {int(parts[1])} MB")
                        print(f"      Driver: {parts[2]}")
                        
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("   NVIDIA GPU: Not detected")
        
        # Try lspci for other GPUs
        try:
            result = subprocess.run(['lspci'], capture_output=True, text=True, check=True)
            
            for line in result.stdout.split('\n'):
                if 'VGA' in line or 'Display' in line:
                    if 'NVIDIA' not in line:  # Already handled above
                        gpu_info.append({
                            'name': line.split(':')[-1].strip(),
                            'type': 'Other'
                        })
                        print(f"   Other GPU: {line.split(':')[-1].strip()}")
                        
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass
        
        if not gpu_info:
            print("   No dedicated GPU detected")
        
        self.system_info['gpu'] = gpu_info
    
    def detect_network(self):
        """Detect network specifications"""
        print("\n🌐 Network Analysis:")
        
        network_info = []
        
        # Get network interfaces
        net_if_addrs = psutil.net_if_addrs()
        net_if_stats = psutil.net_if_stats()
        
        for interface, addresses in net_if_addrs.items():
            if interface in net_if_stats:
                stats = net_if_stats[interface]
                
                interface_info = {
                    'name': interface,
                    'speed_mbps': stats.speed if stats.speed > 0 else 'Unknown',
                    'is_up': stats.isup
                }
                
                # Get IP addresses
                for addr in addresses:
                    if addr.family.name == 'AF_INET':
                        interface_info['ipv4'] = addr.address
                
                network_info.append(interface_info)
                
                if stats.isup and interface != 'lo':
                    print(f"   {interface}: {'Up' if stats.isup else 'Down'}")
                    if stats.speed > 0:
                        print(f"      Speed: {stats.speed} Mbps")
                    if 'ipv4' in interface_info:
                        print(f"      IP: {interface_info['ipv4']}")
        
        self.system_info['network'] = network_info
    
    def assess_performance(self):
        """Assess system performance for BioXen-JCVI workloads"""
        print("\n📊 BioXen-JCVI Performance Assessment:")
        print("=" * 50)
        
        cpu = self.system_info.get('cpu', {})
        memory = self.system_info.get('memory', {})
        gpu = self.system_info.get('gpu', [])
        
        # CPU assessment
        cpu_cores = cpu.get('cores_logical', 0)
        cpu_score = min(10, cpu_cores / 1.6)  # 16 cores = 10/10
        
        print(f"\n🖥️  CPU Score: {cpu_score:.1f}/10")
        if cpu_cores >= 16:
            print("   ✅ Excellent for multi-threaded BLAST and MCscan")
        elif cpu_cores >= 8:
            print("   🟡 Good for genomics workloads")
        else:
            print("   🔴 Limited for large-scale analysis")
            self.recommendations.append("Upgrade to 8+ core CPU for better genomics performance")
        
        # Memory assessment
        memory_gb = memory.get('total_gb', 0)
        memory_score = min(10, memory_gb / 12.8)  # 128GB = 10/10
        
        print(f"\n🧠 Memory Score: {memory_score:.1f}/10")
        if memory_gb >= 64:
            print("   ✅ Excellent for large genome databases")
        elif memory_gb >= 32:
            print("   🟡 Adequate for moderate genomics workloads")
        else:
            print("   🔴 Limited for memory-intensive analysis")
            self.recommendations.append("Upgrade to 32+ GB RAM for genomics databases")
        
        # GPU assessment
        has_nvidia = any(g.get('type') == 'NVIDIA' for g in gpu)
        gpu_memory = max((g.get('memory_mb', 0) for g in gpu), default=0)
        
        gpu_score = 0
        if has_nvidia and gpu_memory >= 12000:
            gpu_score = 10
            print(f"\n🎮 GPU Score: {gpu_score}/10")
            print("   ✅ Excellent CUDA support for GPU-accelerated analysis")
        elif has_nvidia:
            gpu_score = 6
            print(f"\n🎮 GPU Score: {gpu_score}/10") 
            print("   🟡 Good CUDA support, limited by memory")
        else:
            print(f"\n🎮 GPU Score: {gpu_score}/10")
            print("   🔴 No NVIDIA GPU detected")
            self.recommendations.append("Add NVIDIA GPU for CUDA-accelerated genomics")
        
        # Overall assessment
        overall_score = (cpu_score + memory_score + gpu_score) / 3
        
        print(f"\n🎯 Overall BioXen-JCVI Readiness: {overall_score:.1f}/10")
        
        if overall_score >= 8:
            print("   🟢 EXCELLENT - Ready for production genomics workloads")
        elif overall_score >= 6:
            print("   🟡 GOOD - Suitable for moderate genomics analysis")
        elif overall_score >= 4:
            print("   🟠 FAIR - Basic genomics capabilities")
        else:
            print("   🔴 POOR - Significant upgrades needed")
        
        self.assessment['scores'] = {
            'cpu': cpu_score,
            'memory': memory_score,
            'gpu': gpu_score,
            'overall': overall_score
        }
    
    def generate_recommendations(self):
        """Generate specific upgrade recommendations"""
        print("\n🎯 Hardware Upgrade Recommendations:")
        print("=" * 50)
        
        cpu = self.system_info.get('cpu', {})
        memory = self.system_info.get('memory', {})
        gpu = self.system_info.get('gpu', [])
        
        cpu_cores = cpu.get('cores_logical', 0)
        memory_gb = memory.get('total_gb', 0)
        has_nvidia = any(g.get('type') == 'NVIDIA' for g in gpu)
        
        # Priority recommendations
        if cpu_cores < 8:
            print("\n🔴 HIGH PRIORITY: CPU Upgrade")
            print("   Current: {} cores".format(cpu_cores))
            print("   Recommended: AMD Ryzen 7 7700X (8-core) or Ryzen 9 7950X (16-core)")
            print("   Impact: 3-5x faster BLAST and MCscan analysis")
        
        if memory_gb < 32:
            print("\n🔴 HIGH PRIORITY: Memory Upgrade")
            print("   Current: {:.1f} GB".format(memory_gb))
            print("   Recommended: 64GB DDR5 (minimum) or 128GB (optimal)")
            print("   Impact: Enables large genome databases in memory")
        
        if not has_nvidia:
            print("\n🟡 MEDIUM PRIORITY: GPU Addition")
            print("   Current: No NVIDIA GPU detected")
            print("   Recommended: RTX 4070 (12GB) or RTX 4080 (16GB)")
            print("   Impact: 10x faster parallel genomics algorithms")
        
        # Storage recommendations
        storage = self.system_info.get('storage', [])
        has_nvme = any('nvme' in s.get('device', '').lower() for s in storage)
        
        if not has_nvme:
            print("\n🟡 MEDIUM PRIORITY: Storage Upgrade")
            print("   Recommended: 1TB+ NVMe SSD for genome databases")
            print("   Impact: 5-10x faster genome loading and analysis")
        
        # Show budget options
        print("\n💰 Budget-Conscious Upgrades:")
        print("   1. Memory first: 64GB DDR5 (~$400) - biggest immediate impact")
        print("   2. Storage: 1TB NVMe SSD (~$100) - fast genome access")
        print("   3. GPU: RTX 4060 Ti 16GB (~$500) - CUDA acceleration")
        print("   4. CPU: Higher core count (~$300-700) - ultimate performance")
        
        print("\n📋 See HARDWARE_RECOMMENDATIONS.md for complete build guides")
    
    def save_report(self):
        """Save assessment report to file"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_info': self.system_info,
            'assessment': self.assessment,
            'recommendations': self.recommendations
        }
        
        report_file = Path('hardware_assessment_report.json')
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📁 Full report saved: {report_file}")
        
        return report

def main():
    """Run hardware assessment"""
    assessor = BioXenHardwareAssessment()
    
    try:
        assessor.detect_hardware()
        assessor.assess_performance()
        assessor.generate_recommendations()
        assessor.save_report()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Assessment interrupted by user")
    except Exception as e:
        print(f"\n❌ Assessment failed: {e}")

if __name__ == "__main__":
    main()
