I can definitely help you with that. The code you provided has several issues, including duplicate methods, incorrect indentation, and logical errors in the `try/except` blocks.

    # ...existing code...

Below is the cleaned-up and corrected code for the `InteractiveBioXen` class.

```python
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
    def __init__(self):
        self.validator = BioXenGenomeValidator()
        self.available_genomes = []

    def download_genomes(self):
        """
        Manages the download and creation of real or simulated genome data.
        """
        print("\n⬇️ Download New Genomes")
        print("💡 You can select a real genome from NCBI or create a custom simulated one.")

        genome_options = [
            # ... (your list of genome options here, including download_all_real and custom)
        ]
        
        # This list of genome options appears to be cut off in your prompt,
        # but I will assume it exists and contains a custom option.
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

        choices = [Choice(opt["display"], opt) for opt in genome_options]
        choice = questionary.select("Select a genome to download:", choices=choices).ask()

        if choice is None:
            return

        accession = choice["accession"]
        name = choice["name"]
        size = choice["size"]
        
        if accession == "download_all_real":
            print("\n⚠️ This functionality is not yet fully implemented.")
            print("💡 Please select individual genomes for now.")
            questionary.press_any_key_to_continue().ask()
            return
            
        print(f"\n🌐 Attempting to download {accession} from NCBI...")
        
        try:
            # Try advanced download helper first
            from genome_download_helper import GenomeDownloadHelper
            download_helper = GenomeDownloadHelper("genomes")
            success, message = download_helper.download_genome(accession, name)
            
            # Verify if file was actually downloaded
            genome_file = Path("genomes") / f"{name}.genome"
            file_actually_downloaded = genome_file.exists() and genome_file.stat().st_size > 1000  # At least 1KB
            
            if file_actually_downloaded:
                file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                print(f"✅ Successfully downloaded {name}!")
                print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                print(f"   🧬 Ready for biological virtualization")
                print(f"   📁 File: {genome_file}")
            elif success:
                print(f"✅ Download helper reported success: {message}")
                print("   📊 Authentic NCBI data for {name}")
                print("   🧬 Ready for biological virtualization")
            else:
                print(f"⚠️ Download helper returned: {message}")
                print("🔄 Creating simulated genome for testing...")
                self._create_simulated_genome(accession, name, size)
        
        except ImportError:
            print("⚠️ Advanced download helper not available")
            print("🔍 Checking for existing downloaded files...")
            
            genome_file = Path("genomes") / f"{name}.genome"
            if genome_file.exists() and genome_file.stat().st_size > 1000:
                file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                print(f"✅ Found existing genome file!")
                print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                print(f"   🧬 Ready for biological virtualization")
                print(f"   📁 File: {genome_file}")
            else:
                print("💡 Using basic download method...")
                try:
                    subprocess.run(['ncbi-genome-download', '--help'], capture_output=True, check=True)
                    ncbi_download_available = True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    ncbi_download_available = False
                
                genomes_dir = Path("genomes")
                genomes_dir.mkdir(exist_ok=True)
                
                if ncbi_download_available:
                    print("⚠️ ncbi-genome-download is available but not integrated with the new helper.")
                    print("   💡 Please install genome_download_helper for a more robust experience.")
                    print("   🔄 Creating simulated genome for testing...")
                    self._create_simulated_genome(accession, name, size)
                else:
                    print("⚠️ ncbi-genome-download not available")
                    print("   💡 Install with: pip install ncbi-genome-download")
                    print("   🔄 Creating simulated genome for testing...")
                    self._create_simulated_genome(accession, name, size)
        
        except (subprocess.TimeoutExpired, Exception) as e:
            if isinstance(e, subprocess.TimeoutExpired):
                print("❌ Download timed out (>5 minutes)")
            else:
                print(f"❌ Error downloading genome: {e}")
            
            # Check if file was downloaded despite the error/timeout
            genome_file = Path("genomes") / f"{name}.genome"
            if genome_file.exists() and genome_file.stat().st_size > 1000:
                file_size_mb = genome_file.stat().st_size / (1024 * 1024)
                print(f"✅ File was downloaded successfully despite the error!")
                print(f"   📊 Authentic NCBI data ({file_size_mb:.1f} MB)")
                print(f"   🧬 Ready for biological virtualization")
            else:
                print("🔄 Creating simulated genome for testing...")
                self._create_simulated_genome(accession, name, size)

        questionary.press_any_key_to_continue().ask()

    def _create_simulated_genome(self, accession: str, name: str, size: int):
        """Create simulated genome data for testing purposes."""
        print(f"\n🔄 Generating simulated genome data for {accession}...")
        print(f"💡 Creating simulated genome data for testing and development")
        
        try:
            import random
            bases = ['A', 'T', 'G', 'C']
            genome_data = ''.join(random.choice(bases) for _ in range(size))
            
            if genome_data:
                self.available_genomes.append({
                    "accession": accession,
                    "name": name,
                    "data": genome_data
                })
                print(f"✅ Successfully created simulated {name}")
                print(f"   Accession: {accession}")
                print(f"   Size: {len(genome_data):,} base pairs")
                print(f"   ⚠️ Note: This is simulated data for testing purposes")
            else:
                print(f"❌ Failed to create genome data for {accession}")
        except Exception as e:
            print(f"❌ Error creating genome data: {e}")

    def validate_genomes(self):
        """Validate downloaded genomes."""
        # This method has a call to self._check_hypervisor() which is not defined in the provided code.
        # I've commented it out to allow the code to run, assuming it's a helper method that was not included.
        # if not self._check_hypervisor():
        #     return
            
        print("\n🧬 Load Genome for Analysis")
        print("📋 Scanning for available genomes...")
        
        genome_dir = Path("genomes")
        if not genome_dir.exists():
            print("❌ No genomes directory found.")
            print("💡 Use 'Download New Genomes' to get real bacterial genomes from NCBI")
            questionary.press_any_key_to_continue().ask()
            return
            
        genome_files = list(genome_dir.glob("*.genome"))
        
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
                name = genome_file.stem
                size_kb = genome_file.stat().st_size / 1024
                
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
                print(f"⚠️ Warning: Could not read {genome_file.name}: {e}")
        
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
                print("\n⚠️ Some genomes failed validation. Check the logs above.")
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

    def create_lua_vm(self):
        """
        Concise Lua VM orchestration using pylua-bioxen-vm library.
        """
        print("\n🌙 Create Lua VM (pylua-bioxen-vm)")
        print("💡 This option uses the pylua-bioxen-vm library for robust Lua VM orchestration.")
        print("   Make sure 'lua' and 'luasocket' are installed for networking features.")

        try:
            from pylua_bioxen_vm import VMManager
        except ImportError:
            print("❌ pylua-bioxen-vm library not installed. Install with: pip install pylua-bioxen-vm")
            print("   Or install from source: https://github.com/aptitudetechnology/pylua-bioxen-vm")
            questionary.press_any_key_to_continue().ask()
            return

        while True:
            action = questionary.select(
                "Choose Lua VM action:",
                choices=[
                    Choice("Start Server VM", "server"),
                    Choice("Start Client VM", "client"),
                    Choice("Start P2P VM", "p2p"),
                    Choice("Execute Lua code string", "code"),
                    Choice("Execute Lua script file", "script"),
                    Choice("Manage running VMs", "manage"),
                    Choice("Back to Main Menu", "back")
                ]
            ).ask()

            if action is None or action == "back":
                print("↩️ Returning to main menu.")
                break

            try:
                with VMManager() as manager:
                    if action == "server":
                        port = questionary.text("Enter port for Lua Server (e.g., 8080):", default="8080").ask()
                        if not port:
                            continue
                        vm_id = questionary.text("Enter VM ID (or press Enter for auto-generated):", default=f"server_{port}").ask() or f"server_{port}"
                        manager.create_vm(vm_id, networked=True)
                        future = manager.start_server_vm(vm_id, port=int(port))
                        print(f"🌐 Server VM '{vm_id}' listening on port {port}...")
                        try:
                            result = future.result(timeout=None)
                            print(result.get('stdout', ''))
                            if result.get('stderr'): print(f"STDERR: {result['stderr']}", file=sys.stderr)
                        except KeyboardInterrupt:
                            print("🛑 Server stopped.")
                            future.cancel()

                    elif action == "client":
                        ip = questionary.text("Enter Server IP (default: localhost):", default="localhost").ask()
                        port = questionary.text("Enter Server Port (e.g., 8080):", default="8080").ask()
                        message = questionary.text("Enter message to send to server:", default="Greetings, Lua Server!").ask()
                        if not ip or not port or not message:
                            continue
                        vm_id = questionary.text("Enter VM ID (or press Enter for auto-generated):", default=f"client_{ip}_{port}").ask() or f"client_{ip}_{port}"
                        manager.create_vm(vm_id, networked=True)
                        future = manager.start_client_vm(vm_id, ip, int(port), message)
                        print(f"🌐 Client VM '{vm_id}' connecting to {ip}:{port}...")
                        try:
                            result = future.result(timeout=10)
                            print(result.get('stdout', ''))
                            if result.get('stderr'): print(f"STDERR: {result['stderr']}", file=sys.stderr)
                        except Exception as e:
                            print(f"❌ Client error: {e}")

                    elif action == "p2p":
                        local_port = questionary.text("Enter local port for P2P VM (e.g., 8081):", default="8081").ask()
                        peer_ip_port = questionary.text("Enter peer IP:Port (e.g., localhost:8080, blank for none):").ask()
                        peer_ip, peer_port = None, None
                        if peer_ip_port:
                            try:
                                peer_ip, peer_port = peer_ip_port.split(":")
                                peer_port = int(peer_port)
                            except ValueError:
                                print("❌ Invalid peer IP:Port format.")
                                continue
                        vm_id = questionary.text("Enter VM ID (or press Enter for auto-generated):", default=f"p2p_{local_port}").ask() or f"p2p_{local_port}"
                        manager.create_vm(vm_id, networked=True)
                        future = manager.start_p2p_vm(vm_id, int(local_port), peer_ip, peer_port)
                        print(f"🌐 P2P VM '{vm_id}' running on port {local_port}...")
                        try:
                            result = future.result(timeout=35)
                            print(result.get('stdout', ''))
                            if result.get('stderr'): print(f"STDERR: {result['stderr']}", file=sys.stderr)
                        except KeyboardInterrupt:
                            print("🛑 P2P VM stopped.")
                            future.cancel()

                    elif action == "code":
                        lua_code = questionary.text("Enter Lua code to execute:").ask()
                        if not lua_code:
                            continue
                        vm_id = questionary.text("Enter VM ID (or press Enter for auto-generated):", default="code_exec").ask() or "code_exec"
                        manager.create_vm(vm_id, networked=False)
                        result = manager.execute_code(vm_id, lua_code)
                        print(result.get('stdout', ''))
                        if result.get('stderr'): print(f"STDERR: {result['stderr']}", file=sys.stderr)

                    elif action == "script":
                        file_path = questionary.text("Enter path to Lua script file:").ask()
                        if not file_path or not Path(file_path).is_file():
                            print(f"❌ Error: File not found at '{file_path}'.")
                            continue
                        vm_id = questionary.text("Enter VM ID (or press Enter for auto-generated):", default=f"script_{Path(file_path).stem}").ask() or f"script_{Path(file_path).stem}"
                        manager.create_vm(vm_id, networked=False)
                        result = manager.execute_script(vm_id, file_path)
                        print(result.get('stdout', ''))
                        if result.get('stderr'): print(f"STDERR: {result['stderr']}", file=sys.stderr)

                    elif action == "manage":
                        print("\n🖥️ VM Management")
                        vms = manager.list_vms()
                        if not vms:
                            print("No active Lua VMs found.")
                        else:
                            print(f"Active VMs: {len(vms)}")
                            for vm_info in vms:
                                print(f"   • {vm_info}")
                        mgmt_action = questionary.select(
                            "VM Management Actions:",
                            choices=[
                                Choice("List all VMs", "list"),
                                Choice("Stop a VM", "stop"),
                                Choice("Stop all VMs", "stop_all"),
                                Choice("Back", "back")
                            ]
                        ).ask()
                        if mgmt_action == "list":
                            for vm_info in manager.list_vms():
                                print(f"   • {vm_info}")
                        elif mgmt_action == "stop":
                            vm_to_stop = questionary.text("Enter VM ID to stop:").ask()
                            if vm_to_stop:
                                manager.stop_vm(vm_to_stop)
                                print(f"✅ Stopped VM: {vm_to_stop}")
                        elif mgmt_action == "stop_all":
                            confirm = questionary.confirm("Stop all active VMs?").ask()
                            if confirm:
                                manager.stop_all_vms()
                                print("✅ Stopped all VMs")

            except Exception as e:
                print(f"❌ Error: {e}", file=sys.stderr)
            questionary.press_any_key_to_continue().ask()
```