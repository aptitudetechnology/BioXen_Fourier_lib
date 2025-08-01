#!/usr/bin/env python3
"""
Interactive BioXen CLI using questionary for user-friendly genome selection and VM management.
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    import questionary
    from questionary import Choice
except ImportError:
    print("❌ questionary not installed. Install with: pip install questionary")
    sys.exit(1)

try:
    from genome.parser import BioXenRealGenomeIntegrator
    from genome.schema import BioXenGenomeValidator
    from hypervisor.core import BioXenHypervisor, ResourceAllocation
    from chassis import ChassisType, BaseChassis, EcoliChassis, YeastChassis
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    sys.exit(1)

class InteractiveBioXen:
    def __init__(self):
        """Initialize the interactive BioXen interface."""
        self.integrator = BioXenRealGenomeIntegrator()
        self.validator = BioXenGenomeValidator()
        self.hypervisor = None
        self.available_genomes = []
        self.chassis_type = ChassisType.ECOLI  # Default chassis

    def main_menu(self):
        """Display and handle the main menu."""
        while True:
            print("\n" + "="*60)
            print("🧬 BioXen Hypervisor - Interactive Genome Management")
            print("="*60)
            
            choices = [
                Choice("🔍 Select chassis and initialize hypervisor", "init_hypervisor"),
                Choice("📥 Download genomes", "download"),
                Choice("🧬 Validate genomes", "validate"),
                Choice("💾 Create VM", "create_vm"),
                Choice("📊 Show status", "status"),
                Choice("🗑️  Destroy VM", "destroy_vm"),
                Choice("❌ Exit", "exit"),
            ]
            
            action = questionary.select(
                "What would you like to do?",
                choices=choices,
                use_shortcuts=True
            ).ask()
            
            if action is None or action == "exit":
                print("👋 Goodbye!")
                break
            
            try:
                if action == "init_hypervisor":
                    self.initialize_hypervisor()
                elif action == "download":
                    self.download_genomes()
                elif action == "validate":
                    self.validate_genomes()
                elif action == "create_vm":
                    self.create_vm()
                elif action == "status":
                    self.show_status()
                elif action == "destroy_vm":
                    self.destroy_vm()
            except KeyboardInterrupt:
                print("\n\n⚠️  Operation cancelled by user")
                continue
            except Exception as e:
                print(f"\n❌ Error: {e}")
                questionary.press_any_key_to_continue().ask()

    def select_chassis(self):
        """Let user select biological chassis type."""
        print("\n🧬 Select Biological Chassis")
        print("Choose the type of cell to use as your virtual machine chassis:")
        
        chassis_choice = questionary.select(
            "Select chassis type:",
            choices=[
                Choice("🦠 E. coli (Prokaryotic) - Stable, well-tested", ChassisType.ECOLI),
                Choice("🍄 Yeast (Eukaryotic) - PLACEHOLDER - Advanced features", ChassisType.YEAST),
            ]
        ).ask()
        
        if chassis_choice is None:
            return None
            
        if chassis_choice in [ChassisType.ECOLI, ChassisType.YEAST]:
            self.chassis_type = chassis_choice
            
            if chassis_choice == ChassisType.ECOLI:
                print(f"\n✅ Selected E. coli chassis")
                print(f"   • Prokaryotic architecture")
                print(f"   • 80 ribosomes available")
                print(f"   • Up to 4 VMs supported")
                print(f"   • Production-ready implementation")
                
            elif chassis_choice == ChassisType.YEAST:
                print(f"\n⚠️  Selected Yeast chassis (PLACEHOLDER)")
                print(f"   • Eukaryotic architecture")
                print(f"   • 200,000 ribosomes available")
                print(f"   • Organelle support (nucleus, mitochondria, ER)")
                print(f"   • Up to 2 VMs supported")
                print(f"   • ⚠️  PLACEHOLDER - Not fully implemented!")
                
        return chassis_choice

    def initialize_hypervisor(self):
        """Initialize the BioXen hypervisor with chassis selection."""
        if self.hypervisor is not None:
            print("⚠️  Hypervisor is already initialized")
            reinit = questionary.confirm("Do you want to reinitialize with a different chassis?").ask()
            if not reinit:
                return
        
        print("\n🚀 Initializing BioXen Hypervisor")
        
        # Let user select chassis
        selected_chassis = self.select_chassis()
        if selected_chassis is None:
            print("❌ Chassis selection cancelled")
            return
        
        try:
            print(f"\n🔄 Initializing hypervisor with {self.chassis_type.value} chassis...")
            
            if self.chassis_type == ChassisType.ECOLI:
                print("   🦠 Loading E. coli cellular environment...")
                print("   🧬 Configuring prokaryotic gene expression...")
                print("   ⚙️  Setting up ribosome pools...")
                
            elif self.chassis_type == ChassisType.YEAST:
                print("   🍄 Loading Saccharomyces cerevisiae environment...")
                print("   🧬 Configuring eukaryotic gene expression...")
                print("   🏭 Setting up organelle systems...")
                print("   ⚠️  Note: Using PLACEHOLDER implementation")
            
            self.hypervisor = BioXenHypervisor(chassis_type=self.chassis_type)
            
            # Show warning for placeholder implementations
            if self.chassis_type == ChassisType.YEAST:
                print(f"\n⚠️  WARNING: Yeast chassis is currently a PLACEHOLDER implementation")
                print(f"   This chassis provides basic functionality for testing but")
                print(f"   does not include full eukaryotic cellular mechanisms.")
            
            print(f"\n✅ BioXen Hypervisor initialized successfully!")
            print(f"   Chassis: {self.chassis_type.value}")
            print(f"   Status: Ready for genome virtualization")
            
        except Exception as e:
            print(f"❌ Failed to initialize hypervisor: {e}")
        
        questionary.press_any_key_to_continue().ask()

    def download_genomes(self):
        """Download genomes from NCBI with interactive selection."""
        if not self._check_hypervisor():
            return
            
        print("\n📥 Download Genomes from NCBI")
        
        # Predefined interesting genomes with emojis and descriptions
        genome_options = [
            {
                "display": "🦠 E. coli K-12 MG1655 - Classic lab strain",
                "accession": "NC_000913.3",
                "name": "E_coli_K12_MG1655"
            },
            {
                "display": "🍄 S. cerevisiae S288C - Baker's yeast reference",
                "accession": "NC_001133.9", 
                "name": "S_cerevisiae_S288C"
            },
            {
                "display": "🔬 Mycoplasma genitalium - Minimal genome",
                "accession": "NC_000908.2",
                "name": "M_genitalium"
            },
            {
                "display": "🌊 Prochlorococcus marinus - Tiny ocean bacteria",
                "accession": "NC_009840.1",
                "name": "P_marinus"
            },
            {
                "display": "💀 Clostridium botulinum - Botox producer",
                "accession": "NC_009495.1", 
                "name": "C_botulinum"
            },
            {
                "display": "🧪 Custom genome - Enter your own accession",
                "accession": "custom",
                "name": "custom"
            }
        ]
        
        choice = questionary.select(
            "Select a genome to download:",
            choices=[Choice(opt["display"], opt) for opt in genome_options]
        ).ask()
        
        if choice is None:
            return
            
        if choice["accession"] == "custom":
            accession = questionary.text("Enter NCBI accession number (e.g., NC_000913.3):").ask()
            if not accession:
                return
            name = questionary.text("Enter a name for this genome:").ask()
            if not name:
                name = accession.replace(".", "_")
        else:
            accession = choice["accession"]
            name = choice["name"]
        
        print(f"\n🔄 Downloading {accession}...")
        
        try:
            genome_data = self.integrator.download_genome(accession)
            if genome_data:
                # Add to available genomes
                self.available_genomes.append({
                    "accession": accession,
                    "name": name,
                    "data": genome_data
                })
                print(f"✅ Successfully downloaded {name}")
                print(f"   Accession: {accession}")
                print(f"   Size: {len(genome_data):,} base pairs")
            else:
                print(f"❌ Failed to download {accession}")
        except Exception as e:
            print(f"❌ Error downloading genome: {e}")
        
        questionary.press_any_key_to_continue().ask()

    def validate_genomes(self):
        """Validate downloaded genomes."""
        if not self._check_hypervisor():
            return
            
        if not self.available_genomes:
            print("❌ No genomes available. Download some genomes first.")
            questionary.press_any_key_to_continue().ask()
            return
        
        print("\n🧬 Validate Genomes")
        
        # Show available genomes
        genome_choices = [
            Choice(f"{g['name']} ({g['accession']})", g) 
            for g in self.available_genomes
        ]
        genome_choices.append(Choice("🔍 Validate all genomes", "all"))
        
        choice = questionary.select(
            "Select genome(s) to validate:",
            choices=genome_choices
        ).ask()
        
        if choice is None:
            return
        
        genomes_to_validate = self.available_genomes if choice == "all" else [choice]
        
        print(f"\n🔄 Validating {len(genomes_to_validate)} genome(s)...")
        
        for genome in genomes_to_validate:
            print(f"\n📋 Validating {genome['name']}...")
            try:
                is_valid = self.validator.validate_genome(genome['data'])
                if is_valid:
                    print(f"   ✅ {genome['name']} - Valid genome structure")
                else:
                    print(f"   ❌ {genome['name']} - Invalid genome structure")
            except Exception as e:
                print(f"   ❌ {genome['name']} - Validation error: {e}")
        
        questionary.press_any_key_to_continue().ask()

    def create_vm(self):
        """Create a new VM with genome selection."""
        if not self._check_hypervisor():
            return
            
        if not self.available_genomes:
            print("❌ No genomes available. Download some genomes first.")
            questionary.press_any_key_to_continue().ask()
            return
        
        print("\n💾 Create Virtual Machine")
        
        # Select genome
        genome_choices = [
            Choice(f"{g['name']} ({g['accession']}) - {len(g['data']):,} bp", g) 
            for g in self.available_genomes
        ]
        
        selected_genome = questionary.select(
            "Select genome for the VM:",
            choices=genome_choices
        ).ask()
        
        if selected_genome is None:
            return
        
        # Get VM name
        vm_name = questionary.text(
            "Enter VM name:",
            default=f"vm_{selected_genome['name']}"
        ).ask()
        
        if not vm_name:
            return
        
        # Resource allocation
        print("\n⚙️  Resource Allocation")
        memory_mb = questionary.text(
            "Memory allocation (MB):",
            default="512"
        ).ask()
        
        if not memory_mb:
            return
        
        try:
            memory_mb = int(memory_mb)
        except ValueError:
            print("❌ Invalid memory value")
            questionary.press_any_key_to_continue().ask()
            return
        
        print(f"\n🔄 Creating VM '{vm_name}'...")
        print(f"   Genome: {selected_genome['name']} ({selected_genome['accession']})")
        print(f"   Memory: {memory_mb} MB")
        print(f"   Chassis: {self.chassis_type.value}")
        
        try:
            allocation = ResourceAllocation(
                memory_mb=memory_mb,
                ribosomes=20  # Default ribosome allocation
            )
            
            vm_id = self.hypervisor.create_vm(vm_name, selected_genome['data'], allocation)
            if vm_id:
                print(f"✅ VM created successfully!")
                print(f"   VM ID: {vm_id}")
                print(f"   Name: {vm_name}")
                print(f"   Status: Ready")
            else:
                print(f"❌ Failed to create VM")
        except Exception as e:
            print(f"❌ Error creating VM: {e}")
        
        questionary.press_any_key_to_continue().ask()

    def show_status(self):
        """Display hypervisor and VM status."""
        print("\n📊 BioXen System Status")
        print("="*50)
        
        if self.hypervisor:
            print(f"\nHypervisor Status: ✅ Running")
            print(f"Chassis Type: {self.chassis_type.value}")
            
            # Get chassis info
            if self.chassis_type == ChassisType.ECOLI:
                print(f"Architecture: Prokaryotic")
                print(f"Available Ribosomes: 80")
                print(f"Maximum VMs: 4")
            elif self.chassis_type == ChassisType.YEAST:
                print(f"Architecture: Eukaryotic")
                print(f"Available Ribosomes: 200,000")
                print(f"Maximum VMs: 2")
                print(f"Organelles: Nucleus, Mitochondria, ER")
            
            # VM information
            vm_count = len(self.hypervisor.vms)
            print(f"\nVirtual Machines: {vm_count}")
            
            if vm_count > 0:
                print(f"\nVM Details:")
                for vm_id, vm in self.hypervisor.vms.items():
                    status_emoji = "🟢" if hasattr(vm, 'status') and vm.status == "running" else "🔴"
                    memory = vm.allocation.memory_mb if hasattr(vm, 'allocation') else "Unknown"
                    ribosomes = vm.allocation.ribosomes if hasattr(vm, 'allocation') else "Unknown"
                    
                    print(f"  {status_emoji} {vm.name} (ID: {vm_id})")
                    print(f"    Memory: {memory} MB")
                    print(f"    Ribosomes: {ribosomes}")
                    print(f"    Genome size: {len(vm.genome_data):,} bp")
            
            # Resource utilization
            total_memory = sum(vm.allocation.memory_mb for vm in self.hypervisor.vms.values() if hasattr(vm, 'allocation'))
            total_ribosomes = sum(vm.allocation.ribosomes for vm in self.hypervisor.vms.values() if hasattr(vm, 'allocation'))
            
            print(f"\nResource Utilization:")
            print(f"  Memory: {total_memory:,} MB")
            print(f"  Ribosomes: {total_ribosomes}")
            
            # VM state breakdown
            if vm_count > 0:
                states = {}
                for vm in self.hypervisor.vms.values():
                    state = getattr(vm, 'status', 'unknown')
                    states[state] = states.get(state, 0) + 1
                
                if states:
                    print(f"\nVM States:")
                    for state, count in states.items():
                        emoji = {"running": "🟢", "paused": "🟡", "stopped": "🔴", "created": "🔵"}.get(state, "⚪")
                        print(f"  {emoji} {state.title()}: {count}")
            
            # Show warning for placeholder implementations
            if self.chassis_type == ChassisType.YEAST:
                print(f"\n⚠️  Note: Yeast chassis is currently a PLACEHOLDER implementation")
        else:
            print(f"\nHypervisor Status: ❌ Not initialized")
            print(f"Use 'Select chassis and initialize hypervisor' to start")
        
        # Genome information
        print(f"\nAvailable Genomes: {len(self.available_genomes)}")
        if self.available_genomes:
            for genome in self.available_genomes:
                print(f"  📁 {genome['name']} ({genome['accession']}) - {len(genome['data']):,} bp")
        
        questionary.press_any_key_to_continue().ask()

    def destroy_vm(self):
        """Destroy a VM."""
        if not self._check_hypervisor():
            return
            
        if not self.hypervisor.vms:
            print("❌ No VMs available to destroy.")
            questionary.press_any_key_to_continue().ask()
            return
        
        print("\n🗑️  Destroy Virtual Machine")
        
        vm_choices = [
            Choice(f"{vm.name} (ID: {vm_id})", vm_id) 
            for vm_id, vm in self.hypervisor.vms.items()
        ]
        
        vm_id = questionary.select(
            "Select VM to destroy:",
            choices=vm_choices
        ).ask()
        
        if vm_id is None:
            return
        
        vm_name = self.hypervisor.vms[vm_id].name
        
        confirm = questionary.confirm(
            f"Are you sure you want to destroy VM '{vm_name}'? This cannot be undone."
        ).ask()
        
        if not confirm:
            print("❌ VM destruction cancelled")
            questionary.press_any_key_to_continue().ask()
            return
        
        print(f"\n🔄 Destroying VM '{vm_name}'...")
        
        try:
            success = self.hypervisor.destroy_vm(vm_id)
            if success:
                print(f"✅ VM '{vm_name}' destroyed successfully")
            else:
                print(f"❌ Failed to destroy VM '{vm_name}'")
        except Exception as e:
            print(f"❌ Error destroying VM: {e}")
        
        questionary.press_any_key_to_continue().ask()

    def _check_hypervisor(self):
        """Check if hypervisor is initialized."""
        if self.hypervisor is None:
            print("❌ Hypervisor not initialized. Please initialize it first.")
            questionary.press_any_key_to_continue().ask()
            return False
        return True

def main():
    """Main entry point."""
    try:
        app = InteractiveBioXen()
        app.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
