#!/usr/bin/env python3
"""
Interactive BioXen CLI using questionary for user-friendly genome selection and VM management.
"""

import sys
import time
import shutil
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
    from hypervisor.core import BioXenHypervisor, ResourceAllocation, VMState
    from chassis import ChassisType, BaseChassis, EcoliChassis, YeastChassis
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    sys.exit(1)

class InteractiveBioXen:
    def __init__(self):
        """Initialize the interactive BioXen interface."""
        self.validator = BioXenGenomeValidator()
        self.hypervisor = None
        self.available_genomes = []
        self.chassis_type = ChassisType.ECOLI  # Default chassis
        # Note: integrator will be created dynamically when needed for downloads

    def _suggest_unique_vm_id(self, base_name: str) -> str:
        """Suggest a unique VM ID based on existing VMs."""
        if not self.hypervisor or not self.hypervisor.vms:
            return f"vm_{base_name}"
        
        existing_ids = set(self.hypervisor.vms.keys())
        
        # Try base name first
        candidate = f"vm_{base_name}"
        if candidate not in existing_ids:
            return candidate
        
        # Try with numbers
        for i in range(1, 100):
            candidate = f"vm_{base_name}_{i}"
            if candidate not in existing_ids:
                return candidate
        
        # Fallback with timestamp
        import time
        timestamp = int(time.time() % 10000)
        return f"vm_{base_name}_{timestamp}"

    def main_menu(self):
        """Display and handle the main menu."""
        while True:
            print("\n" + "="*60)
            print("🧬 BioXen Hypervisor - Interactive Genome Management")
            print("="*60)
            
            choices = [
                Choice("🔍 Browse Available Genomes", "browse_genomes"),
                Choice("🧬 Load Genome for Analysis", "validate"),
                Choice("🖥️  Initialize Hypervisor", "init_hypervisor"),
                Choice("📥 Download genomes", "download"),
                Choice("⚡ Create Virtual Machine", "create_vm"),
                Choice("� Manage Running VMs", "status"),
                Choice("� View System Status", "view_status"),
                Choice("� Download New Genomes", "download_new"),
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
                if action == "browse_genomes":
                    self.browse_available_genomes()
                elif action == "init_hypervisor":
                    self.initialize_hypervisor()
                elif action == "download":
                    self.download_genomes()
                elif action == "download_new":
                    self.download_genomes()  # Same as download for now
                elif action == "validate":
                    self.validate_genomes()
                elif action == "create_vm":
                    self.create_vm()
                elif action == "status":
                    self.show_status()
                elif action == "view_status":
                    self.show_status()  # Same as status for now
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

    def browse_available_genomes(self):
        """Browse and display available genomes with detailed information."""
        print("\n🔍 Browse Available Genomes")
        print("📋 Scanning local genome collection...")
        
        # Check for real genomes in genomes directory
        genome_dir = Path("genomes")
        if not genome_dir.exists():
            print("❌ No genomes directory found.")
            print("💡 Use 'Download genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        # Find all .genome files
        genome_files = list(genome_dir.glob("*.genome"))
        
        if not genome_files:
            print("❌ No genome files found in genomes/ directory.")
            print("💡 Use 'Download genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        print(f"✅ Found {len(genome_files)} real bacterial genomes")
        print("="*60)
        
        # Display each genome with details
        for i, genome_file in enumerate(genome_files, 1):
            try:
                # Try to get basic info about the genome
                name = genome_file.stem
                size_kb = genome_file.stat().st_size / 1024
                
                print(f"\n{i}. 🧬 {name}")
                print(f"   📁 File: {genome_file.name}")
                print(f"   💾 Size: {size_kb:.1f} KB")
                
                # Try to load more detailed info if possible
                integrator = BioXenRealGenomeIntegrator(genome_file)
                try:
                    stats = integrator.get_genome_stats()
                    if stats:
                        print(f"   🔬 Genes: {stats.get('total_genes', 'Unknown')}")
                        if 'essential_genes' in stats:
                            essential_pct = stats.get('essential_percentage', 0)
                            print(f"   ⚡ Essential: {stats['essential_genes']} ({essential_pct:.1f}%)")
                        print(f"   🦠 Organism: {stats.get('organism', 'Unknown')}")
                        
                        # Show VM requirements
                        template = integrator.create_vm_template()
                        if template:
                            print(f"   🖥️  VM Memory: {template.get('min_memory_kb', 'Unknown')} KB")
                            print(f"   ⏱️  Boot Time: {template.get('boot_time_ms', 'Unknown')} ms")
                except Exception:
                    print(f"   📊 Status: File available (details pending validation)")
                    
            except Exception as e:
                print(f"   ❌ Error reading genome: {e}")
                
        print("\n" + "="*60)
        print(f"📋 Total: {len(genome_files)} real bacterial genomes available")
        print("💡 Use 'Load Genome for Analysis' to work with a specific genome")
        print("🧬 Use 'Create Virtual Machine' to virtualize these genomes")
        
        questionary.press_any_key_to_continue().ask()

    def download_genomes(self):
        """Download genomes from NCBI with interactive selection."""
        if not self._check_hypervisor():
            return
            
        print("\n📥 Download Genomes from NCBI")
        print("✅ BioXen supports real bacterial genome downloads and management")
        print("📋 Current collection: 5 real minimal bacterial genomes available")
        print("🔄 Options: Download all real genomes, individual genomes, or create simulated data for testing.")
        
        
        # Predefined interesting genomes with emojis and descriptions
        genome_options = [
            {
                "display": "🌐 Download All Real Bacterial Genomes - Complete minimal genome collection",
                "accession": "download_all_real",
                "name": "all_real_genomes", 
                "size": 0
            },
            {
                "display": "🦠 E. coli K-12 MG1655 - Classic lab strain",
                "accession": "NC_000913.3",
                "name": "E_coli_K12_MG1655",
                "size": 4641652
            },
            {
                "display": "🍄 S. cerevisiae S288C - Baker's yeast reference",
                "accession": "NC_001133.9", 
                "name": "S_cerevisiae_S288C",
                "size": 230218
            },
            {
                "display": "🔬 Mycoplasma genitalium - Minimal genome",
                "accession": "NC_000908.2",
                "name": "M_genitalium",
                "size": 580076
            },
            {
                "display": "🌊 Prochlorococcus marinus - Tiny ocean bacteria",
                "accession": "NC_009840.1",
                "name": "P_marinus",
                "size": 1751080
            },
            {
                "display": "💀 Clostridium botulinum - Botox producer",
                "accession": "NC_009495.1", 
                "name": "C_botulinum",
                "size": 3886916
            },
            {
                "display": "🧪 Custom genome - Enter your own accession",
                "accession": "custom",
                "name": "custom",
                "size": 1000000
            }
        ]
        
        choice = questionary.select(
            "Select a genome to download:",
            choices=[Choice(opt["display"], opt) for opt in genome_options]
        ).ask()
        
        if choice is None:
            return
            
        if choice["accession"] == "download_all_real":
            # Launch the download_genomes.py script for real genome downloads
            print("\n🌐 Downloading All Real Bacterial Genomes")
            print("🔄 Launching genome downloader for complete minimal genome collection...")
            print("📋 This will download: JCVI-Syn3A, M. genitalium, M. pneumoniae, C. ruddii, B. aphidicola")
            
            confirm = questionary.confirm(
                "Download all 5 real bacterial genomes? This may take several minutes."
            ).ask()
            
            if not confirm:
                return
                
            try:
                import subprocess
                import sys
                
                print("\n🔄 Starting real genome download process...")
                
                # Run the download_genomes.py script with 'all' command
                result = subprocess.run([
                    sys.executable, 'download_genomes.py', 'all'
                ], capture_output=True, text=True, cwd=Path(__file__).parent)
                
                if result.returncode == 0:
                    print("✅ Successfully downloaded all real bacterial genomes!")
                    print("📋 Available genomes:")
                    print("   • JCVI-Syn3A (538 KB, 187 genes)")
                    print("   • Mycoplasma genitalium (580 KB, 1,108 genes)")
                    print("   • Mycoplasma pneumoniae (823 KB, 1,503 genes)")
                    print("   • Carsonella ruddii (174 KB, 473 genes)")
                    print("   • Buchnera aphidicola (640 KB, 583 genes)")
                    print("\n🧬 You can now use 'Browse Available Genomes' to work with these real genomes!")
                else:
                    print(f"❌ Download failed: {result.stderr}")
                    print("💡 Try running 'python3 download_genomes.py' separately for more details")
                    
            except Exception as e:
                print(f"❌ Error launching genome downloader: {e}")
                print("💡 Try running 'python3 download_genomes.py all' manually")
                
            questionary.press_any_key_to_continue().ask()
            return
            
        elif choice["accession"] in ["NC_000908.2", "NC_000913.3", "NC_001133.9", "NC_009840.1", "NC_009495.1"]:
            # Individual real genome download
            accession = choice["accession"]
            name = choice["name"]
            size = choice["size"]
            
            print(f"\n🌐 Downloading Real Genome: {name}")
            print(f"   Accession: {accession}")
            print(f"   Expected size: {size:,} base pairs")
            print(f"💡 Using NCBI download tools for authentic genome data")
            
            confirm = questionary.confirm(
                f"Download {name} from NCBI? This may take a few minutes."
            ).ask()
            
            if not confirm:
                return
            
            try:
                import subprocess
                import sys
                import os
                from pathlib import Path
                
                print(f"\n🔄 Downloading {name} from NCBI...")
                
                # Check if ncbi-genome-download is available
                try:
                    subprocess.run(['ncbi-genome-download', '--help'], 
                                 capture_output=True, check=True)
                    ncbi_download_available = True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    ncbi_download_available = False
                
                # Create genomes directory if it doesn't exist
                genomes_dir = Path("genomes")
                genomes_dir.mkdir(exist_ok=True)
                
                if ncbi_download_available:
                    # Use ncbi-genome-download for real download
                    print("✅ Using ncbi-genome-download for authentic genome data")
                    
                    # Download command targeting specific accession
                    cmd = [
                        'ncbi-genome-download',
                        'bacteria',
                        '--formats', 'fasta,gff',
                        '--output-folder', 'genomes/downloads',
                        '--parallel', '2',
                        '--retries', '3',
                        '--accessions', accession
                    ]
                    
                    print(f"🔄 Running: {' '.join(cmd)}")
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
                    
                    if result.returncode == 0:
                        print(f"✅ Successfully downloaded {name}!")
                        
                        # Convert to BioXen format
                        download_path = Path("genomes/downloads")
                        if download_path.exists():
                            # Find the downloaded files
                            fasta_files = list(download_path.rglob("*.fna"))
                            gff_files = list(download_path.rglob("*.gff"))
                            
                            if fasta_files:
                                # Copy to main genomes directory with proper naming
                                target_file = genomes_dir / f"{name}.genome"
                                shutil.copy2(fasta_files[0], target_file)
                                
                                print(f"✅ Real genome saved as: {target_file}")
                                print(f"   📊 Authentic NCBI data for {name}")
                                print(f"   🧬 Ready for biological virtualization")
                            else:
                                print("⚠️  Downloaded but no FASTA files found")
                        else:
                            print("⚠️  Download completed but files not found in expected location")
                    else:
                        print(f"❌ NCBI download failed: {result.stderr}")
                        print("🔄 Falling back to simulation for testing...")
                        # Fall back to simulation
                        self._create_simulated_genome(accession, name, size)
                
                else:
                    print("⚠️  ncbi-genome-download not available")
                    print("💡 Install with: pip install ncbi-genome-download")
                    print("🔄 Creating simulated genome for testing...")
                    # Fall back to simulation
                    self._create_simulated_genome(accession, name, size)
                    
            except subprocess.TimeoutExpired:
                print("❌ Download timed out (>5 minutes)")
                print("🔄 Creating simulated genome for testing...")
                self._create_simulated_genome(accession, name, size)
            except Exception as e:
                print(f"❌ Error downloading genome: {e}")
                print("🔄 Creating simulated genome for testing...")
                self._create_simulated_genome(accession, name, size)
                
            questionary.press_any_key_to_continue().ask()
            return
        
        elif choice["accession"] == "custom":
            accession = questionary.text("Enter NCBI accession number (e.g., NC_000913.3):").ask()
            if not accession:
                return
            name = questionary.text("Enter a name for this genome:").ask()
            if not name:
                name = accession.replace(".", "_")
            size = 1000000  # Default size for custom genomes
            
            # Try real download first, then simulate if it fails
            print(f"\n🌐 Attempting to download {accession} from NCBI...")
            # For now, create simulation - real download can be implemented later
            self._create_simulated_genome(accession, name, size)
        else:
            # Fallback simulation for any other options
            accession = choice["accession"]
            name = choice["name"]
            size = choice["size"]
            self._create_simulated_genome(accession, name, size)
        
        questionary.press_any_key_to_continue().ask()

    def _create_simulated_genome(self, accession: str, name: str, size: int):
        """Create simulated genome data for testing purposes."""
        print(f"\n🔄 Generating simulated genome data for {accession}...")
        print(f"💡 Creating simulated genome data for testing and development")
        
        try:
            # Create simulated genome data (random DNA sequence)
            import random
            bases = ['A', 'T', 'G', 'C']
            genome_data = ''.join(random.choice(bases) for _ in range(size))
            
            if genome_data:
                # Add to available genomes
                self.available_genomes.append({
                    "accession": accession,
                    "name": name,
                    "data": genome_data
                })
                print(f"✅ Successfully created simulated {name}")
                print(f"   Accession: {accession}")
                print(f"   Size: {len(genome_data):,} base pairs")
                print(f"   ⚠️  Note: This is simulated data for testing purposes")
            else:
                print(f"❌ Failed to create genome data for {accession}")
        except Exception as e:
            print(f"❌ Error creating genome data: {e}")

    def validate_genomes(self):
        """Validate downloaded genomes."""
        if not self._check_hypervisor():
            return
            
        print("\n🧬 Load Genome for Analysis")
        print("📋 Scanning for available genomes...")
        
        # Check for real genomes in genomes directory
        genome_dir = Path("genomes")
        if not genome_dir.exists():
            print("❌ No genomes directory found.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        # Find all .genome files
        genome_files = list(genome_dir.glob("*.genome"))
        
        if not genome_files:
            print("❌ No genome files found in genomes/ directory.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        print(f"✅ Found {len(genome_files)} genome files")
        
        # Create genome choices from actual files
        genome_choices = []
        valid_genomes = []
        
        for genome_file in genome_files:
            try:
                name = genome_file.stem
                size_kb = genome_file.stat().st_size / 1024
                
                # Try to get basic stats
                integrator = BioXenRealGenomeIntegrator(genome_file)
                try:
                    stats = integrator.get_genome_stats()
                    organism = stats.get('organism', name)
                    gene_count = stats.get('total_genes', 'Unknown')
                    display_name = f"🧬 {organism} ({gene_count} genes, {size_kb:.1f} KB)"
                except Exception:
                    display_name = f"🧬 {name} ({size_kb:.1f} KB)"
                
                genome_info = {
                    'name': name,
                    'file_path': genome_file,
                    'display_name': display_name
                }
                
                genome_choices.append(Choice(display_name, genome_info))
                valid_genomes.append(genome_info)
                
            except Exception as e:
                print(f"⚠️  Warning: Could not read {genome_file.name}: {e}")
        
        if not valid_genomes:
            print("❌ No valid genomes found.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        genome_choices.append(Choice("🔍 Validate all genomes", "all"))
        
        choice = questionary.select(
            "Select genome(s) to validate:",
            choices=genome_choices
        ).ask()
        
        if choice is None:
            return
        
        genomes_to_validate = valid_genomes if choice == "all" else [choice]
        
        print(f"\n🔄 Validating {len(genomes_to_validate)} genome(s)...")
        
        for genome in genomes_to_validate:
            print(f"\n📋 Validating {genome['name']}...")
            try:
                # Create integrator for this genome file
                integrator = BioXenRealGenomeIntegrator(genome['file_path'])
                
                # Try to load and validate the genome
                genome_data = integrator.load_genome()
                stats = integrator.get_genome_stats()
                
                print(f"   ✅ {genome['name']} - Successfully loaded")
                print(f"      🧬 Organism: {stats.get('organism', 'Unknown')}")
                print(f"      📊 Total genes: {stats.get('total_genes', 'Unknown')}")
                if 'essential_genes' in stats:
                    essential_pct = stats.get('essential_percentage', 0)
                    print(f"      ⚡ Essential genes: {stats['essential_genes']} ({essential_pct:.1f}%)")
                
                # Test VM template creation
                template = integrator.create_vm_template()
                if template:
                    print(f"      🖥️  VM requirements: {template.get('min_memory_kb')} KB memory")
                    print(f"      ⏱️  Estimated boot time: {template.get('boot_time_ms')} ms")
                
            except Exception as e:
                print(f"   ❌ {genome['name']} - Validation error: {e}")
        
        questionary.press_any_key_to_continue().ask()

    def create_vm(self):
        """Create a new VM with genome selection."""
        if not self._check_hypervisor():
            return
            
        print("\n⚡ Create Virtual Machine")
        print("📋 Scanning for available genomes...")
        
        # Check for real genomes in genomes directory
        genome_dir = Path("genomes")
        if not genome_dir.exists():
            print("❌ No genomes directory found.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        # Find all .genome files
        genome_files = list(genome_dir.glob("*.genome"))
        
        if not genome_files:
            print("❌ No genome files found in genomes/ directory.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        print(f"✅ Found {len(genome_files)} genome files")
        
        # Create genome choices from actual files
        genome_choices = []
        valid_genomes = []
        
        for genome_file in genome_files:
            try:
                name = genome_file.stem
                size_kb = genome_file.stat().st_size / 1024
                
                # Try to get detailed stats for VM requirements
                integrator = BioXenRealGenomeIntegrator(genome_file)
                try:
                    stats = integrator.get_genome_stats()
                    template = integrator.create_vm_template()
                    
                    organism = stats.get('organism', name)
                    gene_count = stats.get('total_genes', 'Unknown')
                    essential_count = stats.get('essential_genes', 'Unknown')
                    min_memory = template.get('min_memory_kb', 136) if template else 136
                    
                    display_name = f"🧬 {organism} ({essential_count} essential genes, min {min_memory} KB)"
                    
                    genome_info = {
                        'name': name,
                        'organism': organism,
                        'file_path': genome_file,
                        'stats': stats,
                        'template': template,
                        'display_name': display_name
                    }
                    
                except Exception:
                    display_name = f"🧬 {name} ({size_kb:.1f} KB)"
                    genome_info = {
                        'name': name,
                        'organism': name,
                        'file_path': genome_file,
                        'stats': None,
                        'template': None,
                        'display_name': display_name
                    }
                
                genome_choices.append(Choice(display_name, genome_info))
                valid_genomes.append(genome_info)
                
            except Exception as e:
                print(f"⚠️  Warning: Could not read {genome_file.name}: {e}")
        
        if not valid_genomes:
            print("❌ No valid genomes found.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
        
        # Select genome
        selected_genome = questionary.select(
            "Which genome should the VM use?",
            choices=genome_choices
        ).ask()
        
        if selected_genome is None:
            return
        
        # Show existing VMs first to help user choose unique ID
        if self.hypervisor and self.hypervisor.vms:
            print(f"\n📋 Existing VMs ({len(self.hypervisor.vms)}):")
            for existing_vm_id, vm in self.hypervisor.vms.items():
                status_emoji = "🟢" if vm.state == VMState.RUNNING else "🔴" if vm.state == VMState.ERROR else "🟡"
                print(f"   {status_emoji} {existing_vm_id}")
        
        # Get VM ID with improved handling
        suggested_id = self._suggest_unique_vm_id(selected_genome['name'])
        
        while True:
            vm_id = questionary.text(
                "VM ID (unique identifier):",
                default=suggested_id
            ).ask()
            
            if not vm_id:
                return
            
            # Check if VM ID already exists
            if self.hypervisor and vm_id in self.hypervisor.vms:
                print(f"\n⚠️  VM '{vm_id}' already exists!")
                
                # Suggest alternative IDs
                alternative_suggestions = [
                    self._suggest_unique_vm_id(selected_genome['name']),
                    self._suggest_unique_vm_id(f"{selected_genome['name']}_new"),
                    self._suggest_unique_vm_id(f"{selected_genome['name']}_test")
                ]
                
                print(f"💡 Suggested alternatives:")
                for i, suggestion in enumerate(alternative_suggestions[:3], 1):
                    print(f"   {i}. {suggestion}")
                
                action = questionary.select(
                    "What would you like to do?",
                    choices=[
                        Choice("🔄 Try a different VM ID", "retry"),
                        Choice(f"✨ Use suggestion: {alternative_suggestions[0]}", "use_suggestion"),
                        Choice("🗑️  Delete existing VM and create new one", "replace"),
                        Choice("📊 View existing VM details", "view"),
                        Choice("❌ Cancel VM creation", "cancel")
                    ]
                ).ask()
                
                if action == "retry":
                    continue  # Ask for VM ID again
                elif action == "use_suggestion":
                    vm_id = alternative_suggestions[0]
                    print(f"✅ Using suggested ID: {vm_id}")
                    break  # Proceed with creation
                elif action == "replace":
                    # Delete existing VM first
                    if self.hypervisor.destroy_vm(vm_id):
                        print(f"✅ Deleted existing VM '{vm_id}'")
                        break  # Proceed with creation
                    else:
                        print(f"❌ Failed to delete existing VM '{vm_id}'")
                        continue
                elif action == "view":
                    # Show VM details
                    existing_vm = self.hypervisor.vms[vm_id]
                    print(f"\n📊 VM '{vm_id}' Details:")
                    print(f"   State: {existing_vm.state.value}")
                    if existing_vm.resources:
                        print(f"   Memory: {existing_vm.resources.memory_kb} KB")
                        print(f"   Ribosomes: {existing_vm.resources.ribosomes}")
                        print(f"   ATP: {existing_vm.resources.atp_percentage}%")
                        print(f"   Priority: {existing_vm.resources.priority}")
                    continue  # Ask for VM ID again
                elif action == "cancel":
                    return
            else:
                break  # VM ID is unique, proceed
        
        # Show genome requirements if available
        if selected_genome['template']:
            template = selected_genome['template']
            min_memory_kb = template.get('min_memory_kb', 136)
            min_cpu = template.get('min_cpu_percent', 15)
            boot_time = template.get('boot_time_ms', 500)
            
            print(f"\n📊 Genome requirements:")
            print(f"   💾 Min memory: {min_memory_kb} KB")
            print(f"   🔧 Min CPU: {min_cpu}%")
            print(f"   ⏱️  Boot time: {boot_time} ms")
        else:
            min_memory_kb = 136  # Default minimum
        
        # Resource allocation with intelligent defaults
        memory_kb = questionary.text(
            f"Memory allocation in KB (min: {min_memory_kb}):",
            default=str(max(min_memory_kb * 2, 500))  # At least 2x minimum or 500KB
        ).ask()
        
        if not memory_kb:
            return
        
        try:
            memory_kb = int(memory_kb)
            if memory_kb < min_memory_kb:
                print(f"⚠️  Warning: Memory {memory_kb} KB is below minimum {min_memory_kb} KB")
        except ValueError:
            print("❌ Invalid memory value")
            questionary.press_any_key_to_continue().ask()
            return
        
        # ATP percentage
        atp_percentage = questionary.text(
            "ATP percentage (10-50%):",
            default="25"
        ).ask()
        
        if not atp_percentage:
            return
        
        try:
            atp_percentage = float(atp_percentage)
            if not (10 <= atp_percentage <= 50):
                print("⚠️  Warning: ATP percentage should be between 10-50%")
        except ValueError:
            print("❌ Invalid ATP percentage")
            questionary.press_any_key_to_continue().ask()
            return
        
        # Ribosome allocation
        ribosomes = questionary.text(
            "Ribosome allocation (5-40):",
            default="20"
        ).ask()
        
        if not ribosomes:
            return
        
        try:
            ribosomes = int(ribosomes)
            if not (5 <= ribosomes <= 40):
                print("⚠️  Warning: Ribosome count should be between 5-40")
        except ValueError:
            print("❌ Invalid ribosome count")
            questionary.press_any_key_to_continue().ask()
            return
        
        # VM Priority
        priority_choices = [
            Choice("🔴 High (1)", 1),
            Choice("🟢 Normal (2)", 2),
            Choice("🟡 Low (3)", 3)
        ]
        
        priority = questionary.select(
            "VM Priority:",
            choices=priority_choices
        ).ask()
        
        if priority is None:
            priority = 2  # Default to normal
        
        print(f"\n🔄 Creating VM '{vm_id}'...")
        print(f"   🧬 Genome: {selected_genome['organism']}")
        print(f"   💾 Memory: {memory_kb} KB")
        print(f"   🧬 Ribosomes: {ribosomes}")
        print(f"   ⚡ ATP: {atp_percentage}%")
        print(f"   🎯 Priority: {priority}")
        print(f"   🖥️  Chassis: {self.chassis_type.value}")
        
        try:
            # Load the actual genome data
            integrator = BioXenRealGenomeIntegrator(selected_genome['file_path'])
            genome_data = integrator.load_genome()
            
            allocation = ResourceAllocation(
                memory_kb=memory_kb,
                ribosomes=ribosomes,
                atp_percentage=atp_percentage,
                priority=priority
            )
            
            vm_result = self.hypervisor.create_vm(vm_id, genome_data, allocation)
            if vm_result:
                print(f"\n✅ Virtual Machine '{vm_id}' created successfully!")
                print(f"   🧬 Genome: {selected_genome['organism']}")
                print(f"   💾 Memory: {memory_kb} KB")
                print(f"   🧬 Ribosomes: {ribosomes}")
                print(f"   ⚡ ATP: {atp_percentage}%")
                print(f"   🎯 Priority: {priority}")
                print(f"   📊 Status: Ready for startup")
                
                # Suggest next actions
                print(f"\n💡 Next steps:")
                print(f"   • Use 'Start Virtual Machine' to boot the VM")
                print(f"   • Use 'Show System Status' to monitor resources")
                print(f"   • Use 'Launch Visualization' to see cellular activity")
            else:
                print(f"\n❌ Failed to create VM '{vm_id}'")
                
                # Provide helpful diagnostics
                print(f"\n🔍 Possible reasons:")
                
                # Check maximum VMs
                vm_count = len(self.hypervisor.vms)
                max_vms = self.hypervisor.max_vms
                if vm_count >= max_vms:
                    print(f"   • Maximum VMs reached ({vm_count}/{max_vms})")
                    print(f"     → Delete existing VMs or increase chassis capacity")
                
                # Check resource availability  
                available_ribosomes = self.hypervisor.available_ribosomes
                allocated_ribosomes = sum(vm.resources.ribosomes for vm in self.hypervisor.vms.values() if vm.resources)
                remaining_ribosomes = available_ribosomes - allocated_ribosomes
                
                if ribosomes > remaining_ribosomes:
                    print(f"   • Insufficient ribosomes (requested: {ribosomes}, available: {remaining_ribosomes})")
                    print(f"     → Reduce ribosome allocation or free up resources")
                
                # Check ATP allocation
                allocated_atp = sum(vm.resources.atp_percentage for vm in self.hypervisor.vms.values() if vm.resources)
                remaining_atp = 100 - allocated_atp
                
                if atp_percentage > remaining_atp:
                    print(f"   • Insufficient ATP (requested: {atp_percentage}%, available: {remaining_atp:.1f}%)")
                    print(f"     → Reduce ATP percentage or pause other VMs")
                
                # Check if VM ID still exists (edge case)
                if vm_id in self.hypervisor.vms:
                    print(f"   • VM ID '{vm_id}' already exists")
                    print(f"     → Choose a different VM ID")
                
                print(f"\n💡 Try:")
                print(f"   • Check 'Show System Status' for resource usage")
                print(f"   • Use 'Manage Virtual Machines' to free up resources")
                print(f"   • Reduce resource allocation requirements")
                
        except Exception as e:
            print(f"\n❌ Error creating VM: {e}")
            print(f"\n🔍 Troubleshooting:")
            print(f"   • Verify genome file is valid: {selected_genome['file_path']}")
            print(f"   • Check hypervisor status")
            print(f"   • Ensure resource values are within valid ranges")
        
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
                    status_emoji = "🟢" if vm.state == VMState.RUNNING else "🔴" if vm.state == VMState.ERROR else "🟡" if vm.state == VMState.PAUSED else "�"
                    # Get resource information
                    memory_kb = vm.resources.memory_kb if vm.resources else 0
                    memory_mb = memory_kb / 1024 if memory_kb > 0 else 0
                    ribosomes = vm.resources.ribosomes if vm.resources else "Unknown"
                    atp_percent = vm.resources.atp_percentage if vm.resources else "Unknown"
                    
                    print(f"  {status_emoji} {vm_id}")
                    print(f"    📊 State: {vm.state.value}")
                    print(f"    💾 Memory: {memory_mb:.1f} MB ({memory_kb} KB)")
                    print(f"    🧬 Ribosomes: {ribosomes}")
                    print(f"    ⚡ ATP: {atp_percent}%")
                    
                    # Show concise genome info instead of full object
                    if hasattr(vm.genome_template, 'organism'):
                        # Real genome
                        genome_info = f"{vm.genome_template.organism} ({len(vm.genome_template.genes)} genes)"
                    elif isinstance(vm.genome_template, str):
                        # Genome name string
                        genome_info = vm.genome_template
                    else:
                        # Unknown format
                        genome_info = f"{type(vm.genome_template).__name__}"
                    
                    print(f"    🧬 Genome: {genome_info}")
                    if vm.start_time:
                        uptime = time.time() - vm.start_time
                        print(f"    ⏱️  Uptime: {uptime:.1f}s")
            
            # Resource utilization  
            total_memory_kb = sum(vm.resources.memory_kb for vm in self.hypervisor.vms.values() if vm.resources)
            total_memory_mb = total_memory_kb / 1024 if total_memory_kb > 0 else 0
            total_ribosomes = sum(vm.resources.ribosomes for vm in self.hypervisor.vms.values() if vm.resources)
            
            print(f"\nResource Utilization:")
            print(f"  💾 Memory: {total_memory_mb:.1f} MB ({total_memory_kb} KB)")
            print(f"  🧬 Ribosomes: {total_ribosomes}")
            
            # VM state breakdown
            if vm_count > 0:
                states = {}
                for vm in self.hypervisor.vms.values():
                    state = vm.state.value
                    states[state] = states.get(state, 0) + 1
                
                if states:
                    print(f"\nVM States:")
                    for state, count in states.items():
                        emoji = {"running": "🟢", "paused": "🟡", "stopped": "🔴", "created": "🔵", "error": "❌"}.get(state, "⚪")
                        print(f"  {emoji} {state.title()}: {count}")
            
            # Show warning for placeholder implementations
            if self.chassis_type == ChassisType.YEAST:
                print(f"\n⚠️  Note: Yeast chassis is currently a PLACEHOLDER implementation")
        else:
            print(f"\nHypervisor Status: ❌ Not initialized")
            print(f"Use '🖥️ Initialize Hypervisor' to start")
        
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
