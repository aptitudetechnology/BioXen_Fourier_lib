#!/usr/bin/env python3
"""
BioXen SIMD Extensions Test
===========================

Tests CPU SIMD capabilities for accelerated biological computations.
Focuses on vectorized operations useful for genome processing and protein calculations.
"""

import sys
import time
import json
import platform
import subprocess
from typing import Dict, List, Any, Optional


class SIMDCapabilityTester:
    """Test SIMD extensions and vectorized computation capabilities"""
    
    def __init__(self):
        self.results = {
            "cpu_features": [],
            "simd_extensions": {},
            "performance_tests": {},
            "library_support": {},
            "bioxen_recommendations": []
        }
    
    def detect_cpu_features(self) -> List[str]:
        """Detect CPU SIMD features from system"""
        features = []
        
        if platform.system() == "Linux":
            try:
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if line.startswith("flags"):
                            features = line.split(":")[1].strip().split()
                            break
            except FileNotFoundError:
                pass
        
        # Alternative: use lscpu
        try:
            result = subprocess.run(
                ["lscpu"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if "Flags:" in line:
                        flags = line.split(":", 1)[1].strip().split()
                        features.extend(flags)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
            
        return list(set(features))  # Remove duplicates
    
    def analyze_simd_extensions(self, features: List[str]) -> Dict[str, Any]:
        """Analyze available SIMD extensions"""
        extensions = {
            "sse": False,
            "sse2": False,
            "sse3": False,
            "ssse3": False,
            "sse4_1": False,
            "sse4_2": False,
            "avx": False,
            "avx2": False,
            "avx512f": False,
            "avx512bw": False,
            "avx512cd": False,
            "avx512dq": False,
            "avx512vl": False,
            "fma": False,
            "fma3": False,
            "capabilities": []
        }
        
        # Map CPU flags to SIMD extensions
        flag_mapping = {
            "sse": "sse",
            "sse2": "sse2", 
            "pni": "sse3",  # pni = Prescott New Instructions = SSE3
            "sse3": "sse3",
            "ssse3": "ssse3",
            "sse4_1": "sse4_1",
            "sse4_2": "sse4_2",
            "avx": "avx",
            "avx2": "avx2",
            "avx512f": "avx512f",
            "avx512bw": "avx512bw", 
            "avx512cd": "avx512cd",
            "avx512dq": "avx512dq",
            "avx512vl": "avx512vl",
            "fma": "fma3"
        }
        
        for flag in features:
            if flag.lower() in flag_mapping:
                ext_name = flag_mapping[flag.lower()]
                extensions[ext_name] = True
                extensions["capabilities"].append(ext_name.upper())
        
        # Determine vector widths
        if extensions["avx512f"]:
            extensions["max_vector_width"] = 512
            extensions["max_double_elements"] = 8
            extensions["max_float_elements"] = 16
        elif extensions["avx2"] or extensions["avx"]:
            extensions["max_vector_width"] = 256
            extensions["max_double_elements"] = 4
            extensions["max_float_elements"] = 8
        elif extensions["sse2"]:
            extensions["max_vector_width"] = 128
            extensions["max_double_elements"] = 2
            extensions["max_float_elements"] = 4
        else:
            extensions["max_vector_width"] = 64
            extensions["max_double_elements"] = 1
            extensions["max_float_elements"] = 1
            
        return extensions
    
    def test_numpy_vectorization(self) -> Dict[str, Any]:
        """Test NumPy vectorization performance"""
        try:
            import numpy as np
            
            # Test array sizes relevant to genome data
            test_sizes = [1000, 10000, 100000, 1000000]  # Gene counts for different organisms
            results = {}
            
            for size in test_sizes:
                # Create test arrays (simulating genome position data)
                a = np.random.random(size).astype(np.float32)
                b = np.random.random(size).astype(np.float32)
                
                # Test vectorized operations
                start_time = time.time()
                
                # Simulate typical biological computations
                result1 = np.multiply(a, b)  # Expression correlation
                result2 = np.sqrt(np.add(np.square(a), np.square(b)))  # Distance calculation
                result3 = np.exp(np.negative(a))  # Probability calculations
                
                end_time = time.time()
                
                results[f"size_{size}"] = {
                    "execution_time_ms": (end_time - start_time) * 1000,
                    "operations_per_second": size * 3 / (end_time - start_time),
                    "vectorization_effective": (end_time - start_time) < (size / 1000000)  # Heuristic
                }
            
            return {
                "numpy_available": True,
                "numpy_version": np.__version__,
                "performance_tests": results,
                "blas_info": str(np.__config__.show()) if hasattr(np.__config__, 'show') else "unavailable"
            }
            
        except ImportError:
            return {
                "numpy_available": False,
                "error": "NumPy not installed - critical for BioXen performance"
            }
    
    def test_scipy_optimization(self) -> Dict[str, Any]:
        """Test SciPy optimization capabilities"""
        try:
            import scipy
            import scipy.optimize
            import numpy as np
            
            # Test optimization (protein folding energy minimization simulation)
            def test_function(x):
                """Simulate protein energy function"""
                return np.sum(x**2) + 0.1 * np.sum(np.sin(10 * x))
            
            x0 = np.random.random(100)  # 100-dimensional protein conformation
            
            start_time = time.time()
            result = scipy.optimize.minimize(test_function, x0, method='BFGS')
            end_time = time.time()
            
            return {
                "scipy_available": True,
                "scipy_version": scipy.__version__,
                "optimization_test": {
                    "success": result.success,
                    "iterations": result.nit,
                    "execution_time_ms": (end_time - start_time) * 1000,
                    "final_energy": result.fun
                }
            }
            
        except ImportError:
            return {
                "scipy_available": False,
                "error": "SciPy not available - may limit optimization capabilities"
            }
    
    def test_parallel_processing(self) -> Dict[str, Any]:
        """Test parallel processing capabilities"""
        try:
            import multiprocessing as mp
            import concurrent.futures
            import numpy as np
            
            def cpu_intensive_task(n):
                """Simulate genome analysis task"""
                result = 0
                for i in range(n):
                    result += np.sin(i) * np.cos(i)
                return result
            
            # Test multiprocessing
            cpu_count = mp.cpu_count()
            task_size = 100000
            
            # Sequential execution
            start_time = time.time()
            sequential_results = [cpu_intensive_task(task_size) for _ in range(4)]
            sequential_time = time.time() - start_time
            
            # Parallel execution
            start_time = time.time()
            with concurrent.futures.ProcessPoolExecutor(max_workers=cpu_count) as executor:
                parallel_results = list(executor.map(cpu_intensive_task, [task_size] * 4))
            parallel_time = time.time() - start_time
            
            speedup = sequential_time / parallel_time if parallel_time > 0 else 0
            
            return {
                "multiprocessing_available": True,
                "cpu_count": cpu_count,
                "sequential_time_ms": sequential_time * 1000,
                "parallel_time_ms": parallel_time * 1000,
                "speedup_factor": speedup,
                "efficiency": speedup / min(cpu_count, 4) if cpu_count > 0 else 0
            }
            
        except Exception as e:
            return {
                "multiprocessing_available": False,
                "error": str(e)
            }
    
    def generate_bioxen_recommendations(self, extensions: Dict[str, Any], numpy_results: Dict[str, Any]) -> List[str]:
        """Generate BioXen-specific performance recommendations"""
        recommendations = []
        
        # SIMD recommendations
        if extensions.get("avx512f"):
            recommendations.append("Excellent: AVX-512 available - optimal for large genome vectorization")
        elif extensions.get("avx2"):
            recommendations.append("Very Good: AVX2 available - good performance for genome operations")
        elif extensions.get("avx"):
            recommendations.append("Good: AVX available - decent vectorization performance")
        elif extensions.get("sse4_2"):
            recommendations.append("Moderate: SSE4.2 available - basic vectorization support")
        else:
            recommendations.append("Warning: Limited SIMD support - may impact performance")
        
        # Vector width recommendations
        max_width = extensions.get("max_vector_width", 64)
        if max_width >= 256:
            recommendations.append(f"Vector width {max_width}-bit enables efficient batch genome processing")
        
        # NumPy recommendations
        if numpy_results.get("numpy_available"):
            recommendations.append("NumPy available - essential for BioXen matrix operations")
            
            # Performance analysis
            perf_tests = numpy_results.get("performance_tests", {})
            if "size_100000" in perf_tests:
                ops_per_sec = perf_tests["size_100000"].get("operations_per_second", 0)
                if ops_per_sec > 10000000:  # 10M ops/sec
                    recommendations.append("Excellent vectorization performance for genome-scale operations")
                elif ops_per_sec > 1000000:  # 1M ops/sec
                    recommendations.append("Good vectorization performance for moderate genome datasets")
                else:
                    recommendations.append("Consider optimized BLAS library for better performance")
        else:
            recommendations.append("Critical: Install NumPy for BioXen mathematical operations")
        
        return recommendations
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Execute complete SIMD capability assessment"""
        print("🧬 Testing SIMD capabilities for BioXen...")
        
        # Detect CPU features
        features = self.detect_cpu_features()
        self.results["cpu_features"] = features
        
        # Analyze SIMD extensions
        extensions = self.analyze_simd_extensions(features)
        self.results["simd_extensions"] = extensions
        
        # Test library support
        numpy_results = self.test_numpy_vectorization()
        scipy_results = self.test_scipy_optimization()
        parallel_results = self.test_parallel_processing()
        
        self.results["library_support"] = {
            "numpy": numpy_results,
            "scipy": scipy_results,
            "parallel": parallel_results
        }
        
        # Generate recommendations
        recommendations = self.generate_bioxen_recommendations(extensions, numpy_results)
        self.results["bioxen_recommendations"] = recommendations
        
        return self.results


def main():
    """Main execution function"""
    try:
        tester = SIMDCapabilityTester()
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