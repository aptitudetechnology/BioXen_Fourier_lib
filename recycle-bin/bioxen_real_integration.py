#!/usr/bin/env python3
"""
BioXen Real Data Integration Example
Shows how to integrate terminal visualization with existing BioXen code
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from hypervisor.core import BioXenHypervisor, ResourceAllocation, VMState
    from chassis import ChassisType
    from bioxen_data_export import BioXenVisualizationMonitor, add_monitoring_to_hypervisor
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    print("Files needed: src/hypervisor/core.py, src/chassis/, bioxen_data_export.py")
    sys.exit(1)


def demo_real_bioxen_with_visualization():
    """Demonstrate BioXen with real-time terminal visualization"""
    
    print("🧬 BioXen Real Data Integration Demo")
    print("=" * 50)
    
    # 1. Create BioXen hypervisor (your existing code)
    print("📡 Initializing BioXen hypervisor...")
    hypervisor = BioXenHypervisor(max_vms=4, chassis_type=ChassisType.ECOLI)
    
    # 2. Add visualization monitoring
    print("📊 Adding real-time data export...")
    monitor = add_monitoring_to_hypervisor(
        hypervisor, 
        export_file="bioxen_live_data.json",
        auto_start=True,
        interval=0.5  # Update every 500ms for responsive visualization
    )
    
    # 3. Create some VMs (your existing workflow)
    print("🦠 Creating virtual machines...")
    
    # VM 1: High-performance VM
    high_perf_resources = ResourceAllocation(
        ribosomes=20,
        atp_percentage=30.0,
        rna_polymerase=15,
        memory_kb=150,
        priority=3
    )
    hypervisor.create_vm("vm_protein_synthesis", "syn3a_minimal", high_perf_resources)
    hypervisor.start_vm("vm_protein_synthesis")
    
    # VM 2: Research VM
    research_resources = ResourceAllocation(
        ribosomes=15,
        atp_percentage=25.0,
        rna_polymerase=12,
        memory_kb=120,
        priority=2
    )
    hypervisor.create_vm("vm_research", "custom_genome", research_resources)
    hypervisor.start_vm("vm_research")
    
    # VM 3: Low-priority background VM
    background_resources = ResourceAllocation(
        ribosomes=8,
        atp_percentage=15.0,
        rna_polymerase=6,
        memory_kb=80,
        priority=1
    )
    hypervisor.create_vm("vm_background", "minimal_genome", background_resources)
    hypervisor.start_vm("vm_background")
    
    print("✅ BioXen setup complete!")
    print()
    print("🖥️  Terminal Visualization Commands:")
    print("   python3 terminal_biovis.py --data=bioxen_live_data.json")
    print("   python3 terminal_biovis.py --data=bioxen_live_data.json --refresh=2.0")
    print()
    print("📊 Current System Status:")
    status = hypervisor.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    print()
    print("🔴 Press Ctrl+C to stop the demo")
    
    try:
        import time
        # Let it run and export data
        while True:
            # You could add your normal BioXen operations here
            # The monitor will continuously export data in the background
            time.sleep(1)
            
            # Optional: Print live stats
            current_data = monitor.get_current_data()
            running_vms = current_data['system']['active_vms']
            total_genes = current_data['system'].get('total_active_genes', 0)
            print(f"📈 Live: {running_vms} VMs running, {total_genes} active genes transcribing")
            
    except KeyboardInterrupt:
        print("\n⏹️  Stopping demo...")
        monitor.stop_monitoring()
        print("✅ Demo stopped successfully")


def create_integration_helper():
    """Create helper function to add to your existing BioXen code"""
    
    integration_code = '''
# Add this to your existing interactive_bioxen.py or main BioXen script:

from bioxen_data_export import add_monitoring_to_hypervisor

class InteractiveBioXen:
    def __init__(self):
        # ... your existing initialization ...
        self.visualization_monitor = None
    
    def enable_terminal_visualization(self, export_file="bioxen_data.json", interval=1.0):
        """Enable real-time terminal visualization"""
        if self.hypervisor and not self.visualization_monitor:
            self.visualization_monitor = add_monitoring_to_hypervisor(
                self.hypervisor,
                export_file=export_file,
                auto_start=True,
                interval=interval
            )
            print(f"🖥️  Terminal visualization enabled!")
            print(f"📊 Run: python3 terminal_biovis.py --data={export_file}")
            return True
        return False
    
    def disable_terminal_visualization(self):
        """Disable terminal visualization"""
        if self.visualization_monitor:
            self.visualization_monitor.stop_monitoring()
            self.visualization_monitor = None
            print("⏹️  Terminal visualization disabled")
'''
    
    print("🔧 Integration Helper Code:")
    print(integration_code)
    
    # Write to file
    with open("integration_helper.py", "w") as f:
        f.write(integration_code)
    print("💾 Saved to integration_helper.py")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="BioXen Real Data Integration")
    parser.add_argument("--demo", action="store_true", help="Run interactive demo")
    parser.add_argument("--helper", action="store_true", help="Generate integration helper code")
    
    args = parser.parse_args()
    
    if args.demo:
        demo_real_bioxen_with_visualization()
    elif args.helper:
        create_integration_helper()
    else:
        print("Usage:")
        print("  python3 bioxen_real_integration.py --demo    # Run live demo")
        print("  python3 bioxen_real_integration.py --helper  # Generate integration code")
