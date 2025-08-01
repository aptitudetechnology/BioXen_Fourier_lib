"""
Command Line Interface for BioXen Hypervisor

This provides a simple CLI for managing biological virtual machines.
"""

import argparse
import json
import sys
from typing import Dict, Any

from ..hypervisor.core import BioXenHypervisor, ResourceAllocation, VMState
from ..genome.syn3a import VMImageBuilder
from ..genetics.circuits import BioCompiler

class BioXenCLI:
    """Command line interface for BioXen hypervisor"""
    
    def __init__(self):
        self.hypervisor = BioXenHypervisor()
        self.vm_builder = VMImageBuilder()
        self.compiler = BioCompiler()
        
    def run(self):
        """Main CLI entry point"""
        parser = self._create_parser()
        args = parser.parse_args()
        
        if hasattr(args, 'func'):
            args.func(args)
        else:
            parser.print_help()
    
    def _create_parser(self):
        """Create the argument parser"""
        parser = argparse.ArgumentParser(
            description="BioXen - Biological Hypervisor for JCVI-Syn3A",
            prog="bioxen"
        )
        
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # VM management commands
        self._add_vm_commands(subparsers)
        
        # System commands
        self._add_system_commands(subparsers)
        
        # Development commands
        self._add_dev_commands(subparsers)
        
        return parser
    
    def _add_vm_commands(self, subparsers):
        """Add VM management commands"""
        
        # Create VM
        create_parser = subparsers.add_parser('create', help='Create a new VM')
        create_parser.add_argument('vm_id', help='Unique VM identifier')
        create_parser.add_argument('--genome', default='syn3a_minimal', 
                                 help='Genome template to use')
        create_parser.add_argument('--ribosomes', type=int, default=20,
                                 help='Number of ribosomes to allocate')
        create_parser.add_argument('--atp', type=float, default=25.0,
                                 help='ATP percentage to allocate')
        create_parser.add_argument('--memory', type=int, default=120,
                                 help='Memory in KB to allocate')
        create_parser.set_defaults(func=self.cmd_create_vm)
        
        # Start VM
        start_parser = subparsers.add_parser('start', help='Start a VM')
        start_parser.add_argument('vm_id', help='VM to start')
        start_parser.set_defaults(func=self.cmd_start_vm)
        
        # Stop VM
        stop_parser = subparsers.add_parser('stop', help='Stop a VM')
        stop_parser.add_argument('vm_id', help='VM to stop')
        stop_parser.set_defaults(func=self.cmd_stop_vm)
        
        # Pause VM
        pause_parser = subparsers.add_parser('pause', help='Pause a VM')
        pause_parser.add_argument('vm_id', help='VM to pause')
        pause_parser.set_defaults(func=self.cmd_pause_vm)
        
        # Resume VM
        resume_parser = subparsers.add_parser('resume', help='Resume a VM')
        resume_parser.add_argument('vm_id', help='VM to resume')
        resume_parser.set_defaults(func=self.cmd_resume_vm)
        
        # Destroy VM
        destroy_parser = subparsers.add_parser('destroy', help='Destroy a VM')
        destroy_parser.add_argument('vm_id', help='VM to destroy')
        destroy_parser.set_defaults(func=self.cmd_destroy_vm)
        
        # List VMs
        list_parser = subparsers.add_parser('list', help='List all VMs')
        list_parser.set_defaults(func=self.cmd_list_vms)
        
        # VM Status
        status_parser = subparsers.add_parser('status', help='Get VM status')
        status_parser.add_argument('vm_id', help='VM to check')
        status_parser.set_defaults(func=self.cmd_vm_status)
    
    def _add_system_commands(self, subparsers):
        """Add system management commands"""
        
        # System resources
        resources_parser = subparsers.add_parser('resources', help='Show system resources')
        resources_parser.set_defaults(func=self.cmd_system_resources)
        
        # Run scheduler
        schedule_parser = subparsers.add_parser('schedule', help='Run scheduler iteration')
        schedule_parser.set_defaults(func=self.cmd_run_scheduler)
    
    def _add_dev_commands(self, subparsers):
        """Add development commands"""
        
        # Build VM image
        build_parser = subparsers.add_parser('build-image', help='Build VM image')
        build_parser.add_argument('vm_id', help='VM identifier')
        build_parser.add_argument('--config', help='VM config file (JSON)')
        build_parser.add_argument('--output', help='Output file for VM image')
        build_parser.set_defaults(func=self.cmd_build_image)
        
        # Compile hypervisor
        compile_parser = subparsers.add_parser('compile', help='Compile hypervisor DNA')
        compile_parser.add_argument('--config', required=True, help='Hypervisor config file')
        compile_parser.add_argument('--output', required=True, help='Output DNA sequences file')
        compile_parser.set_defaults(func=self.cmd_compile)
    
    # VM Management Commands
    
    def cmd_create_vm(self, args):
        """Create a new VM"""
        resources = ResourceAllocation(
            ribosomes=args.ribosomes,
            atp_percentage=args.atp,
            memory_kb=args.memory
        )
        
        success = self.hypervisor.create_vm(args.vm_id, args.genome, resources)
        if success:
            print(f"✓ Created VM '{args.vm_id}'")
        else:
            print(f"✗ Failed to create VM '{args.vm_id}'")
            sys.exit(1)
    
    def cmd_start_vm(self, args):
        """Start a VM"""
        success = self.hypervisor.start_vm(args.vm_id)
        if success:
            print(f"✓ Started VM '{args.vm_id}'")
        else:
            print(f"✗ Failed to start VM '{args.vm_id}'")
            sys.exit(1)
    
    def cmd_stop_vm(self, args):
        """Stop a VM"""
        success = self.hypervisor.pause_vm(args.vm_id)  # Pause for now
        if success:
            print(f"✓ Stopped VM '{args.vm_id}'")
        else:
            print(f"✗ Failed to stop VM '{args.vm_id}'")
            sys.exit(1)
    
    def cmd_pause_vm(self, args):
        """Pause a VM"""
        success = self.hypervisor.pause_vm(args.vm_id)
        if success:
            print(f"✓ Paused VM '{args.vm_id}'")
        else:
            print(f"✗ Failed to pause VM '{args.vm_id}'")
            sys.exit(1)
    
    def cmd_resume_vm(self, args):
        """Resume a VM"""
        success = self.hypervisor.resume_vm(args.vm_id)
        if success:
            print(f"✓ Resumed VM '{args.vm_id}'")
        else:
            print(f"✗ Failed to resume VM '{args.vm_id}'")
            sys.exit(1)
    
    def cmd_destroy_vm(self, args):
        """Destroy a VM"""
        success = self.hypervisor.destroy_vm(args.vm_id)
        if success:
            print(f"✓ Destroyed VM '{args.vm_id}'")
        else:
            print(f"✗ Failed to destroy VM '{args.vm_id}'")
            sys.exit(1)
    
    def cmd_list_vms(self, args):
        """List all VMs"""
        vms = self.hypervisor.list_vms()
        
        if not vms:
            print("No VMs found")
            return
        
        print("VM ID          State      Ribosomes  ATP%   Memory(KB)  Uptime")
        print("-" * 65)
        
        for vm in vms:
            uptime = f"{vm['uptime_seconds']:.0f}s" if vm['uptime_seconds'] > 0 else "0s"
            print(f"{vm['vm_id']:<14} {vm['state']:<10} {vm['ribosome_allocation']:<9} "
                  f"{vm['atp_percentage']:<6.1f} {vm['memory_kb']:<10} {uptime}")
    
    def cmd_vm_status(self, args):
        """Get detailed VM status"""
        status = self.hypervisor.get_vm_status(args.vm_id)
        
        if not status:
            print(f"VM '{args.vm_id}' not found")
            sys.exit(1)
        
        print(f"VM Status: {args.vm_id}")
        print(f"  State: {status['state']}")
        print(f"  Uptime: {status['uptime_seconds']:.0f} seconds")
        print(f"  CPU Time: {status['cpu_time_used']:.1f} seconds")
        print(f"  Resources:")
        print(f"    Ribosomes: {status['ribosome_allocation']}")
        print(f"    ATP: {status['atp_percentage']:.1f}%")
        print(f"    Memory: {status['memory_kb']} KB")
        print(f"  Health: {status['health_status']}")
        print(f"  Priority: {status['priority']}")
    
    # System Commands
    
    def cmd_system_resources(self, args):
        """Show system resources"""
        resources = self.hypervisor.get_system_resources()
        
        print("BioXen System Resources")
        print(f"  Total Ribosomes: {resources['total_ribosomes']}")
        print(f"  Available Ribosomes: {resources['available_ribosomes']}")
        print(f"  Allocated Ribosomes: {resources['allocated_ribosomes']}")
        print(f"  Free Ribosomes: {resources['free_ribosomes']}")
        print(f"  Total ATP Allocated: {resources['total_atp_allocated']:.1f}%")
        print(f"  Hypervisor Overhead: {resources['hypervisor_overhead']:.1%}")
        print(f"  Active VMs: {resources['active_vms']}")
    
    def cmd_run_scheduler(self, args):
        """Run one scheduler iteration"""
        self.hypervisor.run_scheduler()
        print("✓ Scheduler iteration completed")
    
    # Development Commands
    
    def cmd_build_image(self, args):
        """Build VM image"""
        config = {}
        if args.config:
            with open(args.config, 'r') as f:
                config = json.load(f)
        
        vm_image = self.vm_builder.build_vm_image(args.vm_id, config)
        
        if args.output:
            self.vm_builder.save_vm_image(vm_image, args.output)
            print(f"✓ VM image saved to {args.output}")
        else:
            print(f"✓ Built VM image for '{args.vm_id}'")
            print(f"  Genome: {vm_image['genome'].genome_id}")
            print(f"  Genes: {len(vm_image['genome'].genes)}")
            print(f"  Size: {vm_image['genome'].total_size} bp")
    
    def cmd_compile(self, args):
        """Compile hypervisor DNA sequences"""
        with open(args.config, 'r') as f:
            config = json.load(f)
        
        vm_configs = config.get('vms', [])
        sequences = self.compiler.compile_hypervisor(vm_configs)
        
        with open(args.output, 'w') as f:
            json.dump(sequences, f, indent=2)
        
        print(f"✓ Hypervisor DNA compiled to {args.output}")
        print(f"  Generated {len(sequences)} sequences")


def main():
    """Main entry point"""
    cli = BioXenCLI()
    cli.run()


if __name__ == "__main__":
    main()
