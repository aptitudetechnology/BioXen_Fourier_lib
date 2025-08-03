#!/usr/bin/env python3
"""
BioXen Data Export Module
Exports real-time hypervisor data for terminal visualization
"""

import json
import time
import threading
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

# Import BioXen components
import sys
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from hypervisor.core import BioXenHypervisor, VMState
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    sys.exit(1)


class BioXenDataExporter:
    """Exports BioXen hypervisor data to JSON for visualization"""
    
    def __init__(self, hypervisor: BioXenHypervisor, output_file: str = "bioxen_data.json"):
        self.hypervisor = hypervisor
        self.output_file = output_file
        self.running = False
        self.export_thread = None
        self.update_interval = 1.0  # Update every second
        
    def export_vm_data(self, vm_id: str, vm) -> Dict[str, Any]:
        """Export data for a single VM"""
        # Get chassis information for biological context
        chassis_info = self.hypervisor.get_chassis_info()
        
        # Calculate biological metrics
        allocated_ribosomes = vm.resources.ribosomes
        ribosome_utilization = min(95, max(30, allocated_ribosomes * 4))  # Simulate utilization
        
        # Estimate active genes based on ribosome activity
        base_genes = 10 if vm.state == VMState.RUNNING else 3
        active_genes = min(20, max(1, int(base_genes + (ribosome_utilization / 10))))
        
        # Calculate protein synthesis based on activity
        protein_count = int(allocated_ribosomes * 2.5 + active_genes * 1.5)
        mrna_count = max(1, int(active_genes * 0.8))
        
        # Gene expression rate based on ATP and ribosome activity
        atp_level = vm.resources.atp_percentage
        expression_rate = min(95, max(20, int(atp_level * 0.8 + ribosome_utilization * 0.4)))
        
        return {
            "vm_id": vm_id,
            "state": vm.state.value,
            "atp_percentage": int(atp_level),
            "ribosomes": allocated_ribosomes,
            "active_genes": active_genes,
            "protein_count": protein_count,
            "mrna_count": mrna_count,
            "gene_expression_rate": expression_rate,
            "ribosome_utilization": ribosome_utilization,
            "genome_template": vm.genome_template,
            "uptime": time.time() - vm.start_time if vm.start_time else 0,
            "health_status": vm.health_status,
            "memory_usage_kb": vm.resources.memory_kb,
            "priority": vm.resources.priority
        }
    
    def export_system_data(self) -> Dict[str, Any]:
        """Export system-level hypervisor data"""
        system_resources = self.hypervisor.get_system_resources()
        chassis_info = self.hypervisor.get_chassis_info()
        
        # Calculate system metrics
        running_vms = len([vm for vm in self.hypervisor.vms.values() if vm.state == VMState.RUNNING])
        total_allocated_ribosomes = sum(vm.resources.ribosomes for vm in self.hypervisor.vms.values())
        average_atp = sum(vm.resources.atp_percentage for vm in self.hypervisor.vms.values()) / max(len(self.hypervisor.vms), 1)
        
        return {
            "chassis_type": self.hypervisor.chassis_type.value,
            "chassis_id": chassis_info.get("chassis_id", "unknown"),
            "total_ribosomes": self.hypervisor.total_ribosomes,
            "available_ribosomes": self.hypervisor.available_ribosomes,
            "allocated_ribosomes": total_allocated_ribosomes,
            "free_ribosomes": self.hypervisor.available_ribosomes - total_allocated_ribosomes,
            "hypervisor_overhead": self.hypervisor.hypervisor_overhead,
            "max_vms": self.hypervisor.max_vms,
            "active_vms": running_vms,
            "total_vms": len(self.hypervisor.vms),
            "atp_pool": int(average_atp),
            "timestamp": datetime.now().isoformat(),
            "uptime": time.time() - chassis_info.get("initialization_time", time.time())
        }
    
    def export_complete_data(self) -> Dict[str, Any]:
        """Export complete hypervisor state"""
        # Export system data
        system_data = self.export_system_data()
        
        # Export VM data
        vm_data = {}
        for vm_id, vm in self.hypervisor.vms.items():
            vm_data[vm_id] = self.export_vm_data(vm_id, vm)
        
        # Calculate additional system metrics
        if vm_data:
            total_active_genes = sum(vm['active_genes'] for vm in vm_data.values())
            total_proteins = sum(vm['protein_count'] for vm in vm_data.values())
            system_data.update({
                "total_active_genes": total_active_genes,
                "total_proteins": total_proteins
            })
        
        return {
            "system": system_data,
            "vms": vm_data,
            "export_timestamp": datetime.now().isoformat(),
            "data_source": "bioxen_hypervisor_live"
        }
    
    def export_to_file(self) -> bool:
        """Export data to JSON file"""
        try:
            data = self.export_complete_data()
            
            # Write atomically by writing to temp file first
            temp_file = f"{self.output_file}.tmp"
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Rename to final file (atomic on most filesystems)
            Path(temp_file).rename(self.output_file)
            return True
            
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
            return False
    
    def start_continuous_export(self, interval: float = 1.0):
        """Start continuous data export in background thread"""
        self.update_interval = interval
        self.running = True
        
        def export_loop():
            while self.running:
                success = self.export_to_file()
                if success:
                    print(f"📊 Exported BioXen data to {self.output_file}")
                time.sleep(self.update_interval)
        
        self.export_thread = threading.Thread(target=export_loop, daemon=True)
        self.export_thread.start()
        print(f"🚀 Started continuous data export (interval: {interval}s)")
    
    def stop_continuous_export(self):
        """Stop continuous data export"""
        self.running = False
        if self.export_thread:
            self.export_thread.join(timeout=2.0)
        print("⏹️  Stopped continuous data export")


class BioXenVisualizationMonitor:
    """High-level monitor that integrates with existing BioXen systems"""
    
    def __init__(self, hypervisor: BioXenHypervisor):
        self.hypervisor = hypervisor
        self.exporter = BioXenDataExporter(hypervisor)
        
    def start_monitoring(self, export_file: str = "bioxen_data.json", interval: float = 1.0):
        """Start real-time monitoring and data export"""
        self.exporter.output_file = export_file
        self.exporter.start_continuous_export(interval)
        
        print(f"🧬 BioXen Visualization Monitor Started")
        print(f"📁 Data file: {export_file}")
        print(f"⏱️  Update interval: {interval}s")
        print(f"🖥️  Terminal monitor: python3 terminal_biovis.py --data={export_file}")
        
    def stop_monitoring(self):
        """Stop monitoring"""
        self.exporter.stop_continuous_export()
        
    def get_current_data(self) -> Dict[str, Any]:
        """Get current data snapshot"""
        return self.exporter.export_complete_data()


# Utility functions for integration
def add_monitoring_to_hypervisor(hypervisor: BioXenHypervisor, 
                                export_file: str = "bioxen_data.json",
                                auto_start: bool = True,
                                interval: float = 1.0) -> BioXenVisualizationMonitor:
    """Add visualization monitoring to an existing hypervisor"""
    monitor = BioXenVisualizationMonitor(hypervisor)
    
    if auto_start:
        monitor.start_monitoring(export_file, interval)
    
    return monitor


def create_monitored_hypervisor(chassis_type=None, max_vms: int = 4, 
                               export_file: str = "bioxen_data.json",
                               monitor_interval: float = 1.0):
    """Create a new hypervisor with monitoring enabled"""
    from chassis import ChassisType
    
    if chassis_type is None:
        chassis_type = ChassisType.ECOLI
    
    # Create hypervisor
    hypervisor = BioXenHypervisor(max_vms=max_vms, chassis_type=chassis_type)
    
    # Add monitoring
    monitor = add_monitoring_to_hypervisor(
        hypervisor, 
        export_file=export_file,
        auto_start=True,
        interval=monitor_interval
    )
    
    return hypervisor, monitor


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="BioXen Data Export Service")
    parser.add_argument("--output", default="bioxen_data.json", help="Output file path")
    parser.add_argument("--interval", type=float, default=1.0, help="Export interval in seconds")
    parser.add_argument("--max-vms", type=int, default=4, help="Maximum VMs for test hypervisor")
    
    args = parser.parse_args()
    
    print("🧬 Creating test BioXen hypervisor with monitoring...")
    
    # Create monitored hypervisor
    hypervisor, monitor = create_monitored_hypervisor(
        max_vms=args.max_vms,
        export_file=args.output,
        monitor_interval=args.interval
    )
    
    print(f"🚀 BioXen hypervisor running with {args.max_vms} VM slots")
    print(f"📊 Data export to: {args.output}")
    print("🔴 Press Ctrl+C to stop")
    
    try:
        # Keep running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  Stopping BioXen data export...")
        monitor.stop_monitoring()
        print("✅ Stopped successfully")
