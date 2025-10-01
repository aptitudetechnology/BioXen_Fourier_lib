"""
Performance monitoring and profiling for BioXen hypervisor

This module provides tools for monitoring resource usage, scheduling fairness,
and identifying performance bottlenecks in the biological hypervisor.

Enhanced with four-lens analysis capabilities (v2.1):
- Fourier (Lomb-Scargle) for rhythm detection
- Wavelet for transient event detection
- Laplace for stability assessment
- Z-Transform for noise filtering
"""

import time
import threading
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics
import numpy as np

@dataclass
class ResourceMetrics:
    """Resource usage metrics for a time period"""
    timestamp: float
    ribosome_utilization: float  # 0-100%
    atp_level: float             # 0-100%
    memory_usage: float          # 0-100%
    active_vms: int
    context_switches: int

@dataclass
class VMMetrics:
    """Per-VM performance metrics"""
    vm_id: str
    cpu_time: float              # Total CPU time allocated
    wait_time: float             # Time spent waiting for resources
    context_switches: int        # Number of context switches
    resource_violations: int     # Times resource limits were exceeded
    health_score: float          # Overall health (0-100)

@dataclass
class SchedulingMetrics:
    """Scheduling fairness and performance metrics"""
    total_time_quantum: float
    vm_allocations: Dict[str, float]  # VM -> time allocated
    fairness_score: float       # How fair the allocation was (0-100)
    average_wait_time: float
    max_wait_time: float

class PerformanceProfiler:
    """
    Real-time performance profiler for BioXen hypervisor
    
    Enhanced with four-lens analysis capabilities (v2.1):
    - Analyzes time-series metrics (ATP, ribosome utilization, etc.)
    - Detects circadian rhythms via Fourier analysis
    - Identifies transient events via Wavelet analysis
    - Assesses system stability via Laplace analysis
    - Filters noise via Z-Transform analysis
    """
    
    def __init__(self, hypervisor, monitoring_interval: float = 5.0):
        self.hypervisor = hypervisor
        self.monitoring_interval = monitoring_interval
        self.running = False
        self.monitor_thread = None
        
        # Metrics storage
        self.system_metrics: deque = deque(maxlen=1000)  # Last 1000 samples
        self.vm_metrics: Dict[str, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.scheduling_metrics: deque = deque(maxlen=100)
        
        # Performance counters
        self.context_switch_count = 0
        self.last_context_switch_time = time.time()
        self.resource_contention_events = 0
        
        # ✅ NEW: Four-lens analyzer integration (v2.1)
        try:
            from ..analysis.system_analyzer import SystemAnalyzer
            self.analyzer = SystemAnalyzer(sampling_rate=1.0/monitoring_interval)
            self._analysis_enabled = True
        except ImportError:
            self.analyzer = None
            self._analysis_enabled = False
        
    def start_monitoring(self):
        """Start the performance monitoring thread"""
        if self.running:
            return
            
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop the performance monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.running:
            try:
                # Collect system metrics
                self._collect_system_metrics()
                
                # Collect VM metrics
                self._collect_vm_metrics()
                
                # Analyze scheduling performance
                self._analyze_scheduling()
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                print(f"Monitoring error: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_system_metrics(self):
        """Collect system-level performance metrics"""
        current_time = time.time()
        
        # Get system resources
        resources = self.hypervisor.get_system_resources()
        
        # Calculate utilization
        ribosome_util = (resources['allocated_ribosomes'] / 
                        resources['available_ribosomes'] * 100)
        
        # Simulate ATP and memory monitoring (would be real biosensors)
        atp_level = self._simulate_atp_level()
        memory_usage = self._simulate_memory_usage()
        
        metrics = ResourceMetrics(
            timestamp=current_time,
            ribosome_utilization=ribosome_util,
            atp_level=atp_level,
            memory_usage=memory_usage,
            active_vms=resources['active_vms'],
            context_switches=self.context_switch_count
        )
        
        self.system_metrics.append(metrics)
    
    def _collect_vm_metrics(self):
        """Collect per-VM performance metrics"""
        vms = self.hypervisor.list_vms()
        
        for vm_data in vms:
            vm_id = vm_data['vm_id']
            
            # Calculate derived metrics
            health_score = self._calculate_health_score(vm_data)
            wait_time = self._calculate_wait_time(vm_id)
            violations = self._count_resource_violations(vm_id)
            
            metrics = VMMetrics(
                vm_id=vm_id,
                cpu_time=vm_data['cpu_time_used'],
                wait_time=wait_time,
                context_switches=self._get_vm_context_switches(vm_id),
                resource_violations=violations,
                health_score=health_score
            )
            
            self.vm_metrics[vm_id].append(metrics)
    
    def _analyze_scheduling(self):
        """Analyze scheduling fairness and performance"""
        if len(self.vm_metrics) < 2:
            return  # Need at least 2 VMs to analyze fairness
        
        # Calculate time allocations
        vm_allocations = {}
        total_cpu_time = 0
        
        for vm_id, metrics_deque in self.vm_metrics.items():
            if metrics_deque:
                latest_metric = metrics_deque[-1]
                vm_allocations[vm_id] = latest_metric.cpu_time
                total_cpu_time += latest_metric.cpu_time
        
        # Calculate fairness score (how close to equal allocation)
        if total_cpu_time > 0:
            num_vms = len(vm_allocations)
            expected_share = total_cpu_time / num_vms
            
            fairness_score = 0
            for allocation in vm_allocations.values():
                deviation = abs(allocation - expected_share) / expected_share
                fairness_score += (1 - min(deviation, 1))
            
            fairness_score = (fairness_score / num_vms) * 100
        else:
            fairness_score = 100
        
        # Calculate wait times
        wait_times = []
        for metrics_deque in self.vm_metrics.values():
            if metrics_deque:
                wait_times.append(metrics_deque[-1].wait_time)
        
        avg_wait = statistics.mean(wait_times) if wait_times else 0
        max_wait = max(wait_times) if wait_times else 0
        
        scheduling_metrics = SchedulingMetrics(
            total_time_quantum=self.monitoring_interval,
            vm_allocations=vm_allocations,
            fairness_score=fairness_score,
            average_wait_time=avg_wait,
            max_wait_time=max_wait
        )
        
        self.scheduling_metrics.append(scheduling_metrics)
    
    def get_performance_report(self) -> Dict:
        """Generate a comprehensive performance report"""
        if not self.system_metrics:
            return {"error": "No metrics collected yet"}
        
        # System performance summary
        recent_metrics = list(self.system_metrics)[-10:]  # Last 10 samples
        
        avg_ribosome_util = statistics.mean([m.ribosome_utilization for m in recent_metrics])
        avg_atp_level = statistics.mean([m.atp_level for m in recent_metrics])
        avg_memory_usage = statistics.mean([m.memory_usage for m in recent_metrics])
        
        # VM performance summary
        vm_summary = {}
        for vm_id, metrics_deque in self.vm_metrics.items():
            if metrics_deque:
                recent_vm_metrics = list(metrics_deque)[-10:]
                avg_health = statistics.mean([m.health_score for m in recent_vm_metrics])
                total_violations = sum([m.resource_violations for m in recent_vm_metrics])
                
                vm_summary[vm_id] = {
                    "average_health": avg_health,
                    "total_violations": total_violations,
                    "current_cpu_time": recent_vm_metrics[-1].cpu_time,
                    "current_wait_time": recent_vm_metrics[-1].wait_time
                }
        
        # Scheduling performance
        scheduling_summary = {}
        if self.scheduling_metrics:
            recent_sched = list(self.scheduling_metrics)[-5:]  # Last 5 samples
            avg_fairness = statistics.mean([s.fairness_score for s in recent_sched])
            avg_wait = statistics.mean([s.average_wait_time for s in recent_sched])
            
            scheduling_summary = {
                "average_fairness_score": avg_fairness,
                "average_wait_time": avg_wait,
                "context_switches_per_minute": self._calculate_context_switch_rate()
            }
        
        return {
            "timestamp": time.time(),
            "monitoring_duration": len(self.system_metrics) * self.monitoring_interval,
            "system_performance": {
                "average_ribosome_utilization": avg_ribosome_util,
                "average_atp_level": avg_atp_level,
                "average_memory_usage": avg_memory_usage,
                "resource_contention_events": self.resource_contention_events
            },
            "vm_performance": vm_summary,
            "scheduling_performance": scheduling_summary,
            "bottlenecks": self._identify_bottlenecks(),
            "recommendations": self._generate_recommendations()
        }
    
    def _identify_bottlenecks(self) -> List[str]:
        """Identify performance bottlenecks"""
        bottlenecks = []
        
        if not self.system_metrics:
            return bottlenecks
        
        recent_metrics = list(self.system_metrics)[-10:]
        
        # Check for resource saturation
        avg_ribosome_util = statistics.mean([m.ribosome_utilization for m in recent_metrics])
        if avg_ribosome_util > 80:
            bottlenecks.append("High ribosome utilization (>80%)")
        
        avg_atp = statistics.mean([m.atp_level for m in recent_metrics])
        if avg_atp < 30:
            bottlenecks.append("Low ATP levels (<30%)")
        
        avg_memory = statistics.mean([m.memory_usage for m in recent_metrics])
        if avg_memory > 85:
            bottlenecks.append("High memory usage (>85%)")
        
        # Check scheduling fairness
        if self.scheduling_metrics:
            recent_fairness = [s.fairness_score for s in list(self.scheduling_metrics)[-5:]]
            avg_fairness = statistics.mean(recent_fairness)
            if avg_fairness < 70:
                bottlenecks.append("Poor scheduling fairness (<70%)")
        
        # Check context switch frequency
        switch_rate = self._calculate_context_switch_rate()
        if switch_rate > 2:  # More than 2 switches per minute
            bottlenecks.append("High context switch frequency")
        
        return bottlenecks
    
    def _generate_recommendations(self) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        bottlenecks = self._identify_bottlenecks()
        
        if "High ribosome utilization (>80%)" in bottlenecks:
            recommendations.append("Consider reducing VM count or ribosome allocation per VM")
        
        if "Low ATP levels (<30%)" in bottlenecks:
            recommendations.append("Implement ATP throttling or pause non-essential VMs")
        
        if "High memory usage (>85%)" in bottlenecks:
            recommendations.append("Enable more aggressive garbage collection")
        
        if "Poor scheduling fairness (<70%)" in bottlenecks:
            recommendations.append("Adjust scheduling algorithm or time quantum")
        
        if "High context switch frequency" in bottlenecks:
            recommendations.append("Increase time quantum to reduce context switch overhead")
        
        # VM-specific recommendations
        for vm_id, metrics_deque in self.vm_metrics.items():
            if metrics_deque:
                latest = metrics_deque[-1]
                if latest.health_score < 60:
                    recommendations.append(f"Investigate health issues in VM {vm_id}")
                if latest.resource_violations > 5:
                    recommendations.append(f"Review resource allocation for VM {vm_id}")
        
        return recommendations
    
    def record_context_switch(self):
        """Record a context switch event"""
        self.context_switch_count += 1
        self.last_context_switch_time = time.time()
    
    def record_resource_contention(self):
        """Record a resource contention event"""
        self.resource_contention_events += 1
    
    # Helper methods for simulation (would be replaced with real biosensors)
    
    def _simulate_atp_level(self) -> float:
        """Simulate ATP level monitoring"""
        # In real implementation, this would read from ATP biosensors
        base_level = 80.0
        variation = (time.time() % 60) / 60 * 20  # 20% variation over 60 seconds
        return max(0, min(100, base_level + variation - 10))
    
    def _simulate_memory_usage(self) -> float:
        """Simulate memory usage monitoring"""
        # Based on number of active VMs and their allocations
        total_allocated = sum(
            vm_data['memory_kb'] 
            for vm_data in self.hypervisor.list_vms()
            if vm_data['state'] == 'running'
        )
        total_available = 1000  # Assume 1MB total available
        return (total_allocated / total_available) * 100
    
    def _calculate_health_score(self, vm_data: Dict) -> float:
        """Calculate health score for a VM"""
        # Simple health calculation based on uptime and state
        if vm_data['state'] == 'running':
            base_score = 90
        elif vm_data['state'] == 'paused':
            base_score = 70
        else:
            base_score = 30
        
        # Adjust based on uptime
        uptime_hours = vm_data['uptime_seconds'] / 3600
        if uptime_hours > 24:  # Penalize very long uptimes
            base_score -= min(20, (uptime_hours - 24) * 2)
        
        return max(0, min(100, base_score))
    
    def _calculate_wait_time(self, vm_id: str) -> float:
        """Calculate current wait time for a VM"""
        # Simplified calculation
        return max(0, time.time() - self.last_context_switch_time - 30)
    
    def _count_resource_violations(self, vm_id: str) -> int:
        """Count resource violations for a VM"""
        # Simplified - in real implementation would track actual violations
        return 0
    
    def _get_vm_context_switches(self, vm_id: str) -> int:
        """Get context switch count for a VM"""
        # Simplified - would track per-VM context switches
        return self.context_switch_count // len(self.hypervisor.vms) if self.hypervisor.vms else 0
    
    def _calculate_context_switch_rate(self) -> float:
        """Calculate context switches per minute"""
        if len(self.system_metrics) < 2:
            return 0
        
        time_span = self.system_metrics[-1].timestamp - self.system_metrics[0].timestamp
        if time_span == 0:
            return 0
        
        return (self.context_switch_count / time_span) * 60  # Per minute


class BenchmarkSuite:
    """Benchmark suite for testing hypervisor performance"""
    
    def __init__(self, hypervisor):
        self.hypervisor = hypervisor
        self.results = {}
    
    def run_single_vm_benchmark(self) -> Dict:
        """Test single VM performance (Phase 1)"""
        print("Running single VM benchmark...")
        
        # Create and start a single VM
        start_time = time.time()
        self.hypervisor.create_vm("benchmark_vm1", "syn3a_minimal")
        self.hypervisor.start_vm("benchmark_vm1")
        
        # Monitor for 60 seconds
        profiler = PerformanceProfiler(self.hypervisor, monitoring_interval=1.0)
        profiler.start_monitoring()
        
        time.sleep(60)
        
        profiler.stop_monitoring()
        end_time = time.time()
        
        # Calculate overhead
        report = profiler.get_performance_report()
        overhead = 100 - report['system_performance']['average_ribosome_utilization']
        
        # Cleanup
        self.hypervisor.destroy_vm("benchmark_vm1")
        
        result = {
            "test_duration": end_time - start_time,
            "hypervisor_overhead": overhead,
            "average_health": report['vm_performance'].get('benchmark_vm1', {}).get('average_health', 0),
            "bottlenecks": report['bottlenecks'],
            "success_criteria": overhead < 20  # Less than 20% overhead
        }
        
        self.results['single_vm'] = result
        return result
    
    def run_dual_vm_benchmark(self) -> Dict:
        """Test dual VM performance (Phase 2)"""
        print("Running dual VM benchmark...")
        
        start_time = time.time()
        
        # Create two VMs
        self.hypervisor.create_vm("benchmark_vm1", "syn3a_minimal")
        self.hypervisor.create_vm("benchmark_vm2", "syn3a_minimal")
        
        # Start both VMs
        self.hypervisor.start_vm("benchmark_vm1")
        self.hypervisor.start_vm("benchmark_vm2")
        
        # Monitor with profiler
        profiler = PerformanceProfiler(self.hypervisor, monitoring_interval=1.0)
        profiler.start_monitoring()
        
        # Run scheduler for 120 seconds
        for _ in range(120):
            self.hypervisor.run_scheduler()
            time.sleep(1)
        
        profiler.stop_monitoring()
        end_time = time.time()
        
        report = profiler.get_performance_report()
        
        # Check fairness
        fairness_score = report['scheduling_performance'].get('average_fairness_score', 0)
        
        # Cleanup
        self.hypervisor.destroy_vm("benchmark_vm1")
        self.hypervisor.destroy_vm("benchmark_vm2")
        
        result = {
            "test_duration": end_time - start_time,
            "fairness_score": fairness_score,
            "average_wait_time": report['scheduling_performance'].get('average_wait_time', 0),
            "context_switches": report['scheduling_performance'].get('context_switches_per_minute', 0),
            "bottlenecks": report['bottlenecks'],
            "success_criteria": fairness_score > 80  # Good fairness
        }
        
        self.results['dual_vm'] = result
        return result
    
    def run_stress_test(self) -> Dict:
        """Test maximum VM capacity (Phase 3)"""
        print("Running stress test with maximum VMs...")
        
        start_time = time.time()
        
        # Create maximum number of VMs
        created_vms = []
        for i in range(4):  # Maximum VMs
            vm_id = f"stress_vm{i+1}"
            if self.hypervisor.create_vm(vm_id, "syn3a_minimal"):
                created_vms.append(vm_id)
                self.hypervisor.start_vm(vm_id)
        
        # Monitor under stress
        profiler = PerformanceProfiler(self.hypervisor, monitoring_interval=1.0)
        profiler.start_monitoring()
        
        # Run for 180 seconds with scheduling
        for _ in range(180):
            self.hypervisor.run_scheduler()
            time.sleep(1)
        
        profiler.stop_monitoring()
        end_time = time.time()
        
        report = profiler.get_performance_report()
        
        # Cleanup
        for vm_id in created_vms:
            self.hypervisor.destroy_vm(vm_id)
        
        result = {
            "test_duration": end_time - start_time,
            "max_vms_created": len(created_vms),
            "system_stability": len(report['bottlenecks']) == 0,
            "resource_utilization": report['system_performance']['average_ribosome_utilization'],
            "bottlenecks": report['bottlenecks'],
            "success_criteria": len(created_vms) >= 3 and len(report['bottlenecks']) <= 2
        }
        
        self.results['stress_test'] = result
        return result
    
    def generate_benchmark_report(self) -> str:
        """Generate a comprehensive benchmark report"""
        if not self.results:
            return "No benchmark results available"
        
    
    # ========== FOUR-LENS ANALYSIS METHODS (v2.1) ==========
    
    def extract_time_series(self, metric_name: str = 'atp_level') -> Tuple[np.ndarray, np.ndarray]:
        """
        Extract time series from stored metrics for analysis.
        
        Args:
            metric_name: Metric to extract ('atp_level', 'ribosome_utilization', 
                        'memory_usage', 'active_vms', 'context_switches')
        
        Returns:
            (values, timestamps) tuple as numpy arrays
        
        Example:
            >>> values, timestamps = profiler.extract_time_series('atp_level')
            >>> print(f"Collected {len(values)} samples over {timestamps[-1]-timestamps[0]:.1f}s")
        """
        timestamps = []
        values = []
        
        for metric in self.system_metrics:
            if hasattr(metric, metric_name):
                timestamps.append(metric.timestamp)
                values.append(getattr(metric, metric_name))
        
        return np.array(values), np.array(timestamps)
    
    def analyze_metric_fourier(self, metric_name: str = 'atp_level') -> Dict[str, Any]:
        """
        Analyze a metric using Fourier lens (Lomb-Scargle).
        
        Detects periodic rhythms in the metric time series.
        
        Args:
            metric_name: Metric to analyze
        
        Returns:
            FourierResult or error dictionary
        
        Example:
            >>> result = profiler.analyze_metric_fourier('atp_level')
            >>> if 20 < result.dominant_period < 28:
            ...     print("Circadian rhythm detected!")
        """
        if not self._analysis_enabled or not self.analyzer:
            return {'error': 'Analysis not enabled', 'hint': 'SystemAnalyzer not available'}
        
        values, timestamps = self.extract_time_series(metric_name)
        
        if len(values) < 50:
            return {'error': 'Insufficient data', 'samples': len(values), 'required': 50}
        
        try:
            return self.analyzer.fourier_lens(values, timestamps)
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_metric_wavelet(self, metric_name: str = 'atp_level') -> Dict[str, Any]:
        """
        Analyze a metric using Wavelet lens.
        
        Detects transient events and time-localized features.
        
        Args:
            metric_name: Metric to analyze
        
        Returns:
            WaveletResult or error dictionary
        
        Example:
            >>> result = profiler.analyze_metric_wavelet('atp_level')
            >>> print(f"Detected {len(result.transient_events)} stress responses")
        """
        if not self._analysis_enabled or not self.analyzer:
            return {'error': 'Analysis not enabled', 'hint': 'SystemAnalyzer not available'}
        
        values, _ = self.extract_time_series(metric_name)
        
        if len(values) < 64:
            return {'error': 'Insufficient data', 'samples': len(values), 'required': 64}
        
        try:
            return self.analyzer.wavelet_lens(values)
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_metric_laplace(self, metric_name: str = 'atp_level') -> Dict[str, Any]:
        """
        Analyze a metric using Laplace lens.
        
        Assesses system stability based on pole locations.
        
        Args:
            metric_name: Metric to analyze
        
        Returns:
            LaplaceResult or error dictionary
        
        Example:
            >>> result = profiler.analyze_metric_laplace('atp_level')
            >>> if result.stability == 'unstable':
            ...     print("WARNING: System homeostasis compromised!")
        """
        if not self._analysis_enabled or not self.analyzer:
            return {'error': 'Analysis not enabled', 'hint': 'SystemAnalyzer not available'}
        
        values, _ = self.extract_time_series(metric_name)
        
        if len(values) < 50:
            return {'error': 'Insufficient data', 'samples': len(values), 'required': 50}
        
        try:
            return self.analyzer.laplace_lens(values)
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_metric_ztransform(self, metric_name: str = 'atp_level') -> Dict[str, Any]:
        """
        Analyze a metric using Z-Transform lens (digital filtering).
        
        Removes noise while preserving signal features.
        
        Args:
            metric_name: Metric to analyze
        
        Returns:
            ZTransformResult or error dictionary
        
        Example:
            >>> result = profiler.analyze_metric_ztransform('atp_level')
            >>> clean_signal = result.filtered_signal
            >>> print(f"Noise reduced by {result.noise_reduction_percent:.1f}%")
        """
        if not self._analysis_enabled or not self.analyzer:
            return {'error': 'Analysis not enabled', 'hint': 'SystemAnalyzer not available'}
        
        values, _ = self.extract_time_series(metric_name)
        
        if len(values) < 50:
            return {'error': 'Insufficient data', 'samples': len(values), 'required': 50}
        
        try:
            return self.analyzer.z_transform_lens(values)
        except Exception as e:
            return {'error': str(e)}
    
    def analyze_metric_all(self, metric_name: str = 'atp_level') -> Dict[str, Any]:
        """
        Apply all four lenses to a metric.
        
        Provides comprehensive analysis with:
        - Fourier: Detect periodic rhythms
        - Wavelet: Detect transient events
        - Laplace: Assess system stability
        - Z-Transform: Filter noise
        
        Args:
            metric_name: Metric to analyze
        
        Returns:
            Dictionary with results from all lenses or error information
        
        Example:
            >>> results = profiler.analyze_metric_all('atp_level')
            >>> print(f"Period: {results['fourier'].dominant_period:.1f}h")
            >>> print(f"Events: {len(results['wavelet'].transient_events)}")
            >>> print(f"Stability: {results['laplace'].stability}")
            >>> print(f"Noise reduction: {results['ztransform'].noise_reduction_percent:.1f}%")
        """
        if not self._analysis_enabled or not self.analyzer:
            return {
                'error': 'Analysis not enabled',
                'hint': 'SystemAnalyzer not available - check imports'
            }
        
        values, timestamps = self.extract_time_series(metric_name)
        
        # Validate signal
        validation = self.analyzer.validate_signal(values)
        if not validation['all_passed']:
            return {
                'error': 'Validation failed',
                'checks': validation,
                'samples': len(values),
                'hint': 'Signal quality issues detected'
            }
        
        results = {
            'validation': validation,
            'metric': metric_name,
            'samples': len(values),
            'duration_seconds': timestamps[-1] - timestamps[0] if len(timestamps) > 0 else 0
        }
        
        # Apply all lenses
        try:
            results['fourier'] = self.analyzer.fourier_lens(values, timestamps)
            results['wavelet'] = self.analyzer.wavelet_lens(values)
            results['laplace'] = self.analyzer.laplace_lens(values)
            results['ztransform'] = self.analyzer.z_transform_lens(values)
        except Exception as e:
            results['error'] = str(e)
            import traceback
            results['traceback'] = traceback.format_exc()
        
        return results
        
        report = ["BioXen Hypervisor Benchmark Report", "=" * 40, ""]
        
        for test_name, result in self.results.items():
            report.append(f"{test_name.upper()} TEST:")
            report.append(f"  Duration: {result['test_duration']:.1f}s")
            
            if 'hypervisor_overhead' in result:
                report.append(f"  Hypervisor Overhead: {result['hypervisor_overhead']:.1f}%")
            
            if 'fairness_score' in result:
                report.append(f"  Fairness Score: {result['fairness_score']:.1f}%")
            
            if 'max_vms_created' in result:
                report.append(f"  Max VMs: {result['max_vms_created']}")
            
            success = "✓ PASS" if result['success_criteria'] else "✗ FAIL"
            report.append(f"  Result: {success}")
            
            if result['bottlenecks']:
                report.append(f"  Bottlenecks: {', '.join(result['bottlenecks'])}")
            
            report.append("")
        
        return "\n".join(report)
