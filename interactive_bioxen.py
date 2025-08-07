#!/usr/bin/env python3
"""
Enhanced Interactive BioXen CLI with improved error handling, logging, and additional features.
"""

import sys
import time
import shutil
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bioxen.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

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
    from chassis import ChassisType, BaseChassis, EcoliChassis, YeastChassis, OrthogonalChassis
except ImportError as e:
    logger.error(f"Import error: {e}")
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    sys.exit(1)

@dataclass
class GenomeInfo:
    """Data class for genome information."""
    name: str
    accession: str
    size: int
    file_path: Optional[Path] = None
    data: Optional[str] = None
    validated: bool = False
    organism: Optional[str] = None
    gene_count: Optional[int] = None

class InteractiveBioXen:
    """Enhanced Interactive BioXen CLI with improved functionality."""
    
    def __init__(self):
        self.validator = BioXenGenomeValidator()
        self.available_genomes: List[GenomeInfo] = []
        self.genomes_dir = Path("genomes")
        self.genomes_dir.mkdir(exist_ok=True)
        logger.info("InteractiveBioXen initialized")

    def get_genome_options(self) -> List[Dict[str, Any]]:
        """Get predefined genome options with metadata."""
        return [
            {
                "display": "🌐 Download All Real Bacterial Genomes - Complete minimal genome collection",
                "accession": "download_all_real",
                "name": "all_real_genomes",
                "size": 0,
                "organism": "Multiple",
                "description": "Downloads a curated collection of minimal bacterial genomes"
            },
            {
                "display": "🦠 E. coli K-12 MG1655 - Classic lab strain",
                "accession": "NC_000913.3",
                "name": "E_coli_K12_MG1655",
                "size": 4641652,
                "organism": "Escherichia coli",
                "description": "Most widely used laboratory strain of E. coli"
            },
            {
                "display": "🍄 S. cerevisiae S288C - Baker's yeast reference",
                "accession": "NC_001133.9",
                "name": "S_cerevisiae_S288C",
                "size": 230218,
                "organism": "Saccharomyces cerevisiae",
                "description": "Reference genome for baker's yeast"
            },
            {
                "display": "🔬 Mycoplasma genitalium - Minimal genome",
                "accession": "NC_000908.2",
                "name": "M_genitalium",
                "size": 580076,
                "organism": "Mycoplasma genitalium",
                "description": "One of the smallest known genomes"
            },
            {
                "display": "🌊 Prochlorococcus marinus - Tiny ocean bacteria",
                "accession": "NC_009840.1",
                "name": "P_marinus",
                "size": 1751080,
                "organism": "Prochlorococcus marinus",
                "description": "Abundant marine cyanobacterium"
            },
            {
                "display": "💀 Clostridium botulinum - Botox producer",
                "accession": "NC_009495.1",
                "name": "C_botulinum",
                "size": 3886916,
                "organism": "Clostridium botulinum",
                "description": "Produces botulinum toxin"
            },
            {
                "display": "🧪 Custom genome - Enter your own accession",
                "accession": "custom",
                "name": "custom",
                "size": 1000000,
                "organism": "Custom",
                "description": "Enter a custom NCBI accession number"
            }
        ]

    def download_genomes(self):
        """Enhanced genome download with better error handling and progress tracking."""
        print("\n⬇️ Download New Genomes")
        print("💡 You can select a real genome from NCBI or create a custom simulated one.")

        genome_options = self.get_genome_options()
        choices = [Choice(opt["display"], opt) for opt in genome_options]
        
        choice = questionary.select("Select a genome to download:", choices=choices).ask()

        if choice is None:
            return

        accession = choice["accession"]
        name = choice["name"]
        size = choice["size"]
        organism = choice.get("organism", name)
        
        logger.info(f"Starting download for {accession} ({name})")
        
        if accession == "download_all_real":
            self._download_all_real_genomes()
            return
            
        if accession == "custom":
            custom_accession = questionary.text("Enter NCBI accession number (e.g., NC_000913.3):").ask()
            if not custom_accession:
                return
            accession = custom_accession
            name = f"custom_{custom_accession.replace('.', '_')}"
            
        print(f"\n🌐 Attempting to download {accession} from NCBI...")
        
        try:
            success = self._attempt_genome_download(accession, name, organism, size)
            if not success:
                print("🔄 Creating simulated genome for testing...")
                self._create_simulated_genome(accession, name, size, organism)
        
        except Exception as e:
            logger.error(f"Error during genome download: {e}")
            print(f"❌ Unexpected error during download: {e}")
            print("🔄 Creating simulated genome for testing...")
            self._create_simulated_genome(accession, name, size, organism)

        questionary.press_any_key_to_continue().ask()

    def _download_all_real_genomes(self):
        """Download all predefined real genomes."""
        print("\n🌐 Downloading all real bacterial genomes...")
        print("⚠️ This will download multiple genomes and may take some time.")
        
        confirm = questionary.confirm("Continue with bulk download?").ask()
        if not confirm:
            return
            
        genome_options = [opt for opt in self.get_genome_options() 
                         if opt["accession"] not in ["download_all_real", "custom"]]
        
        successful_downloads = 0
        total_genomes = len(genome_options)
        
        for i, genome_opt in enumerate(genome_options, 1):
            print(f"\n📦 Downloading {i}/{total_genomes}: {genome_opt['name']}")
            try:
                success = self._attempt_genome_download(
                    genome_opt["accession"], 
                    genome_opt["name"], 
                    genome_opt["organism"], 
                    genome_opt["size"]
                )
                if success:
                    successful_downloads += 1
                    print(f"✅ Successfully downloaded {genome_opt['name']}")
                else:
                    print(f"⚠️ Failed to download {genome_opt['name']}, created simulation")
            except Exception as e:
                logger.error(f"Error downloading {genome_opt['name']}: {e}")
                print(f"❌ Error downloading {genome_opt['name']}: {e}")
        
        print(f"\n📊 Download Summary: {successful_downloads}/{total_genomes} successful downloads")

    def _attempt_genome_download(self, accession: str, name: str, organism: str, size: int) -> bool:
        """Attempt to download a genome using available methods."""
        genome_file = self.genomes_dir / f"{name}.genome"
        
        # Check if file already exists
        if genome_file.exists() and genome_file.stat().st_size > 1000:
            file_size_mb = genome_file.stat().st_size / (1024 * 1024)
            print(f"✅ Found existing genome file!")
            print(f"   📊 File size: {file_size_mb:.1f} MB")
            print(f"   🧬 Ready for biological virtualization")
            return True
        
        # Try advanced download helper
        try:
            from genome_download_helper import GenomeDownloadHelper
            download_helper = GenomeDownloadHelper(str(self.genomes_dir))
            success, message = download_helper.download_genome(accession, name)
            
            if genome_file.exists() and genome_file.stat().st_size > 1000:
                file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                print(f"✅ Successfully downloaded {name}!")
                print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                print(f"   🧬 Ready for biological virtualization")
                logger.info(f"Downloaded {name} successfully ({file_size_mb:.1f} MB)")
                return True
            elif success:
                print(f"✅ Download helper reported success: {message}")
                return True
            else:
                print(f"⚠️ Download helper failed: {message}")
                return False
                
        except ImportError:
            logger.warning("Advanced download helper not available")
            print("⚠️ Advanced download helper not available")
            
        # Try basic ncbi-genome-download
        try:
            result = subprocess.run(['ncbi-genome-download', '--help'], 
                                  capture_output=True, check=True, timeout=5)
            # If we get here, the tool is available
            print("💡 Using ncbi-genome-download...")
            
            download_cmd = [
                'ncbi-genome-download', 'bacteria', 
                '--accessions', accession,
                '--output-folder', str(self.genomes_dir),
                '--formats', 'fasta',
                '--parallel', '2'
            ]
            
            result = subprocess.run(download_cmd, capture_output=True, 
                                  text=True, timeout=300)  # 5 minute timeout
            
            if result.returncode == 0 and genome_file.exists():
                return True
            else:
                print(f"⚠️ ncbi-genome-download failed: {result.stderr}")
                return False
                
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            print("⚠️ ncbi-genome-download not available or failed")
            return False

    def _create_simulated_genome(self, accession: str, name: str, size: int, organism: str = None):
        """Create simulated genome data with better structure."""
        print(f"\n🔄 Generating simulated genome data for {accession}...")
        print(f"💡 Creating realistic simulated genome data for testing")
        
        try:
            import random
            random.seed(42)  # For reproducible results
            
            # Create more realistic genome structure
            bases = ['A', 'T', 'G', 'C']
            weights = [0.25, 0.25, 0.25, 0.25]  # Equal distribution for simplicity
            
            # Generate genome sequence
            genome_sequence = ''.join(random.choices(bases, weights=weights, k=size))
            
            # Create a simple FASTA-like format
            genome_data = f">gi|fake|ref|{accession}| {organism or name} complete genome\n"
            
            # Break sequence into lines of 80 characters
            for i in range(0, len(genome_sequence), 80):
                genome_data += genome_sequence[i:i+80] + "\n"
            
            # Save to file
            genome_file = self.genomes_dir / f"{name}.genome"
            with open(genome_file, 'w') as f:
                f.write(genome_data)
            
            # Create GenomeInfo object
            genome_info = GenomeInfo(
                name=name,
                accession=accession,
                size=len(genome_sequence),
                file_path=genome_file,
                organism=organism or name
            )
            
            self.available_genomes.append(genome_info)
            
            print(f"✅ Successfully created simulated {name}")
            print(f"   Accession: {accession}")
            print(f"   Size: {len(genome_sequence):,} base pairs")
            print(f"   File: {genome_file}")
            print(f"   ⚠️ Note: This is simulated data for testing purposes")
            
            logger.info(f"Created simulated genome {name} ({len(genome_sequence)} bp)")
            
        except Exception as e:
            logger.error(f"Error creating simulated genome: {e}")
            print(f"❌ Error creating genome data: {e}")

    def validate_genomes(self):
        """Enhanced genome validation with better reporting."""
        print("\n🧬 Load Genome for Analysis")
        print("📋 Scanning for available genomes...")
        
        if not self.genomes_dir.exists():
            print("❌ No genomes directory found.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        genome_files = list(self.genomes_dir.glob("*.genome"))
        
        if not genome_files:
            print("❌ No genome files found in genomes/ directory.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        print(f"✅ Found {len(genome_files)} genome files")
        
        genome_choices = []
        valid_genomes = []
        
        for genome_file in genome_files:
            try:
                genome_info = self._analyze_genome_file(genome_file)
                if genome_info:
                    display_name = self._format_genome_display_name(genome_info)
                    genome_choices.append(Choice(display_name, genome_info))
                    valid_genomes.append(genome_info)
                    
            except Exception as e:
                logger.warning(f"Could not analyze {genome_file.name}: {e}")
                print(f"⚠️ Warning: Could not read {genome_file.name}: {e}")
        
        if not valid_genomes:
            print("❌ No readable genomes found.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        genome_choices.extend([
            Choice("🔍 Validate all genomes", "all"),
            Choice("📊 Show genome statistics", "stats")
        ])
        
        choice = questionary.select(
            "Select a genome action:",
            choices=genome_choices
        ).ask()
        
        if choice is None:
            return
            
        if choice == "all":
            self._validate_all_genomes(valid_genomes)
        elif choice == "stats":
            self._show_genome_statistics(valid_genomes)
        else:
            self._validate_single_genome(choice)
        
        questionary.press_any_key_to_continue().ask()

    def _analyze_genome_file(self, genome_file: Path) -> Optional[GenomeInfo]:
        """Analyze a genome file and extract metadata."""
        try:
            name = genome_file.stem
            size_kb = genome_file.stat().st_size / 1024
            
            # Try to get detailed stats using integrator
            try:
                integrator = BioXenRealGenomeIntegrator(genome_file)
                stats = integrator.get_genome_stats()
                organism = stats.get('organism', name)
                gene_count = stats.get('total_genes', None)
            except Exception:
                # Fallback to basic file analysis
                organism = name
                gene_count = None
            
            return GenomeInfo(
                name=name,
                accession=name,  # Use name as accession if not available
                size=int(size_kb * 1024),  # Convert back to bytes
                file_path=genome_file,
                organism=organism,
                gene_count=gene_count
            )
            
        except Exception as e:
            logger.error(f"Error analyzing genome file {genome_file}: {e}")
            return None

    def _format_genome_display_name(self, genome_info: GenomeInfo) -> str:
        """Format genome information for display."""
        size_kb = genome_info.size / 1024 if genome_info.size else 0
        
        if genome_info.gene_count:
            return f"🧬 {genome_info.organism} ({genome_info.gene_count} genes, {size_kb:.1f} KB)"
        else:
            return f"🧬 {genome_info.organism} ({size_kb:.1f} KB)"

    def _validate_all_genomes(self, genomes: List[GenomeInfo]):
        """Validate all available genomes."""
        print("\n🔄 Validating all available genomes...")
        
        validation_results = []
        
        for genome_info in genomes:
            print(f"\n🔬 Validating {genome_info.name}...")
            try:
                is_valid, messages = self.validator.validate_genome(genome_info.file_path)
                validation_results.append({
                    'genome': genome_info,
                    'valid': is_valid,
                    'messages': messages
                })
                
                if is_valid:
                    print(f"✅ {genome_info.name} is a valid BioXen genome.")
                    genome_info.validated = True
                else:
                    print(f"❌ {genome_info.name} is NOT a valid BioXen genome:")
                    for msg in messages:
                        print(f"   - {msg}")
                        
            except Exception as e:
                logger.error(f"Error validating {genome_info.name}: {e}")
                print(f"❌ Error validating {genome_info.name}: {e}")
                validation_results.append({
                    'genome': genome_info,
                    'valid': False,
                    'messages': [str(e)]
                })
        
        # Summary
        valid_count = sum(1 for result in validation_results if result['valid'])
        total_count = len(validation_results)
        
        print(f"\n📊 Validation Summary:")
        print(f"   ✅ Valid genomes: {valid_count}/{total_count}")
        print(f"   ❌ Invalid genomes: {total_count - valid_count}/{total_count}")
        
        if valid_count == total_count:
            print("\n🎉 All genomes validated successfully!")
            # Add valid genomes to available list
            for result in validation_results:
                if result['valid'] and result['genome'] not in self.available_genomes:
                    self.available_genomes.append(result['genome'])

    def _validate_single_genome(self, genome_info: GenomeInfo):
        """Validate a single genome."""
        print(f"\n🔬 Validating {genome_info.name}...")
        try:
            is_valid, messages = self.validator.validate_genome(genome_info.file_path)
            if is_valid:
                print(f"✅ {genome_info.name} is a valid BioXen genome.")
                genome_info.validated = True
                
                if genome_info not in self.available_genomes:
                    self.available_genomes.append(genome_info)
                    print(f"💡 {genome_info.name} is now available for VM creation.")
            else:
                print(f"❌ {genome_info.name} is NOT a valid BioXen genome:")
                for msg in messages:
                    print(f"   - {msg}")
        except Exception as e:
            logger.error(f"Error validating {genome_info.name}: {e}")
            print(f"❌ Error validating {genome_info.name}: {e}")

    def _show_genome_statistics(self, genomes: List[GenomeInfo]):
        """Show detailed statistics for all genomes."""
        print("\n📊 Genome Statistics")
        print("=" * 80)
        
        for genome_info in genomes:
            print(f"\n🧬 {genome_info.name}")
            print(f"   Organism: {genome_info.organism}")
            print(f"   File size: {genome_info.size / 1024:.1f} KB")
            if genome_info.gene_count:
                print(f"   Genes: {genome_info.gene_count:,}")
            print(f"   File path: {genome_info.file_path}")
            print(f"   Validated: {'✅ Yes' if genome_info.validated else '❌ No'}")

    def create_lua_vm(self):
        """Enhanced Lua VM creation with better error handling."""
        print("\n🌙 Create Lua VM (pylua-bioxen-vm)")
        print("💡 This option uses the pylua-bioxen-vm library for robust Lua VM orchestration.")
        print("   Make sure 'lua' and 'luasocket' are installed for networking features.")

        try:
            from pylua_bioxen_vm import VMManager
        except ImportError:
            print("❌ pylua-bioxen-vm library not installed.")
            print("   Install with: pip install pylua-bioxen-vm")
            print("   Or from source: https://github.com/aptitudetechnology/pylua-bioxen-vm")
            questionary.press_any_key_to_continue().ask()
            return

        self._lua_vm_menu()

    def _lua_vm_menu(self):
        """Show Lua VM management menu."""
        while True:
            action = questionary.select(
                "Choose Lua VM action:",
                choices=[
                    Choice("🖥️ Start Server VM", "server"),
                    Choice("🔗 Start Client VM", "client"),
                    Choice("🌐 Start P2P VM", "p2p"),
                    Choice("⚡ Execute Lua code string", "code"),
                    Choice("📄 Execute Lua script file", "script"),
                    Choice("🛠️ Manage running VMs", "manage"),
                    Choice("📊 VM Statistics", "stats"),
                    Choice("↩️ Back to Main Menu", "back")
                ]
            ).ask()

            if action is None or action == "back":
                print("↩️ Returning to main menu.")
                break

            try:
                self._handle_lua_vm_action(action)
            except Exception as e:
                logger.error(f"Error in Lua VM action {action}: {e}")
                print(f"❌ Error: {e}")
            
            questionary.press_any_key_to_continue().ask()

    def _handle_lua_vm_action(self, action: str):
        """Handle specific Lua VM actions."""
        from pylua_bioxen_vm import VMManager
        
        with VMManager() as manager:
            if action == "server":
                self._start_server_vm(manager)
            elif action == "client":
                self._start_client_vm(manager)
            elif action == "p2p":
                self._start_p2p_vm(manager)
            elif action == "code":
                self._execute_lua_code(manager)
            elif action == "script":
                self._execute_lua_script(manager)
            elif action == "manage":
                self._manage_vms(manager)
            elif action == "stats":
                self._show_vm_statistics(manager)

    def _start_server_vm(self, manager):
        """Start a Lua server VM."""
        port = questionary.text("Enter port for Lua Server:", 
                               default="8080", 
                               validate=lambda x: x.isdigit() and 1000 <= int(x) <= 65535).ask()
        if not port:
            return
            
        vm_id = questionary.text("Enter VM ID:", default=f"server_{port}").ask() or f"server_{port}"
        
        print(f"🌐 Creating server VM '{vm_id}' on port {port}...")
        manager.create_vm(vm_id, networked=True)
        
        future = manager.start_server_vm(vm_id, port=int(port))
        print(f"🌐 Server VM '{vm_id}' listening on port {port}...")
        print("   Press Ctrl+C to stop the server")
        
        try:
            result = future.result(timeout=None)
            print(result.get('stdout', ''))
            if result.get('stderr'): 
                print(f"STDERR: {result['stderr']}")
        except KeyboardInterrupt:
            print("🛑 Server stopped.")
            future.cancel()

    def _start_client_vm(self, manager):
        """Start a Lua client VM."""
        ip = questionary.text("Enter Server IP:", default="localhost").ask()
        port = questionary.text("Enter Server Port:", default="8080").ask()
        message = questionary.text("Enter message to send:", default="Hello from BioXen Lua Client!").ask()
        
        if not all([ip, port, message]):
            print("❌ All fields are required for client VM")
            return
            
        vm_id = questionary.text("Enter VM ID:", default=f"client_{ip}_{port}").ask() or f"client_{ip}_{port}"
        
        print(f"🔗 Creating client VM '{vm_id}'...")
        manager.create_vm(vm_id, networked=True)
        
        future = manager.start_client_vm(vm_id, ip, int(port), message)
        print(f"🔗 Client VM '{vm_id}' connecting to {ip}:{port}...")
        
        try:
            result = future.result(timeout=30)
            print("📨 Client response:")
            print(result.get('stdout', ''))
            if result.get('stderr'): 
                print(f"STDERR: {result['stderr']}")
        except Exception as e:
            print(f"❌ Client error: {e}")

    def _execute_lua_code(self, manager):
        """Execute Lua code string."""
        lua_code = questionary.text("Enter Lua code to execute:", 
                                   default="print('Hello from BioXen Lua VM!')").ask()
        if not lua_code:
            return
            
        vm_id = questionary.text("Enter VM ID:", default="code_exec").ask() or "code_exec"
        
        print(f"⚡ Executing Lua code in VM '{vm_id}'...")
        manager.create_vm(vm_id, networked=False)
        
        result = manager.execute_code(vm_id, lua_code)
        print("📤 Execution result:")
        print(result.get('stdout', ''))
        if result.get('stderr'): 
            print(f"STDERR: {result['stderr']}")

    def _show_vm_statistics(self, manager):
        """Show VM statistics and information."""
        print("\n📊 VM Statistics")
        print("=" * 60)
        
        vms = manager.list_vms()
        if not vms:
            print("No active Lua VMs found.")
        else:
            print(f"Active VMs: {len(vms)}")
            for i, vm_info in enumerate(vms, 1):
                print(f"   {i}. {vm_info}")
        
        # Additional system information
        try:
            import psutil
            print(f"\nSystem Information:")
            print(f"   CPU Usage: {psutil.cpu_percent()}%")
            print(f"   Memory Usage: {psutil.virtual_memory().percent}%")
        except ImportError:
            pass

    def get_status_summary(self) -> Dict[str, Any]:
        """Get a summary of the current BioXen status."""
        return {
            'available_genomes': len(self.available_genomes),
            'validated_genomes': len([g for g in self.available_genomes if g.validated]),
            'genomes_directory': str(self.genomes_dir),
            'total_genome_files': len(list(self.genomes_dir.glob("*.genome"))),
            'timestamp': datetime.now().isoformat()
        }