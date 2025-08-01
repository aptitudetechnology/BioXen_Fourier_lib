#!/usr/bin/env python3
"""
BioXen GPU Acceleration Test
============================

Tests GPU compute capabilities for accelerated biological simulations.
Focuses on CUDA, OpenCL, and general GPU acceleration for protein folding and genome analysis.
"""

import sys
import time
import json
import subprocess
import platform
from typing import Dict, List, Any, Optional


class GPUCapabilityTester:
    """Test GPU acceleration capabilities for biological computing"""
    
    def __init__(self):
        self.results = {
            "gpu_hardware": {},
            "cuda_support": {},
            "opencl_support": {},
            "compute_libraries": {},
            "performance_tests": {},
            "bioxen_recommendations": []
        }
    
    def detect_nvidia_gpus(self) -> Dict[str, Any]:
        """Detect NVIDIA GPU hardware and capabilities"""
        nvidia_info = {
            "gpus": [],
            "driver_version": None,
            "cuda_version": None,
            "available": False
        }
        
        try:
            # Check nvidia-smi
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,compute_cap,driver_version", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                nvidia_info["available"] = True
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        parts = [p.strip() for p in line.split(',')]
                        if len(parts) >= 4:
                            gpu_info = {
                                "name": parts[0],
                                "memory_mb": int(parts[1]) if parts[1].isdigit() else parts[1],
                                "compute_capability": parts[2],
                                "driver_version": parts[3]
                            }
                            nvidia_info["gpus"].append(gpu_info)
                            if not nvidia_info["driver_version"]:
                                nvidia_info["driver_version"] = parts[3]
        
        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.CalledProcessError):
            pass
        
        # Check CUDA version
        try:
            cuda_result = subprocess.run(
                ["nvcc", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if cuda_result.returncode == 0:
                for line in cuda_result.stdout.split('\n'):
                    if "release" in line:
                        # Extract CUDA version from line like "Cuda compilation tools, release 11.2, V11.2.152"
                        parts = line.split(',')
                        for part in parts:
                            if "release" in part:
                                nvidia_info["cuda_version"] = part.split("release")[1].strip()
                                break
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        return nvidia_info
    
    def test_cuda_support(self) -> Dict[str, Any]:
        """Test CUDA compute support and performance"""
        cuda_info = {
            "available": False,
            "pycuda_available": False,
            "cupy_available": False,
            "performance_test": None
        }
        
        # Test PyCUDA
        try:
            import pycuda.driver as cuda
            import pycuda.autoinit
            import pycuda.gpuarray as gpuarray
            import numpy as np
            
            cuda_info["pycuda_available"] = True
            cuda_info["available"] = True
            
            # Simple performance test - vector addition (genome position operations)
            size = 1000000  # 1M elements (typical for large genomes)
            
            # Create test arrays
            a_cpu = np.random.randn(size).astype(np.float32)
            b_cpu = np.random.randn(size).astype(np.float32)
            
            # GPU computation
            start_time = time.time()
            a_gpu = gpuarray.to_gpu(a_cpu)
            b_gpu = gpuarray.to_gpu(b_cpu)
            result_gpu = a_gpu + b_gpu  # Vector addition
            result_cpu_from_gpu = result_gpu.get()
            gpu_time = time.time() - start_time
            
            # CPU computation for comparison
            start_time = time.time()
            result_cpu = a_cpu + b_cpu
            cpu_time = time.time() - start_time
            
            cuda_info["performance_test"] = {
                "array_size": size,
                "gpu_time_ms": gpu_time * 1000,
                "cpu_time_ms": cpu_time * 1000,
                "speedup": cpu_time / gpu_time if gpu_time > 0 else 0,
                "gpu_memory_transfer_overhead": True
            }
            
        except ImportError:
            cuda_info["pycuda_error"] = "PyCUDA not installed"
        except Exception as e:
            cuda_info["pycuda_error"] = str(e)
        
        # Test CuPy
        try:
            import cupy as cp
            
            cuda_info["cupy_available"] = True
            cuda_info["available"] = True
            
            # CuPy performance test
            size = 100000
            start_time = time.time()
            
            # Simulate protein folding energy calculation
            x_gpu = cp.random.random((size,), dtype=cp.float32)
            y_gpu = cp.random.random((size,), dtype=cp.float32)
            
            # Distance calculations (common in molecular dynamics)
            dist_gpu = cp.sqrt(cp.sum((x_gpu - y_gpu)**2))
            energy_gpu = cp.exp(-dist_gpu)  # Simplified energy function
            
            cp.cuda.Stream.null.synchronize()  # Wait for GPU to finish
            cupy_time = time.time() - start_time
            
            cuda_info["cupy_performance_test"] = {
                "execution_time_ms": cupy_time * 1000,
                "operations": "protein_distance_energy_simulation"
            }
            
        except ImportError:
            cuda_info["cupy_error"] = "CuPy not installed"
        except Exception as e:
            cuda_info["cupy_error"] = str(e)
            
        return cuda_info
    
    def test_opencl_support(self) -> Dict[str, Any]:
        """Test OpenCL compute support"""
        opencl_info = {
            "available": False,
            "platforms": [],
            "devices": [],
            "pyopencl_available": False
        }
        
        try:
            import pyopencl as cl
            
            opencl_info["pyopencl_available"] = True
            opencl_info["available"] = True
            
            # Get platforms and devices
            platforms = cl.get_platforms()
            opencl_info["platform_count"] = len(platforms)
            
            for platform in platforms:
                platform_info = {
                    "name": platform.name,
                    "vendor": platform.vendor,
                    "version": platform.version,
                    "devices": []
                }
                
                devices = platform.get_devices()
                for device in devices:
                    device_info = {
                        "name": device.name,
                        "type": cl.device_type.to_string(device.type),
                        "max_compute_units": device.max_compute_units,
                        "max_work_group_size": device.max_work_group_size,
                        "global_memory_mb": device.global_mem_size // (1024 * 1024),
                        "local_memory_kb": device.local_mem_size // 1024
                    }
                    platform_info["devices"].append(device_info)
                
                opencl_info["platforms"].append(platform_info)
            
            # Simple OpenCL performance test
            if platforms:
                context = cl.Context()
                queue = cl.CommandQueue(context)
                
                # Test kernel for genome sequence analysis
                kernel_source = """
                __kernel void sequence_analysis(__global float* input, 
                                              __global float* output, 
                                              const int size) {
                    int gid = get_global_id(0);
                    if (gid < size) {
                        // Simulate nucleotide scoring
                        output[gid] = sin(input[gid]) * cos(input[gid] * 2.0f);
                    }
                }
                """
                
                program = cl.Program(context, kernel_source).build()
                
                # Test data
                size = 10000
                input_data = cl.array.to_device(queue, 
                    __import__('numpy').random.random(size).astype(__import__('numpy').float32))
                output_data = cl.array.empty_like(input_data)
                
                start_time = time.time()
                program.sequence_analysis(queue, (size,), None, 
                                        input_data.data, output_data.data, 
                                        __import__('numpy').int32(size))
                queue.finish()
                opencl_time = time.time() - start_time
                
                opencl_info["performance_test"] = {
                    "execution_time_ms": opencl_time * 1000,
                    "array_size": size,
                    "kernel_type": "sequence_analysis_simulation"
                }
                
        except ImportError:
            opencl_info["error"] = "PyOpenCL not installed"
        except Exception as e:
            opencl_info["error"] = str(e)
            
        return opencl_info
    
    def test_tensorflow_gpu(self) -> Dict[str, Any]:
        """Test TensorFlow GPU support for machine learning"""
        tf_info = {
            "available": False,
            "gpu_support": False,
            "version": None
        }
        
        try:
            import tensorflow as tf
            
            tf_info["available"] = True
            tf_info["version"] = tf.__version__
            
            # Check GPU availability
            gpus = tf.config.experimental.list_physical_devices('GPU')
            tf_info["gpu_count"] = len(gpus)
            tf_info["gpu_support"] = len(gpus) > 0
            
            if gpus:
                tf_info["gpu_devices"] = []
                for gpu in gpus:
                    gpu_info = {
                        "name": gpu.name,
                        "device_type": gpu.device_type
                    }
                    tf_info["gpu_devices"].append(gpu_info)
                
                # Simple performance test
                start_time = time.time()
                with tf.device('/GPU:0'):
                    # Simulate neural network for protein structure prediction
                    x = tf.random.normal([1000, 100])  # 1000 proteins, 100 features each
                    w = tf.random.normal([100, 50])    # Weight matrix
                    result = tf.matmul(x, w)           # Matrix multiplication
                    result = tf.nn.relu(result)        # Activation function
                
                tf_time = time.time() - start_time
                tf_info["performance_test"] = {
                    "execution_time_ms": tf_time * 1000,
                    "operation": "protein_feature_neural_network"
                }
                
        except ImportError:
            tf_info["error"] = "TensorFlow not installed"
        except Exception as e:
            tf_info["error"] = str(e)
            
        return tf_info
    
    def generate_bioxen_recommendations(self) -> List[str]:
        """Generate BioXen-specific GPU recommendations"""
        recommendations = []
        
        # NVIDIA GPU recommendations
        nvidia_info = self.results.get("gpu_hardware", {})
        if nvidia_info.get("available") and nvidia_info.get("gpus"):
            gpu_count = len(nvidia_info["gpus"])
            recommendations.append(f"Excellent: {gpu_count} NVIDIA GPU(s) detected")
            
            for gpu in nvidia_info["gpus"]:
                memory_gb = int(gpu["memory_mb"]) / 1024 if isinstance(gpu["memory_mb"], int) else 0
                compute_cap = gpu.get("compute_capability", "Unknown")
                
                if memory_gb >= 16:
                    recommendations.append(f"GPU {gpu['name']}: {memory_gb:.1f}GB - excellent for large protein simulations")
                elif memory_gb >= 8:
                    recommendations.append(f"GPU {gpu['name']}: {memory_gb:.1f}GB - good for molecular dynamics") 
                elif memory_gb >= 4:
                    recommendations.append(f"GPU {gpu['name']}: {memory_gb:.1f}GB - suitable for genome processing")
                
                if compute_cap and compute_cap != "Unknown":
                    try:
                        cap_float = float(compute_cap)
                        if cap_float >= 7.0:
                            recommendations.append(f"Compute capability {compute_cap} - optimal for BioXen acceleration")
                        elif cap_float >= 5.0:
                            recommendations.append(f"Compute capability {compute_cap} - good acceleration support")
                    except ValueError:
                        pass
        else:
            recommendations.append("No NVIDIA GPUs detected - CPU-only molecular simulations")
        
        # CUDA recommendations
        cuda_info = self.results.get("cuda_support", {})
        if cuda_info.get("available"):
            if cuda_info.get("cupy_available"):
                recommendations.append("CuPy available - optimal for GPU-accelerated array operations")
            elif cuda_info.get("pycuda_available"):
                recommendations.append("PyCUDA available - custom CUDA kernels supported")
            
            perf_test = cuda_info.get("performance_test")
            if perf_test and perf_test.get("speedup", 0) > 2:
                recommendations.append(f"GPU speedup: {perf_test['speedup']:.1f}x - excellent acceleration")
            elif perf_test:
                recommendations.append("GPU acceleration available but may have memory transfer overhead")
        else:
            recommendations.append("Install CUDA libraries (CuPy/PyCUDA) for GPU acceleration")
        
        # OpenCL recommendations
        opencl_info = self.results.get("opencl_support", {})
        if opencl_info.get("available"):
            platform_count = opencl_info.get("platform_count", 0)
            recommendations.append(f"OpenCL available with {platform_count} platform(s) - cross-vendor GPU support")
        
        # TensorFlow recommendations
        tf_info = self.results.get("compute_libraries", {}).get("tensorflow", {})
        if tf_info.get("gpu_support"):
            recommendations.append("TensorFlow GPU support - excellent for ML-based protein folding")
        elif tf_info.get("available"):
            recommendations.append("TensorFlow available (CPU-only) - consider GPU version for ML acceleration")
        
        return recommendations
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Execute complete GPU capability assessment"""
        print("🎮 Testing GPU acceleration for BioXen...")
        
        # Detect GPU hardware
        nvidia_info = self.detect_nvidia_gpus()
        self.results["gpu_hardware"] = nvidia_info
        
        # Test CUDA support
        cuda_info = self.test_cuda_support()
        self.results["cuda_support"] = cuda_info
        
        # Test OpenCL support
        opencl_info = self.test_opencl_support()
        self.results["opencl_support"] = opencl_info
        
        # Test ML libraries
        tf_info = self.test_tensorflow_gpu()
        self.results["compute_libraries"] = {
            "tensorflow": tf_info
        }
        
        # Generate recommendations
        recommendations = self.generate_bioxen_recommendations()
        self.results["bioxen_recommendations"] = recommendations
        
        return self.results


def main():
    """Main execution function"""
    try:
        tester = GPUCapabilityTester()
        results = tester.run_all_tests()
        
        # Output results as JSON for parent script
        print(json.dumps(results, indent=2))
        
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failed"
        }
        print(json.dumps(error_result, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()