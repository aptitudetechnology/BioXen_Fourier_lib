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
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    sys.exit(1)

class InteractiveBioXen:
    """Interactive BioXen interface using questionary."""
    
    def __init__(self):
        self.hypervisor = None
        self.available_genomes = {}
        self.loaded_genomes = {}
        self.active_vms = {}
        
    def start(self):
        """Start the interactive BioXen session."""
        print("🧬 Welcome to BioXen Interactive Interface")
        print("=" * 50)
        
        # Scan for available genomes
        self.scan_available_genomes()
        
        # Main menu loop
        while True:
            action = questionary.select(
                "What would you like to do?",
                choices=[
                    Choice("🔍 Browse Available Genomes", "browse"),
                    Choice("🧬 Load Genome for Analysis", "load"),
                    Choice("🖥️  Initialize Hypervisor", "init_hypervisor"),
                    Choice("⚡ Create Virtual Machine", "create_vm"),
                    Choice("📊 Manage Running VMs", "manage_vms"),
                    Choice("📈 View System Status", "status"),
                    Choice("💾 Download New Genomes", "download"),
                    Choice("❌ Exit", "exit")
                ]
            ).ask()
            
            if action == "exit":
                print("\n👋 Thanks for using BioXen!")
                break
            elif action == "browse":
                self.browse_genomes()
            elif action == "load":
                self.load_genome()
            elif action == "init_hypervisor":
                self.initialize_hypervisor()
            elif action == "create_vm":
                self.create_virtual_machine()
            elif action == "manage_vms":
                self.manage_vms()
            elif action == "status":
                self.show_status()
            elif action == "download":
                self.download_genomes()
    
    def scan_available_genomes(self):
        """Scan for available genome files."""
        genomes_dir = Path("genomes")
        if not genomes_dir.exists():
            genomes_dir.mkdir()
            return
        
        genome_files = list(genomes_dir.glob("*.genome"))
        json_files = list(genomes_dir.glob("*.json"))
        
        for genome_file in genome_files:
            try:
                # Quick validation
                is_valid, errors = BioXenGenomeValidator.validate_file(genome_file)
                
                # For real genomes, we'll be more permissive
                # Consider a genome "usable" if it has structural validity even with warnings
                has_critical_errors = any('invalid format' in str(error).lower() or 
                                        'missing required' in str(error).lower() or
                                        'cannot parse' in str(error).lower() 
                                        for error in errors)
                
                is_usable = is_valid or not has_critical_errors
                
                # Try to get metadata from corresponding JSON file
                json_file = genomes_dir / f"{genome_file.stem}.json"
                metadata = {}
                if json_file.exists():
                    import json
                    with open(json_file, 'r') as f:
                        metadata = json.load(f)
                
                self.available_genomes[genome_file.stem] = {
                    'file': genome_file,
                    'valid': is_valid,
                    'usable': is_usable,  # New field for real genome support
                    'errors': errors,
                    'metadata': metadata
                }
                
                if not is_valid and is_usable:
                    print(f"⚠️  {genome_file.stem}: {len(errors)} validation warnings (still usable)")
                    
            except Exception as e:
                print(f"⚠️  Warning: Could not scan {genome_file.name}: {e}")
    
    def browse_genomes(self):
        """Browse available genomes with details."""
        if not self.available_genomes:
            print("📁 No genome files found in 'genomes/' directory")
            print("   Use 'Download New Genomes' to get some, or add .genome files manually")
            return
        
        print("\n🧬 Available Genomes:")
        print("=" * 60)
        
        for name, info in self.available_genomes.items():
            if info['valid']:
                status = "✅ Valid"
            elif info['usable']:
                status = "⚠️  Usable (with warnings)"
            else:
                status = "❌ Invalid"
                
            print(f"\n{status} - {name}")
            
            if info['metadata']:
                meta = info['metadata']
                print(f"   📋 Organism: {meta.get('organism', 'Unknown')}")
                print(f"   📏 Size: {meta.get('genome_size', 0):,} bp")
                print(f"   🧬 Genes: {meta.get('total_genes', 0)}")
                print(f"   ⚡ Essential: {meta.get('essential_genes', 0)}")
                print(f"   🔬 Minimal: {'Yes' if meta.get('minimal_genome', False) else 'No'}")
            else:
                print(f"   📁 File: {info['file'].name}")
            
            if not info['valid'] and info['errors']:
                warning_count = len(info['errors'])
                print(f"   ⚠️  {warning_count} validation warnings (mostly gene overlaps - normal for real genomes)")
        
        questionary.press_any_key_to_continue().ask()
    
    def load_genome(self):
        """Load a genome for analysis."""
        if not self.available_genomes:
            print("❌ No genomes available. Use 'Download New Genomes' first.")
            return
        
        # Filter to usable genomes (valid OR usable with warnings)
        usable_genomes = {k: v for k, v in self.available_genomes.items() if v.get('usable', v['valid'])}
        
        if not usable_genomes:
            print("❌ No usable genomes found. Check validation errors in 'Browse Genomes'.")
            return
        
        choices = []
        for name, info in usable_genomes.items():
            meta = info['metadata']
            organism = meta.get('organism', name) if meta else name
            genes = f" ({meta.get('total_genes', '?')} genes)" if meta else ""
            
            # Add status indicator
            if info['valid']:
                status = "✅ "
            elif info.get('usable', False):
                status = "⚠️  "
            else:
                status = ""
                
            choices.append(Choice(f"{status}{organism}{genes}", name))
        
        selected = questionary.select(
            "Which genome would you like to load?",
            choices=choices
        ).ask()
        
        if not selected:
            return
        
        try:
            print(f"\n📊 Loading {selected}...")
            
            genome_file = self.available_genomes[selected]['file']
            integrator = BioXenRealGenomeIntegrator(genome_file)
            real_genome = integrator.load_genome()
            stats = integrator.get_genome_stats()
            
            self.loaded_genomes[selected] = {
                'integrator': integrator,
                'genome': real_genome,
                'stats': stats
            }
            
            print(f"✅ Successfully loaded {stats['organism']}")
            print(f"   📏 Genome size: {stats['genome_length_bp']:,} bp")
            print(f"   🧬 Total genes: {stats['total_genes']}")
            print(f"   ⚡ Essential genes: {stats['essential_genes']} ({stats['essential_percentage']:.1f}%)")
            print(f"   📦 Coding density: {stats['coding_density']:.1f}%")
            
            # Show gene categories
            print(f"\n🔬 Gene categories:")
            for category, count in stats['gene_categories'].items():
                print(f"   {category.replace('_', ' ').title()}: {count}")
            
            # Show validation status
            genome_info = self.available_genomes[selected]
            if not genome_info['valid'] and genome_info.get('usable', False):
                print(f"\n⚠️  Note: This genome has {len(genome_info['errors'])} validation warnings")
                print(f"   (mostly gene overlaps - common in real bacterial genomes)")
            
            questionary.press_any_key_to_continue().ask()
            
        except Exception as e:
            print(f"❌ Failed to load genome: {e}")
            import traceback
            traceback.print_exc()
    
    def initialize_hypervisor(self):
        """Initialize the BioXen hypervisor with user configuration."""
        print("\n🖥️  Initializing BioXen Hypervisor")
        print("=" * 40)
        
        # Get hypervisor configuration
        max_vms = questionary.text(
            "Maximum number of VMs (default: 4):",
            default="4"
        ).ask()
        
        total_ribosomes = questionary.text(
            "Total ribosomes available (default: 80):",
            default="80"
        ).ask()
        
        try:
            max_vms = int(max_vms)
            total_ribosomes = int(total_ribosomes)
            
            self.hypervisor = BioXenHypervisor(
                max_vms=max_vms,
                total_ribosomes=total_ribosomes
            )
            
            print(f"✅ Hypervisor initialized:")
            print(f"   🖥️  Max VMs: {max_vms}")
            print(f"   🧬 Ribosomes: {total_ribosomes}")
            print(f"   📊 Status: Ready")
            
            questionary.press_any_key_to_continue().ask()
            
        except ValueError as e:
            print(f"❌ Invalid configuration: {e}")
    
    def create_virtual_machine(self):
        """Create a virtual machine with interactive configuration."""
        if not self.hypervisor:
            print("❌ Hypervisor not initialized. Use 'Initialize Hypervisor' first.")
            return
        
        if not self.loaded_genomes:
            print("❌ No genomes loaded. Use 'Load Genome for Analysis' first.")
            return
        
        print("\n⚡ Creating Virtual Machine")
        print("=" * 35)
        
        # Select genome
        genome_choices = []
        for name, info in self.loaded_genomes.items():
            stats = info['stats']
            organism = stats['organism']
            essential = stats['essential_genes']
            genome_choices.append(Choice(f"{organism} ({essential} essential genes)", name))
        
        selected_genome = questionary.select(
            "Which genome should the VM use?",
            choices=genome_choices
        ).ask()
        
        if not selected_genome:
            return
        
        # Get VM configuration
        vm_id = questionary.text(
            "VM ID (unique identifier):",
            default=f"vm_{len(self.active_vms) + 1}"
        ).ask()
        
        if vm_id in self.active_vms:
            print(f"❌ VM '{vm_id}' already exists!")
            return
        
        # Get resource allocation based on genome requirements
        genome_info = self.loaded_genomes[selected_genome]
        template = genome_info['integrator'].create_vm_template()
        
        print(f"\n📊 Genome requirements:")
        print(f"   💾 Min memory: {template['min_memory_kb']} KB")
        print(f"   🔧 Min CPU: {template['min_cpu_percent']}%")
        print(f"   ⏱️  Boot time: {template['boot_time_ms']} ms")
        
        # Resource allocation with smart defaults
        memory_kb = questionary.text(
            f"Memory allocation in KB (min: {template['min_memory_kb']}):",
            default=str(template['min_memory_kb'] * 2)
        ).ask()
        
        atp_percentage = questionary.text(
            "ATP percentage (10-50%):",
            default="25"
        ).ask()
        
        ribosomes = questionary.text(
            "Ribosome allocation (5-40):",
            default="20"
        ).ask()
        
        priority = questionary.select(
            "VM Priority:",
            choices=[
                Choice("🔵 Low (1)", "1"),
                Choice("🟡 Normal (2)", "2"),
                Choice("🟠 High (3)", "3"),
                Choice("🔴 Critical (4)", "4")
            ]
        ).ask()
        
        try:
            # Create resource allocation
            resources = ResourceAllocation(
                memory_kb=int(memory_kb),
                atp_percentage=float(atp_percentage),
                ribosomes=int(ribosomes),
                rna_polymerase=10,
                priority=int(priority)
            )
            
            # Validate resources meet minimum requirements
            if resources.memory_kb < template['min_memory_kb']:
                print(f"⚠️  Warning: Memory below minimum requirement ({template['min_memory_kb']} KB)")
                proceed = questionary.confirm("Continue anyway?").ask()
                if not proceed:
                    return
            
            # Create VM
            success = self.hypervisor.create_vm(
                vm_id=vm_id,
                genome_template=selected_genome,
                resource_allocation=resources
            )
            
            if success:
                self.active_vms[vm_id] = {
                    'genome': selected_genome,
                    'resources': resources,
                    'template': template
                }
                
                print(f"\n✅ Virtual Machine '{vm_id}' created successfully!")
                print(f"   🧬 Genome: {genome_info['stats']['organism']}")
                print(f"   💾 Memory: {resources.memory_kb} KB")
                print(f"   🧬 Ribosomes: {resources.ribosomes}")
                print(f"   ⚡ ATP: {resources.atp_percentage}%")
                print(f"   🎯 Priority: {resources.priority}")
                
                # Ask if user wants to start the VM
                start_now = questionary.confirm("Start the VM now?").ask()
                if start_now:
                    self.hypervisor.start_vm(vm_id)
                    print(f"🚀 VM '{vm_id}' started!")
                
            else:
                print(f"❌ Failed to create VM '{vm_id}'")
            
            questionary.press_any_key_to_continue().ask()
            
        except ValueError as e:
            print(f"❌ Invalid resource configuration: {e}")
    
    def manage_vms(self):
        """Manage running virtual machines."""
        if not self.hypervisor:
            print("❌ Hypervisor not initialized.")
            return
        
        if not self.hypervisor.vms:
            print("📭 No VMs exist. Use 'Create Virtual Machine' first.")
            return
        
        # Show current VMs
        print("\n🖥️  Virtual Machine Management")
        print("=" * 40)
        
        vm_list = self.hypervisor.list_vms()
        
        for vm in vm_list:
            state_emoji = {"running": "🟢", "paused": "🟡", "stopped": "🔴", "created": "🔵"}.get(vm['state'], "⚪")
            print(f"{state_emoji} {vm['vm_id']} - {vm['state']}")
            print(f"   💾 Memory: {vm['memory_kb']} KB")
            print(f"   🧬 Ribosomes: {vm['ribosome_allocation']}")
            print(f"   ⚡ ATP: {vm['atp_percentage']}%")
            if vm['state'] == 'running':
                print(f"   ⏱️  Uptime: {vm['uptime_seconds']:.1f}s")
        
        # VM action menu
        vm_choices = [Choice(f"{vm['vm_id']} ({vm['state']})", vm['vm_id']) for vm in vm_list]
        
        selected_vm = questionary.select(
            "Select a VM to manage:",
            choices=vm_choices + [Choice("🔙 Back to main menu", "back")]
        ).ask()
        
        if selected_vm == "back":
            return
        
        # Action selection
        vm_status = self.hypervisor.get_vm_status(selected_vm)
        current_state = vm_status['state']
        
        available_actions = []
        if current_state == 'created':
            available_actions.append(Choice("🚀 Start VM", "start"))
        elif current_state == 'running':
            available_actions.extend([
                Choice("⏸️  Pause VM", "pause"),
                Choice("🔄 Restart VM", "restart")
            ])
        elif current_state == 'paused':
            available_actions.append(Choice("▶️  Resume VM", "resume"))
        
        available_actions.extend([
            Choice("📊 Show Detailed Status", "status"),
            Choice("💥 Destroy VM", "destroy"),
            Choice("🔙 Back", "back")
        ])
        
        action = questionary.select(
            f"Action for VM '{selected_vm}':",
            choices=available_actions
        ).ask()
        
        try:
            if action == "start":
                self.hypervisor.start_vm(selected_vm)
                print(f"🚀 VM '{selected_vm}' started!")
            elif action == "pause":
                self.hypervisor.pause_vm(selected_vm)
                print(f"⏸️  VM '{selected_vm}' paused!")
            elif action == "resume":
                self.hypervisor.resume_vm(selected_vm)
                print(f"▶️  VM '{selected_vm}' resumed!")
            elif action == "restart":
                self.hypervisor.pause_vm(selected_vm)
                self.hypervisor.start_vm(selected_vm)
                print(f"🔄 VM '{selected_vm}' restarted!")
            elif action == "status":
                self.show_vm_details(selected_vm)
            elif action == "destroy":
                confirm = questionary.confirm(f"⚠️  Really destroy VM '{selected_vm}'? This cannot be undone.").ask()
                if confirm:
                    self.hypervisor.destroy_vm(selected_vm)
                    if selected_vm in self.active_vms:
                        del self.active_vms[selected_vm]
                    print(f"💥 VM '{selected_vm}' destroyed!")
            elif action == "back":
                return
            
            if action != "status":
                questionary.press_any_key_to_continue().ask()
                
        except Exception as e:
            print(f"❌ Action failed: {e}")
    
    def show_vm_details(self, vm_id: str):
        """Show detailed VM information."""
        vm_status = self.hypervisor.get_vm_status(vm_id)
        
        print(f"\n📊 VM Details: {vm_id}")
        print("=" * 30)
        print(f"State: {vm_status['state']}")
        print(f"Memory: {vm_status['memory_kb']} KB")
        print(f"Ribosomes: {vm_status['ribosome_allocation']}")
        print(f"ATP: {vm_status['atp_percentage']}%")
        print(f"Priority: {vm_status['priority']}")
        print(f"Health: {vm_status['health_status']}")
        
        if vm_status['state'] == 'running':
            print(f"Uptime: {vm_status['uptime_seconds']:.1f} seconds")
            print(f"CPU time used: {vm_status['cpu_time_used']:.2f}")
        
        if vm_id in self.active_vms:
            genome_name = self.active_vms[vm_id]['genome']
            if genome_name in self.loaded_genomes:
                genome_stats = self.loaded_genomes[genome_name]['stats']
                print(f"\nGenome: {genome_stats['organism']}")
                print(f"Total genes: {genome_stats['total_genes']}")
                print(f"Essential genes: {genome_stats['essential_genes']}")
        
        questionary.press_any_key_to_continue().ask()
    
    def show_status(self):
        """Show overall system status."""
        print("\n📈 BioXen System Status")
        print("=" * 30)
        
        print(f"Available genomes: {len(self.available_genomes)}")
        print(f"Loaded genomes: {len(self.loaded_genomes)}")
        
        if self.hypervisor:
            resources = self.hypervisor.get_system_resources()
            print(f"\nHypervisor Status: ✅ Active")
            print(f"Total VMs: {len(self.hypervisor.vms)}")
            print(f"Available ribosomes: {resources['available_ribosomes']}")
            print(f"Max VMs: {resources['max_vms']}")
            
            running_vms = [vm for vm in self.hypervisor.vms.values() if vm.state.value == 'running']
            print(f"Running VMs: {len(running_vms)}")
        else:
            print(f"\nHypervisor Status: ❌ Not initialized")
        
        questionary.press_any_key_to_continue().ask()
    
    def download_genomes(self):
        """Download new genomes using the download system."""
        print("\n💾 Download New Genomes")
        print("This feature requires ncbi-genome-download to be installed.")
        print("Run: pip install -r requirements.txt")
        print("\nThen use: python3 download_genomes.py list")
        questionary.press_any_key_to_continue().ask()

def main():
    """Main entry point for interactive BioXen."""
    try:
        interactive = InteractiveBioXen()
        interactive.start()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
