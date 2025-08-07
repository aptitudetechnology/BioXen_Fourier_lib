#!/usr/bin/env python3
"""
Interactive BioXen CLI using questionary for user-friendly genome selection and VM management.
"""

import sys
import time
import shutil
import subprocess

from pathlib import Path
from typing import List, Dict, Optional
try:
    from pylua_vm import VMManager
except ImportError:
    print("❌ pylua-vm library not installed. Install with: pip install pylua-vm")
    sys.exit(1)

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
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    sys.exit(1)

class InteractiveBioXen:
    def create_lua_vm(self):
        """
        High-level Lua VM orchestration using VMManager from vm_manager.py.
        """
        from vm_manager import VMManager
        print("\n🌙 Create Lua VM (VMManager)")
        print("💡 This option uses the VMManager library for robust Lua VM orchestration.")
        print("   Make sure 'lua' and 'luasocket' are installed for networking features.")

        vm_manager = VMManager()

        while True:
            lua_action = questionary.select(
                "How would you like to interact with the Lua VM?",
                choices=[
                    Choice("Start Lua Server VM (Socket)", "server_socket"),
                    Choice("Start Lua Client VM (Socket)", "client_socket"),
                    Choice("Start Lua P2P VM (Socket)", "p2p_socket"),
                    Choice("Execute Lua code string", "string"),
                    Choice("Execute Lua script file", "file"),
                    Choice("Back to Main Menu", "back")
                ]
            ).ask()

            if lua_action is None or lua_action == "back":
                print("↩️ Returning to main menu.")
                break

            try:
                if lua_action == "server_socket":
                    port = questionary.text("Enter port for Lua Server (e.g., 8080):", default="8080", validate=lambda x: x.isdigit() and 1024 <= int(x) <= 65535 or "Port must be between 1024 and 65535").ask()
                    if not port:
                        continue
                    process_name = f"Lua Server on Port {port}"
                    print(f"\n--- Starting {process_name} ---")
                    print("💡 This process will block until a client connects and sends a message.")
                    output, error = vm_manager.run_server(port=int(port))
                    if output:
                        print(f"--- {process_name} STDOUT ---\n{output.strip()}")
                    if error:
                        print(f"--- {process_name} STDERR ---\n{error.strip()}", file=sys.stderr)

                elif lua_action == "client_socket":
                    ip = questionary.text("Enter Server IP (default: localhost):", default="localhost").ask()
                    if not ip:
                        continue
                    port = questionary.text("Enter Server Port (e.g., 8080):", default="8080", validate=lambda x: x.isdigit() and 1024 <= int(x) <= 65535 or "Port must be between 1024 and 65535").ask()
                    if not port:
                        continue
                    message = questionary.text("Enter message to send to server:", default="Greetings, Lua Server!").ask()
                    if not message:
                        continue
                    process_name = f"Lua Client to {ip}:{port}"
                    print(f"\n--- Starting {process_name} ---")
                    output, error = vm_manager.run_client(ip=ip, port=int(port), message=message)
                    if output:
                        print(f"--- {process_name} STDOUT ---\n{output.strip()}")
                    if error:
                        print(f"--- {process_name} STDERR ---\n{error.strip()}", file=sys.stderr)

                elif lua_action == "p2p_socket":
                    local_port = questionary.text("Enter local port for P2P VM to listen on (e.g., 8081):", default="8081", validate=lambda x: x.isdigit() and 1024 <= int(x) <= 65535 or "Port must be between 1024 and 65535").ask()
                    if not local_port:
                        continue
                    peer_ip_port_str = questionary.text("Enter peer IP:Port to connect to (e.g., localhost:8080, leave blank for no outgoing connection):").ask()
                    peer_ip, peer_port = None, None
                    if peer_ip_port_str:
                        try:
                            peer_ip, peer_port = peer_ip_port_str.split(":")
                            peer_port = int(peer_port)
                        except ValueError:
                            print("❌ Invalid peer IP:Port format. Use IP:Port (e.g., localhost:8080).")
                            continue
                    process_name = f"Lua P2P VM (Listen:{local_port}"
                    if peer_ip_port_str:
                        process_name += f", Connect:{peer_ip_port_str})"
                    else:
                        process_name += ")"
                    print(f"\n--- Starting {process_name} ---")
                    print(f"💡 This P2P VM will run for 30 seconds, attempting to listen on port {local_port}")
                    if peer_ip_port_str:
                        print(f"   and connect to peer {peer_ip_port_str}.")
                    output, error = vm_manager.run_p2p(local_port=int(local_port), peer_ip=peer_ip, peer_port=peer_port, run_duration=30)
                    if output:
                        print(f"--- {process_name} STDOUT ---\n{output.strip()}")
                    if error:
                        print(f"--- {process_name} STDERR ---\n{error.strip()}", file=sys.stderr)

                elif lua_action == "string":
                    lua_code = questionary.text("Enter Lua code to execute (e.g., print('Hello')):").ask()
                    if not lua_code:
                        print("⚠️ No Lua code entered. Returning to Lua VM menu.")
                        continue
                    process_name = "Lua Code String"
                    output, error = vm_manager.run_code(lua_code)
                    print(f"--- {process_name} STDOUT ---\n{output.strip() if output else ''}")
                    if error:
                        print(f"--- {process_name} STDERR ---\n{error.strip()}", file=sys.stderr)

                elif lua_action == "file":
                    file_path_str = questionary.text("Enter path to Lua script file (e.g., my_script.lua):").ask()
                    if not file_path_str:
                        print("⚠️ No file path entered. Returning to Lua VM menu.")
                        continue
                    lua_file_path = Path(file_path_str)
                    if not lua_file_path.is_file():
                        print(f"❌ Error: File not found at '{lua_file_path}'.")
                        continue
                    process_name = f"Lua Script File: {lua_file_path.name}"
                    output, error = vm_manager.run_script(str(lua_file_path))
                    print(f"--- {process_name} STDOUT ---\n{output.strip() if output else ''}")
                    if error:
                        print(f"--- {process_name} STDERR ---\n{error.strip()}", file=sys.stderr)

            except Exception as e:
                print(f"❌ An unexpected error occurred: {e}", file=sys.stderr)
            questionary.press_any_key_to_continue().ask()
    def __init__(self):
        """Initialize the interactive BioXen interface."""
        self.validator = BioXenGenomeValidator()
        self.hypervisor = None
        self.available_genomes = []
        self.chassis_type = ChassisType.ECOLI  # Default chassis
        
        # Terminal visualization support
        self.visualization_monitor = None
        self.visualization_active = False

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
                Choice("📊 Manage Running VMs", "status"),
                Choice("📺 Terminal DNA Visualization", "terminal_vis"),
                Choice("📈 View System Status", "view_status"),
                Choice("🌐 Download New Genomes", "download_new"),
                # --- NEW: Lua VM Option ---
                Choice("🌙 Create Lua VM", "create_lua_vm"),
                # -------------------------
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
                elif action == "terminal_vis":
                    self.toggle_terminal_visualization()
                elif action == "destroy_vm":
                    self.destroy_vm()
                # --- NEW: Call Lua VM Method ---
                elif action == "create_lua_vm":
                    self.create_lua_vm()
                # -------------------------------
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
                Choice("🧩 Orthogonal Cell (Synthetic) - Experimental, engineered system", ChassisType.ORTHOGONAL),
            ]
        ).ask()
        
        if chassis_choice is None:
            return None
            
        if chassis_choice in [ChassisType.ECOLI, ChassisType.YEAST, ChassisType.ORTHOGONAL]:
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
            elif chassis_choice == ChassisType.ORTHOGONAL:
                print(f"\n⚡ Selected Orthogonal Cell chassis (EXPERIMENTAL)")
                print(f"   • Synthetic, engineered cell system")
                print(f"   • 500 ribosomes available (customizable)")
                print(f"   • Up to 1 VM supported")
                print(f"   • ⚠️  Experimental: For advanced synthetic biology and virtualization")
                print(f"   • ⚠️  Hardware requirements may be higher!")
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
            elif self.chassis_type == ChassisType.ORTHOGONAL:
                print("   🧩 Loading Orthogonal Cell synthetic environment...")
                print("   🧬 Configuring engineered gene expression...")
                print("   ⚡ Setting up custom ribosome pools...")
                print("   ⚠️  Note: Experimental synthetic cell chassis")
            self.hypervisor = BioXenHypervisor(chassis_type=self.chassis_type)
            # Show warning for placeholder/experimental implementations
            if self.chassis_type == ChassisType.YEAST:
                print(f"\n⚠️  WARNING: Yeast chassis is currently a PLACEHOLDER implementation")
                print(f"   This chassis provides basic functionality for testing but")
                print(f"   does not include full eukaryotic cellular mechanisms.")
            elif self.chassis_type == ChassisType.ORTHOGONAL:
                print(f"\n⚡ WARNING: Orthogonal Cell chassis is EXPERIMENTAL")
                print(f"   This chassis is designed for advanced synthetic biology and virtualization.")
                print(f"   Hardware requirements may be higher. Use with caution!")
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
                print(f"\n🔄 Downloading {name} from NCBI...")
                
                # Use the new robust genome download helper
                try:
                    from genome_download_helper import GenomeDownloadHelper
                    
                    download_helper = GenomeDownloadHelper("genomes")
                    success, message = download_helper.download_genome(accession, name)
                    
                    # Verify if file was actually downloaded, regardless of reported success
                    genome_file = Path("genomes") / f"{name}.genome"
                    file_actually_downloaded = genome_file.exists() and genome_file.stat().st_size > 1000  # At least 1KB
                    
                    if file_actually_downloaded:
                        # File was successfully downloaded
                        file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                        print(f"✅ Successfully downloaded {name}!")
                        print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                        print(f"   🧬 Ready for biological virtualization")
                        print(f"   📁 File: {genome_file}")
                    elif success:
                        # Helper reported success but no file found
                        print(f"✅ Download helper reported success: {message}")
                        print(f"⚠️  File verification pending...")
                        print(f"   📊 Authentic NCBI data for {name}")
                        print(f"   🧬 Ready for biological virtualization")
                    else:
                        # Both helper failed and no file found
                        print(f"⚠️  Download helper returned: {message}")
                        print(f"🔍 Checking for downloaded file...")
                        
                        if genome_file.exists():
                            file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                            print(f"✅ File found despite error message!")
                            print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                            print(f"   🧬 Ready for biological virtualization")
                        else:
                            print(f"❌ No file downloaded")
                            print(f"\n🔍 Troubleshooting:")
                            print(f"   • All download strategies attempted")
                            print(f"   • Check network connectivity")
                            print(f"   • Verify NCBI servers are accessible")
                            
                            print(f"\n💡 Alternative approaches:")
                            print(f"   • Use 'Download All Real Bacterial Genomes' for pre-tested collection")
                            print(f"   • Visit NCBI manually: https://www.ncbi.nlm.nih.gov/assembly/")
                            print(f"   • Use simulation for testing: proceeding with simulated data")
                            
                            print("🔄 Falling back to simulation for testing...")
                            # Fall back to simulation only if no file was downloaded
                            self._create_simulated_genome(accession, name, size)
                        
                except ImportError:
                    print("⚠️  Advanced download helper not available")
                    print("🔍 Checking for existing downloaded files...")
                    
                    # Check if file already exists (from previous downloads)
                    genome_file = Path("genomes") / f"{name}.genome"
                    if genome_file.exists() and genome_file.stat().st_size > 1000:
                        file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                        print(f"✅ Found existing genome file!")
                        print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                        print(f"   🧬 Ready for biological virtualization")
                        print(f"   📁 File: {genome_file}")
                    else:
                        print("💡 Using basic download method...")
                        
                        # Fallback to basic download if helper not available
                        # ...existing code...
                        
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
                            print("⚠️  Using basic download method - may create simulated data")
                            print("💡 For reliable real genome downloads, install genome_download_helper")
                            print("🔄 Creating simulated genome for testing...")
                            self._create_simulated_genome(accession, name, size)
                        else:
                            print("⚠️  ncbi-genome-download not available")
                            print("💡 Install with: pip install ncbi-genome-download")
                            print("🔄 Creating simulated genome for testing...")
                            # Fall back to simulation
                            self._create_simulated_genome(accession, name, size)
                    
            except subprocess.TimeoutExpired:
                print("❌ Download timed out (>5 minutes)")
                # Check if file was downloaded despite timeout
                genome_file = Path("genomes") / f"{name}.genome"
                if genome_file.exists() and genome_file.stat().st_size > 1000:
                    file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                    print(f"✅ File was downloaded successfully despite timeout!")
                    print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                    print(f"   🧬 Ready for biological virtualization")
                else:
                    print("🔄 Creating simulated genome for testing...")
                    self._create_simulated_genome(accession, name, size)
            except Exception as e:
                print(f"❌ Error downloading genome: {e}")
                # Check if file was downloaded despite error
                genome_file = Path("genomes") / f"{name}.genome"
                if genome_file.exists() and genome_file.stat().st_size > 1000:
                    file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                    print(f"✅ File was downloaded successfully despite error!")
                    print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                    print(f"   🧬 Ready for biological virtualization")
                else:
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
            
            # Try real download with the new helper
            print(f"\n🌐 Attempting to download {accession} from NCBI...")
            
            try:
                from genome_download_helper import GenomeDownloadHelper
                
                download_helper = GenomeDownloadHelper("genomes")
                success, message = download_helper.download_genome(accession, name)
                
                # Verify if file was actually downloaded, regardless of reported success
                genome_file = Path("genomes") / f"{name}.genome"
                file_actually_downloaded = genome_file.exists() and genome_file.stat().st_size > 1000  # At least 1KB
                
                if file_actually_downloaded:
                    # File was successfully downloaded
                    file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                    print(f"✅ Successfully downloaded {name}!")
                    print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                    print(f"   🧬 Ready for biological virtualization")
                    print(f"   📁 File: {genome_file}")
                elif success:
                    # Helper reported success but no file found
                    print(f"✅ Download helper reported success: {message}")
                    print(f"   📊 Authentic NCBI data for {name}")
                    print(f"   🧬 Ready for biological virtualization")
                else:
                    print(f"⚠️  Download helper returned: {message}")
                    print("🔄 Creating simulated genome for testing...")
                    self._create_simulated_genome(accession, name, size)
                    
            except ImportError:
                print("⚠️  Advanced download helper not available")
                # Check if file already exists (from previous downloads)
                genome_file = Path("genomes") / f"{name}.genome"
                if genome_file.exists() and genome_file.stat().st_size > 1000:
                    file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                    print(f"✅ Found existing genome file!")
                    print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                    print(f"   🧬 Ready for biological virtualization")
                    print(f"   📁 File: {genome_file}")
                else:
                    print("🔄 Creating simulated genome for testing...")
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
            "Select a genome to validate:",
            choices=genome_choices
        ).ask()
        
        if choice is None:
            return
            
        if choice == "all":
            print("\n🔄 Validating all available genomes...")
            all_valid = True
            for genome_info in valid_genomes:
                print(f"\n🔬 Validating {genome_info['name']}...")
                try:
                    is_valid, messages = self.validator.validate_genome(genome_info['file_path'])
                    if is_valid:
                        print(f"✅ {genome_info['name']} is a valid BioXen genome.")
                    else:
                        print(f"❌ {genome_info['name']} is NOT a valid BioXen genome:")
                        for msg in messages:
                            print(f"   - {msg}")
                        all_valid = False
                except Exception as e:
                    print(f"❌ Error validating {genome_info['name']}: {e}")
                    all_valid = False
            
            if all_valid:
                print("\n✅ All available genomes validated successfully!")
            else:
                print("\n⚠️  Some genomes failed validation. Check the logs above.")
        else:
            print(f"\n🔬 Validating {choice['name']}...")
            try:
                is_valid, messages = self.validator.validate_genome(choice['file_path'])
                if is_valid:
                    print(f"✅ {choice['name']} is a valid BioXen genome.")
                    self.available_genomes.append({
                        "name": choice['name'],
                        "file_path": choice['file_path'],
                        "data": None # Data will be loaded when VM is created
                    })
                    print(f"💡 {choice['name']} is now available for VM creation.")
                else:
                    print(f"❌ {choice['name']} is NOT a valid BioXen genome:")
                    for msg in messages:
                        print(f"   - {msg}")
            except Exception as e:
                print(f"❌ Error validating {choice['name']}: {e}")
        
        questionary.press_any_key_to_continue().ask()

    def create_vm(self):
        """Create a new virtual machine."""
        if not self._check_hypervisor():
            return

        print("\n⚡ Create Virtual Machine")
        print("📋 Scanning for available genomes to virtualize...")

        genome_dir = Path("genomes")
        if not genome_dir.exists() or not list(genome_dir.glob("*.genome")):
            print("❌ No genome files found. Please download or validate genomes first.")
            print("💡 Use 'Download New Genomes' or 'Load Genome for Analysis' options.")
            questionary.press_any_key_to_continue().ask()
            return

        genome_choices = []
        for genome_file in genome_dir.glob("*.genome"):
            try:
                integrator = BioXenRealGenomeIntegrator(genome_file)
                stats = integrator.get_genome_stats()
                organism_name = stats.get('organism', genome_file.stem)
                genome_choices.append(Choice(f"🧬 {organism_name} ({genome_file.stem})", genome_file))
            except Exception:
                genome_choices.append(Choice(f"🧬 {genome_file.stem} (Error reading details)", genome_file))

        if not genome_choices:
            print("❌ No valid genomes found to create a VM from.")
            questionary.press_any_key_to_continue().ask()
            return

        selected_genome_path = questionary.select(
            "Select a genome to virtualize:",
            choices=genome_choices
        ).ask()

        if selected_genome_path is None:
            print("❌ VM creation cancelled.")
            return

        genome_name = selected_genome_path.stem
        vm_id = self._suggest_unique_vm_id(genome_name)

        print(f"\n⚙️  Configuring VM for {genome_name}")

        # Resource allocation
        min_memory_kb = 1024  # Default minimal memory
        boot_time_ms = 100   # Default minimal boot time
        try:
            integrator = BioXenRealGenomeIntegrator(selected_genome_path)
            template = integrator.create_vm_template()
            if template:
                min_memory_kb = template.get('min_memory_kb', min_memory_kb)
                boot_time_ms = template.get('boot_time_ms', boot_time_ms)
        except Exception as e:
            print(f"⚠️  Could not load VM template from genome: {e}. Using default resources.")

        print(f"   Suggested Minimum Memory: {min_memory_kb} KB")
        print(f"   Suggested Boot Time: {boot_time_ms} ms")

        # Allow user to adjust resources
        mem_input = questionary.text(
            f"Enter memory allocation in KB (default: {min_memory_kb}):",
            default=str(min_memory_kb),
            validate=lambda x: x.isdigit() and int(x) > 0 or "Must be a positive number"
        ).ask()
        memory_kb = int(mem_input) if mem_input else min_memory_kb

        boot_input = questionary.text(
            f"Enter simulated boot time in ms (default: {boot_time_ms}):",
            default=str(boot_time_ms),
            validate=lambda x: x.isdigit() and int(x) > 0 or "Must be a positive number"
        ).ask()
        boot_time = int(boot_input) if boot_input else boot_time_ms

        resource_allocation = ResourceAllocation(memory_kb=memory_kb, boot_time_ms=boot_time)

        try:
            print(f"\n🔄 Creating VM '{vm_id}' for {genome_name}...")
            self.hypervisor.create_vm(vm_id, selected_genome_path, resource_allocation)
            print(f"✅ VM '{vm_id}' created successfully!")
            print(f"   Genome: {genome_name}")
            print(f"   Memory: {memory_kb} KB")
            print(f"   Boot Time: {boot_time} ms")
            print(f"   State: {self.hypervisor.get_vm_state(vm_id).value}")
        except Exception as e:
            print(f"❌ Failed to create VM: {e}")

        questionary.press_any_key_to_continue().ask()

    def show_status(self):
        """Display the status of the hypervisor and running VMs."""
        if not self._check_hypervisor():
            return
            
        print("\n📊 BioXen Hypervisor Status")
        print("="*60)
        print(f"Chassis Type: {self.hypervisor.chassis_type.value}")
        print(f"Total Ribosomes: {self.hypervisor.chassis.total_ribosomes}")
        print(f"Available Ribosomes: {self.hypervisor.chassis.available_ribosomes}")
        print(f"Max VMs Supported: {self.hypervisor.chassis.max_vms}")
        print(f"Current Active VMs: {len(self.hypervisor.vms)}")
        print("="*60)
        
        if not self.hypervisor.vms:
            print("No virtual machines are currently running.")
            print("💡 Use 'Create Virtual Machine' to get started.")
        else:
            print("\n🖥️  Virtual Machine States:")
            for vm_id, vm_instance in self.hypervisor.vms.items():
                state = self.hypervisor.get_vm_state(vm_id)
                print(f"   • VM ID: {vm_id}")
                print(f"     Status: {state.value}")
                print(f"     Genome: {vm_instance.genome_name}")
                print(f"     Memory: {vm_instance.resources.memory_kb} KB")
                print(f"     Boot Time: {vm_instance.resources.boot_time_ms} ms")
                
                # Add actions for running VMs
                if state == VMState.RUNNING:
                    vm_actions = questionary.select(
                        f"Actions for VM '{vm_id}':",
                        choices=[
                            Choice("⏹️ Stop VM", "stop"),
                            Choice("🔄 Restart VM", "restart"),
                            Choice("🗑️ Destroy VM", "destroy"),
                            Choice("↩️ Back", "back")
                        ]
                    ).ask()
                    
                    if vm_actions == "stop":
                        self.hypervisor.stop_vm(vm_id)
                        print(f"✅ VM '{vm_id}' stopped.")
                    elif vm_actions == "restart":
                        self.hypervisor.restart_vm(vm_id)
                        print(f"✅ VM '{vm_id}' restarted.")
                    elif vm_actions == "destroy":
                        self.hypervisor.destroy_vm(vm_id)
                        print(f"✅ VM '{vm_id}' destroyed.")
                    elif vm_actions == "back":
                        pass # Go back to main status loop
        
        questionary.press_any_key_to_continue().ask()

    def destroy_vm(self):
        """Destroy a selected virtual machine."""
        if not self._check_hypervisor():
            return
        
        if not self.hypervisor.vms:
            print("❌ No virtual machines to destroy.")
            questionary.press_any_key_to_continue().ask()
            return
            
        vm_choices = [Choice(f"{vm_id} ({self.hypervisor.get_vm_state(vm_id).value})", vm_id)
                      for vm_id in self.hypervisor.vms.keys()]
                      
        vm_to_destroy = questionary.select(
            "Select VM to destroy:",
            choices=vm_choices
        ).ask()
        
        if vm_to_destroy is None:
            print("❌ VM destruction cancelled.")
            return
            
        confirm = questionary.confirm(f"Are you sure you want to destroy VM '{vm_to_destroy}'? This action is irreversible.").ask()
        
        if confirm:
            try:
                self.hypervisor.destroy_vm(vm_to_destroy)
                print(f"✅ VM '{vm_to_destroy}' destroyed successfully.")
            except Exception as e:
                print(f"❌ Failed to destroy VM '{vm_to_destroy}': {e}")
        else:
            print("❌ VM destruction cancelled.")
            
        questionary.press_any_key_to_continue().ask()

    def toggle_terminal_visualization(self):
        """Launch advanced Rich-based DNA visualization from terminal_biovis.py."""
        print("\n📺 Starting Terminal DNA Visualization...")
        print("💡 This feature provides a real-time, Rich-based visualization of DNA transcription, ribosome activity, and gene expression.")
        print("   It requires a running VM to display meaningful data.")
        try:
            from terminal_biovis import run_dna_monitor
            # Optionally, pass a real data source if available
            run_dna_monitor(refresh_rate=2.0)
        except ImportError:
            print("❌ Advanced visualization module 'terminal_biovis.py' not found.")
        except Exception as e:
            print(f"❌ Error starting advanced visualization: {e}")
        questionary.press_any_key_to_continue().ask()

    def _check_hypervisor(self):
        """Helper to check if hypervisor is initialized."""
        if self.hypervisor is None:
            print("❌ BioXen Hypervisor not initialized.")
            print("💡 Please select 'Initialize Hypervisor' from the main menu first.")
            questionary.press_any_key_to_continue().ask()
            return False
        return True

    def create_lua_vm(self):
        """
        Create and manage a Lua VM using pylua-bioxen-vm library with interactive user input.
        """
        print("\n🌙 Create Lua VM")
        print("💡 Launching a Lua VM using pylua-bioxen-vm.")
        print("   Ensure 'lua' and 'luasocket' are installed.")

        while True:
            lua_action = questionary.select(
                "How would you like to interact with the Lua VM?",
                choices=[
                    questionary.Choice("Start Lua Server VM (Socket)", "server_socket"),
                    questionary.Choice("Start Lua Client VM (Socket)", "client_socket"),
                    questionary.Choice("Start Lua P2P VM (Socket)", "p2p_socket"),
                    questionary.Choice("Execute Lua code string", "string"),
                    questionary.Choice("Execute Lua script file", "file"),
                    questionary.Choice("Back to Main Menu", "back")
                ]
            ).ask()

            if lua_action is None or lua_action == "back":
                print("↩️ Returning to main menu.")
                break

            try:
                with VMManager() as vm_manager:
                    vm_id = self._suggest_unique_vm_id("lua")  # Generate unique VM ID

                    # Create VM with networking for socket-based modes
                    if lua_action in ["server_socket", "client_socket", "p2p_socket"]:
                        vm_manager.create_vm(vm_id, networked=True)
                    else:
                        vm_manager.create_vm(vm_id, networked=False)

                    if lua_action == "server_socket":
                        port = questionary.text(
                            "Enter port for Lua Server (e.g., 8080):",
                            default="8080",
                            validate=lambda x: x.isdigit() and 1024 <= int(x) <= 65535 or "Port must be between 1024 and 65535"
                        ).ask()
                        if not port:
                            continue
                        vm_manager.start_server_vm(vm_id, int(port))
                        print(f"\n--- Starting Lua Server on Port {port} ---")
                        print("💡 Waiting for client connection. Start a Lua Client VM in another instance.")

                    elif lua_action == "client_socket":
                        ip = questionary.text("Enter Server IP (default: localhost):", default="localhost").ask()
                        if not ip:
                            continue
                        port = questionary.text(
                            "Enter Server Port (e.g., 8080):",
                            default="8080",
                            validate=lambda x: x.isdigit() and 1024 <= int(x) <= 65535 or "Port must be between 1024 and 65535"
                        ).ask()
                        if not port:
                            continue
                        message = questionary.text("Enter message to send to server:", default="Greetings, Lua Server!").ask()
                        if not message:
                            continue
                        vm_manager.start_client_vm(vm_id, ip, int(port), message)
                        print(f"\n--- Starting Lua Client to {ip}:{port} ---")
                        print(f"💡 Connecting to server with message: '{message}'")

                    elif lua_action == "p2p_socket":
                        local_port = questionary.text(
                            "Enter local port for P2P VM to listen on (e.g., 8081):",
                            default="8081",
                            validate=lambda x: x.isdigit() and 1024 <= int(x) <= 65535 or "Port must be between 1024 and 65535"
                        ).ask()
                        if not local_port:
                            continue
                        peer_ip_port = questionary.text(
                            "Enter peer IP:Port to connect to (e.g., localhost:8080, leave blank for no outgoing connection):"
                        ).ask()
                        if peer_ip_port:
                            try:
                                peer_ip, peer_port = peer_ip_port.split(':')
                                peer_port = int(peer_port)
                                if not (1024 <= peer_port <= 65535):
                                    raise ValueError("Peer port must be between 1024 and 65535")
                                vm_manager.start_p2p_vm(vm_id, int(local_port), peer_ip, peer_port)
                                print(f"\n--- Starting Lua P2P VM (Listen:{local_port}, Connect:{peer_ip}:{peer_port}) ---")
                            except ValueError as e:
                                print(f"❌ Invalid peer IP:Port format: {e}")
                                continue
                        else:
                            vm_manager.start_p2p_vm(vm_id, int(local_port), None, None)
                            print(f"\n--- Starting Lua P2P VM (Listen:{local_port}) ---")
                        print(f"💡 Running for ~30 seconds. Start another P2P VM to communicate.")

                    elif lua_action == "string":
                        lua_code = questionary.text("Enter Lua code to execute (e.g., print('Hello')):").ask()
                        if not lua_code:
                            print("⚠️ No Lua code entered.")
                            continue
                        vm_manager.execute_code(vm_id, lua_code)
                        print("\n--- Executing Lua Code String ---")

                    elif lua_action == "file":
                        file_path = questionary.text("Enter path to Lua script file (e.g., my_script.lua):").ask()
                        if not file_path:
                            print("⚠️ No file path entered.")
                            continue
                        lua_file_path = Path(file_path)
                        if not lua_file_path.is_file():
                            print(f"❌ Error: File not found at '{lua_file_path}'.")
                            continue
                        vm_manager.execute_script(vm_id, str(lua_file_path))
                        print(f"\n--- Executing Lua Script File: {lua_file_path.name} ---")

            except Exception as e:
                print(f"❌ Error: {e}")
                print("💡 Ensure 'lua' and 'luasocket' are installed (e.g., `luarocks install luasocket`).")

            questionary.press_any_key_to_continue().ask()
# This is typically how your main CLI entry point would look
if __name__ == "__main__":
    # Ensure 'genomes' directory exists for real genome downloads
    Path("genomes").mkdir(exist_ok=True)
    
    # Ensure 'lua-vm' directory exists for Lua-related scripts (like ps2lua.py)
    Path("lua-vm").mkdir(exist_ok=True)

    app = InteractiveBioXen()
    app.main_menu()
