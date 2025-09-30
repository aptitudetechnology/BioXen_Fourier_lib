#!/usr/bin/env python3
"""
BioXen Hypervisor CLI - Phase 1.3

Interactive command-line interface for biological VM management.
Focused on hypervisor operations without JCVI dependencies.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List

try:
    import questionary
    from questionary import Choice
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError as e:
    print(f"❌ Missing required dependency: {e}")
    print("Install with: pip install questionary rich")
    sys.exit(1)

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from src.api import (
        create_bio_vm, 
        create_biological_vm,
        BiologicalVM,
        BioResourceManager,
        get_supported_biological_types,
        get_supported_vm_types
    )
except ImportError as e:
    print(f"❌ BioXen API import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    sys.exit(1)

class BioXenHypervisorCLI:
    """Interactive CLI for BioXen hypervisor management."""
    
    def __init__(self):
        self.console = Console()
        self.active_vms: Dict[str, BiologicalVM] = {}
        self.supported_biological_types = get_supported_biological_types()
        self.supported_vm_types = get_supported_vm_types()
    
    def display_header(self):
        """Display application header."""
        header = Panel.fit(
            "[bold blue]🧬 BioXen Hypervisor CLI v0.0.5[/bold blue]\n"
            "[cyan]Biological Virtual Machine Management[/cyan]",
            border_style="blue"
        )
        self.console.print(header)
        self.console.print()
    
    def display_vm_table(self):
        """Display table of active VMs."""
        if not self.active_vms:
            self.console.print("[yellow]No active VMs[/yellow]")
            return
        
        table = Table(title="Active Biological VMs")
        table.add_column("VM ID", style="cyan")
        table.add_column("Type", style="green")
        table.add_column("Biological Type", style="yellow")
        table.add_column("Status", style="magenta")
        
        for vm_id, vm in self.active_vms.items():
            try:
                status = vm.get_status()
                status_str = status.get('status', 'unknown')
            except Exception:
                status_str = 'error'
            
            table.add_row(vm_id, vm.get_vm_type(), vm.get_biological_type(), status_str)
        
        self.console.print(table)
        self.console.print()
    
    def create_vm(self):
        """Create a new biological VM."""
        self.console.print("[bold green]Create Biological VM[/bold green]")
        
        # Get VM ID
        vm_id = questionary.text("Enter VM ID:").ask()
        if not vm_id:
            return
        
        if vm_id in self.active_vms:
            self.console.print(f"[red]VM '{vm_id}' already exists[/red]")
            return
        
        # Select biological type
        biological_type = questionary.select(
            "Select biological type:",
            choices=[Choice(bt, bt) for bt in self.supported_biological_types]
        ).ask()
        
        # Select VM type
        vm_type = questionary.select(
            "Select VM infrastructure type:",
            choices=[Choice(vt, vt) for vt in self.supported_vm_types]
        ).ask()
        
        try:
            # Handle XCP-ng configuration
            config = {}
            if vm_type == "xcpng":
                self.console.print("[yellow]XCP-ng requires additional configuration[/yellow]")
                use_default = questionary.confirm("Use placeholder configuration? (Phase 2 will implement full XCP-ng)").ask()
                if use_default:
                    config = {
                        "xcpng_config": {
                            "xapi_url": "https://xcpng-placeholder:443",
                            "username": "root",
                            "password": "placeholder",
                            "ssh_user": "bioxen"
                        }
                    }
                else:
                    return
            
            # Create VM
            vm = create_bio_vm(vm_id, biological_type, vm_type, config)
            self.active_vms[vm_id] = vm
            self.console.print(f"[green]✅ Created VM '{vm_id}' ({biological_type}, {vm_type})[/green]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Failed to create VM: {e}[/red]")
    
    def start_vm(self):
        """Start a VM."""
        if not self.active_vms:
            self.console.print("[yellow]No VMs available to start[/yellow]")
            return
        
        vm_id = questionary.select(
            "Select VM to start:",
            choices=[Choice(vm_id, vm_id) for vm_id in self.active_vms.keys()]
        ).ask()
        
        if vm_id:
            try:
                vm = self.active_vms[vm_id]
                success = vm.start()
                if success:
                    self.console.print(f"[green]✅ Started VM '{vm_id}'[/green]")
                else:
                    self.console.print(f"[red]❌ Failed to start VM '{vm_id}'[/red]")
            except Exception as e:
                self.console.print(f"[red]❌ Error starting VM: {e}[/red]")
    
    def stop_vm(self):
        """Stop a VM."""
        if not self.active_vms:
            self.console.print("[yellow]No VMs available to stop[/yellow]")
            return
        
        vm_id = questionary.select(
            "Select VM to stop:",
            choices=[Choice(vm_id, vm_id) for vm_id in self.active_vms.keys()]
        ).ask()
        
        if vm_id:
            try:
                vm = self.active_vms[vm_id]
                success = vm.destroy()
                if success:
                    self.console.print(f"[green]✅ Stopped VM '{vm_id}'[/green]")
                else:
                    self.console.print(f"[red]❌ Failed to stop VM '{vm_id}'[/red]")
            except Exception as e:
                self.console.print(f"[red]❌ Error stopping VM: {e}[/red]")
    
    def delete_vm(self):
        """Delete a VM."""
        if not self.active_vms:
            self.console.print("[yellow]No VMs available to delete[/yellow]")
            return
        
        vm_id = questionary.select(
            "Select VM to delete:",
            choices=[Choice(vm_id, vm_id) for vm_id in self.active_vms.keys()]
        ).ask()
        
        if vm_id:
            confirm = questionary.confirm(f"Are you sure you want to delete VM '{vm_id}'?").ask()
            if confirm:
                try:
                    vm = self.active_vms[vm_id]
                    vm.destroy()
                    del self.active_vms[vm_id]
                    self.console.print(f"[green]✅ Deleted VM '{vm_id}'[/green]")
                except Exception as e:
                    self.console.print(f"[red]❌ Error deleting VM: {e}[/red]")
    
    def vm_status(self):
        """Show detailed status of a VM."""
        if not self.active_vms:
            self.console.print("[yellow]No VMs available[/yellow]")
            return
        
        vm_id = questionary.select(
            "Select VM to inspect:",
            choices=[Choice(vm_id, vm_id) for vm_id in self.active_vms.keys()]
        ).ask()
        
        if vm_id:
            try:
                vm = self.active_vms[vm_id]
                status = vm.get_status()
                metrics = vm.get_biological_metrics()
                
                status_panel = Panel(
                    f"[bold]VM Status:[/bold]\n{status}\n\n"
                    f"[bold]Biological Metrics:[/bold]\n{metrics}",
                    title=f"VM: {vm_id}",
                    border_style="green"
                )
                self.console.print(status_panel)
                
            except Exception as e:
                self.console.print(f"[red]❌ Error getting VM status: {e}[/red]")
    
    def resource_management(self):
        """Resource management interface."""
        if not self.active_vms:
            self.console.print("[yellow]No VMs available for resource management[/yellow]")
            return
        
        vm_id = questionary.select(
            "Select VM for resource management:",
            choices=[Choice(vm_id, vm_id) for vm_id in self.active_vms.keys()]
        ).ask()
        
        if vm_id:
            vm = self.active_vms[vm_id]
            
            action = questionary.select(
                "Resource management action:",
                choices=[
                    Choice("View resource usage", "view"),
                    Choice("Allocate ATP", "atp"),
                    Choice("Allocate ribosomes", "ribosomes"),
                    Choice("Back to main menu", "back")
                ]
            ).ask()
            
            try:
                if action == "view":
                    usage = vm.get_resource_usage()
                    self.console.print(f"[cyan]Resource usage for {vm_id}:[/cyan]\n{usage}")
                
                elif action == "atp":
                    atp_amount = questionary.text("Enter ATP allocation (0-100):").ask()
                    if atp_amount and atp_amount.replace('.', '').isdigit():
                        success = vm.allocate_resources({"atp": float(atp_amount)})
                        if success:
                            self.console.print(f"[green]✅ Allocated {atp_amount} ATP to {vm_id}[/green]")
                        else:
                            self.console.print(f"[red]❌ Failed to allocate ATP[/red]")
                
                elif action == "ribosomes":
                    ribosome_count = questionary.text("Enter ribosome count:").ask()
                    if ribosome_count and ribosome_count.isdigit():
                        success = vm.allocate_resources({"ribosomes": int(ribosome_count)})
                        if success:
                            self.console.print(f"[green]✅ Allocated {ribosome_count} ribosomes to {vm_id}[/green]")
                        else:
                            self.console.print(f"[red]❌ Failed to allocate ribosomes[/red]")
                
            except Exception as e:
                self.console.print(f"[red]❌ Resource management error: {e}[/red]")
    
    def run(self):
        """Main CLI loop."""
        self.display_header()
        
        while True:
            self.display_vm_table()
            
            choice = questionary.select(
                "Select an action:",
                choices=[
                    Choice("🏭 Create Biological VM", "create"),
                    Choice("▶️ Start VM", "start"),
                    Choice("⏹️ Stop VM", "stop"),
                    Choice("🗑️ Delete VM", "delete"),
                    Choice("📊 VM Status & Metrics", "status"),
                    Choice("⚙️ Resource Management", "resources"),
                    Choice("🚪 Exit", "exit")
                ]
            ).ask()
            
            if choice == "create":
                self.create_vm()
            elif choice == "start":
                self.start_vm()
            elif choice == "stop":
                self.stop_vm()
            elif choice == "delete":
                self.delete_vm()
            elif choice == "status":
                self.vm_status()
            elif choice == "resources":
                self.resource_management()
            elif choice == "exit":
                self.console.print("[blue]👋 Goodbye![/blue]")
                break
            
            self.console.print()


def main():
    """Main entry point."""
    try:
        cli = BioXenHypervisorCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
