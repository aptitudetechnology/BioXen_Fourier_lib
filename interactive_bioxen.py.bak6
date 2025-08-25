#!/usr/bin/env python3
"""
Interactive BioXen CLI using questionary for genome selection and VM management.
Integrated with pylua_bioxen_vm_lib v0.1.6 package management system.
"""

import sys
import time
import logging
from pathlib import Path
from typing import List, Dict, Optional

sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    import questionary
    from questionary import Choice
except ImportError:
    print("❌ questionary not installed. Install with: pip install questionary")
    sys.exit(1)

try:
    from pylua_bioxen_vm_lib import VMManager, InteractiveSession, SessionManager
    from pylua_bioxen_vm_lib.exceptions import (
        InteractiveSessionError, AttachError, DetachError, 
        SessionNotFoundError, SessionAlreadyExistsError, 
        VMManagerError, LuaVMError
    )
    from pylua_bioxen_vm_lib.utils.curator import (
        Curator, get_curator, bootstrap_lua_environment, Package,
        PackageRegistry, DependencyResolver, PackageInstaller,
        PackageValidator, search_packages
    )
    from pylua_bioxen_vm_lib.env import EnvironmentManager
    from pylua_bioxen_vm_lib.package_manager import (
        PackageManager, InstallationManager, RepositoryManager
    )
    MODERN_VM_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Modern VM library not available: {e}")
    print("💡 Install with: pip install pylua-bioxen-vm-lib")
    MODERN_VM_AVAILABLE = False

try:
    from genome.parser import BioXenRealGenomeIntegrator
    from genome.schema import BioXenGenomeValidator
    from hypervisor.core import BioXenHypervisor, ResourceAllocation, VMState
    from chassis import ChassisType, BaseChassis, EcoliChassis, YeastChassis, OrthogonalChassis
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running from the BioXen root directory")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('bioxen.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

class InteractiveBioXen:
    """Interactive CLI for BioXen hypervisor and package management."""
    def __init__(self):
        self.validator = BioXenGenomeValidator()
        self.hypervisor = None
        self.available_genomes = []
        self.chassis_type = ChassisType.ECOLI
        self.visualization_monitor = None
        self.visualization_active = False
        if MODERN_VM_AVAILABLE:
            self.vm_manager = VMManager()
            self.curator = get_curator()
            self.env_manager = EnvironmentManager()
            self.package_manager = PackageManager()
            self.installation_manager = InstallationManager()
            self.repository_manager = RepositoryManager()
            self.package_registry = PackageRegistry()
            self.dependency_resolver = DependencyResolver()
            self.package_installer = PackageInstaller()
            self.package_validator = PackageValidator()
            logger.info("BioXen initialized with package management")
        else:
            logger.warning("BioXen initialized without modern VM support")

    def _check_hypervisor(self):
        """Check if hypervisor is initialized."""
        if self.hypervisor is None:
            print("❌ Hypervisor not initialized. Select 'Initialize Hypervisor' from main menu.")
            return False
        return True

    def _suggest_unique_vm_id(self, base_name: str) -> str:
        """Suggest a unique VM ID."""
        if not self.hypervisor or not self.hypervisor.vms:
            return f"vm_{base_name}"
        existing_ids = set(self.hypervisor.vms.keys())
        candidate = f"vm_{base_name}"
        if candidate not in existing_ids:
            return candidate
        for i in range(1, 100):
            candidate = f"vm_{base_name}_{i}"
            if candidate not in existing_ids:
                return candidate
        return f"vm_{base_name}_{int(time.time() % 10000)}"

    def main_menu(self):
        """Display main menu for BioXen operations."""
        while True:
            print("\n" + "="*60 + "\n🧬 BioXen Hypervisor - Interactive Genome Management\n" + "="*60)
            choices = [
                Choice("🔍 Browse Available Genomes", "browse_genomes"),
                Choice("🧬 Load Genome for Analysis", "validate"),
                Choice("🖥️ Initialize Hypervisor", "init_hypervisor"),
                Choice("🌐 Download New Genomes", "download_new"),
                Choice("⚡ Create Virtual Machine", "create_vm"),
                Choice("📊 Manage Running VMs", "status"),
                Choice("📺 Terminal DNA Visualization", "terminal_vis"),
                Choice("🗑️ Destroy VM", "destroy_vm"),
            ]
            if MODERN_VM_AVAILABLE:
                choices.extend([
                    Choice("🌙 Interactive Lua VM (One-shot)", "create_lua_vm"),
                    Choice("🖥️ Persistent Lua VM", "create_persistent_vm"),
                    Choice("🔗 Attach to Lua VM", "attach_lua_vm"),
                    Choice("📦 Package Management", "package_management_menu"),
                ])
            choices.append(Choice("❌ Exit", "exit"))
            action = questionary.select("What would you like to do?", choices=choices, use_shortcuts=True).ask()
            if action is None or action == "exit":
                print("👋 Goodbye!")
                break
            try:
                getattr(self, action)()
            except KeyboardInterrupt:
                print("\n⚠️ Operation cancelled")
                continue
            except Exception as e:
                logger.error(f"Main menu error: {e}")
                print(f"❌ Error: {e}")
                questionary.press_any_key_to_continue().ask()

    def package_management_menu(self):
        """Package management menu for Lua operations."""
        while True:
            choices = [
                Choice("🔍 Search Packages", "search_lua_packages"),
                Choice("📋 List Installed", "list_installed_packages"),
                Choice("⬇️ Install Package", "install_lua_package"),
                Choice("⬆️ Update Package", "update_lua_package"),
                Choice("🗑️ Remove Package", "remove_lua_package"),
                Choice("📊 Package Info", "package_info"),
                Choice("🔄 Update All Packages", "update_all_packages"),
                Choice("🏗️ Bootstrap Environment", "bootstrap_lua_environment"),
                Choice("🔧 Manage Environments", "manage_lua_environments"),
                Choice("⚙️ Package Settings", "package_settings"),
                Choice("🔙 Back", "back")
            ]
            choice = questionary.select("📦 Package Management", choices=choices).ask()
            if choice is None or choice == "back":
                break
            try:
                getattr(self, choice)()
            except KeyboardInterrupt:
                print("\n⚠️ Operation cancelled")
                continue
            except Exception as e:
                logger.error(f"Package management error: {e}")
                print(f"❌ Error: {e}")
                questionary.press_any_key_to_continue().ask()

    def search_lua_packages(self):
        """Search for Lua packages."""
        query = questionary.text("🔍 Enter search query:").ask()
        if not query:
            return
        try:
            packages = search_packages(query)
            if packages:
                print(f"\n📦 Found {len(packages)} packages:")
                for pkg in packages:
                    print(f"  • {pkg.name} ({pkg.version}) - {pkg.description}")
            else:
                print("❌ No packages found")
        except Exception as e:
            logger.error(f"Search error: {e}")
            print(f"❌ Search error: {e}")
        questionary.press_any_key_to_continue().ask()

    def install_lua_package(self):
        """Install a Lua package."""
        package_name = questionary.text("📦 Package name to install:").ask()
        if not package_name:
            return
        version = questionary.text("🏷️ Version (leave empty for latest):").ask()
        try:
            print(f"🔄 Installing '{package_name}'...")
            success = self.package_installer.install_package(package_name, version=version) if version else self.package_installer.install_package(package_name)
            print(f"{'✅' if success else '❌'} Package '{package_name}' {'installed' if success else 'failed to install'}")
        except Exception as e:
            logger.error(f"Installation error: {e}")
            print(f"❌ Installation error: {e}")
        questionary.press_any_key_to_continue().ask()

    def list_installed_packages(self):
        """List installed Lua packages."""
        try:
            packages = self.package_registry.get_installed_packages()
            if packages:
                print(f"\n📋 Installed Packages ({len(packages)}):")
                for pkg in packages:
                    print(f"  • {pkg.name} ({pkg.version}) - {pkg.description}")
            else:
                print("📦 No packages installed")
        except Exception as e:
            logger.error(f"Error listing packages: {e}")
            print(f"❌ Error listing packages: {e}")
        questionary.press_any_key_to_continue().ask()

    def update_lua_package(self):
        """Update a Lua package."""
        try:
            installed = self.package_registry.get_installed_packages()
            if not installed:
                print("📦 No packages installed")
                return
            choices = [Choice(f"{pkg.name} ({pkg.version})", pkg.name) for pkg in installed]
            package_name = questionary.select("⬆️ Select package to update:", choices=choices).ask()
            if package_name:
                print(f"🔄 Updating '{package_name}'...")
                success = self.package_installer.update_package(package_name)
                print(f"{'✅' if success else '❌'} Package '{package_name}' {'updated' if success else 'failed to update'}")
        except Exception as e:
            logger.error(f"Update error: {e}")
            print(f"❌ Update error: {e}")
        questionary.press_any_key_to_continue().ask()

    def remove_lua_package(self):
        """Remove a Lua package."""
        try:
            installed = self.package_registry.get_installed_packages()
            if not installed:
                print("📦 No packages installed")
                return
            choices = [Choice(f"{pkg.name} ({pkg.version})", pkg.name) for pkg in installed]
            package_name = questionary.select("🗑️ Select package to remove:", choices=choices).ask()
            if package_name and questionary.confirm(f"Are you sure you want to remove '{package_name}'?").ask():
                success = self.package_installer.remove_package(package_name)
                print(f"{'✅' if success else '❌'} Package '{package_name}' {'removed' if success else 'failed to remove'}")
        except Exception as e:
            logger.error(f"Removal error: {e}")
            print(f"❌ Removal error: {e}")
        questionary.press_any_key_to_continue().ask()

    def bootstrap_lua_environment(self):
        """Bootstrap a Lua environment."""
        env_name = questionary.text("🏗️ Environment name:").ask()
        if not env_name:
            return
        try:
            print(f"🔄 Bootstrapping '{env_name}'...")
            success = bootstrap_lua_environment(env_name)
            print(f"{'✅' if success else '❌'} Environment '{env_name}' {'bootstrapped' if success else 'failed to bootstrap'}")
        except Exception as e:
            logger.error(f"Bootstrap error: {e}")
            print(f"❌ Bootstrap error: {e}")
        questionary.press_any_key_to_continue().ask()

    def manage_lua_environments(self):
        """Manage Lua environments."""
        try:
            choices = [
                Choice("🆕 Create New Environment", "create_env"),
                Choice("🔄 Switch Environment", "switch_env"),
                Choice("📋 List Environments", "list_env"),
                Choice("🗑️ Delete Environment", "delete_env"),
                Choice("🔙 Back", "back")
            ]
            action = questionary.select("🔧 Environment Management:", choices=choices).ask()
            if action == "create_env":
                env_name = questionary.text("Environment name:").ask()
                if env_name:
                    self.env_manager.create_environment(env_name)
                    print(f"✅ Environment '{env_name}' created")
            elif action == "switch_env":
                environments = self.env_manager.list_environments()
                if environments:
                    choices = [Choice(env.name, env.name) for env in environments]
                    selected = questionary.select("Select environment:", choices=choices).ask()
                    if selected:
                        self.env_manager.activate_environment(selected)
                        print(f"✅ Switched to '{selected}'")
                else:
                    print("No environments available")
            elif action == "list_env":
                environments = self.env_manager.list_environments()
                if environments:
                    print("\n📋 Available Environments:")
                    for env in environments:
                        print(f"  {'✅' if env.is_active else '  '} {env.name}")
                else:
                    print("📋 No environments created")
            elif action == "delete_env":
                environments = self.env_manager.list_environments()
                if environments:
                    choices = [Choice(env.name, env.name) for env in environments]
                    selected = questionary.select("Delete environment:", choices=choices).ask()
                    if selected and questionary.confirm(f"Delete '{selected}'?").ask():
                        self.env_manager.delete_environment(selected)
                        print(f"✅ Environment '{selected}' deleted")
                else:
                    print("No environments to delete")
        except Exception as e:
            logger.error(f"Environment management error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def package_info(self):
        """Display Lua package info."""
        package_name = questionary.text("📊 Package name for info:").ask()
        if not package_name:
            return
        try:
            package_info = self.package_registry.get_package_info(package_name)
            if package_info is None:
                print(f"❌ Package '{package_name}' not found")
                return
            print(f"\n📦 Package: {package_name}")
            print(f"   Version: {package_info.version}")
            print(f"   Description: {package_info.description}")
            print(f"   Dependencies: {', '.join(package_info.dependencies) if package_info.dependencies else 'None'}")
            print(f"   Author: {getattr(package_info, 'author', 'Unknown')}")
            print(f"   License: {getattr(package_info, 'license', 'Unknown')}")
        except Exception as e:
            logger.error(f"Package info error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def update_all_packages(self):
        """Update all Lua packages."""
        try:
            installed = self.package_registry.get_installed_packages()
            if not installed:
                print("📦 No packages installed")
                return
            if not questionary.confirm(f"Update all {len(installed)} packages?").ask():
                return
            print(f"🔄 Updating {len(installed)} packages...")
            updated_count = 0
            for package in installed:
                try:
                    success = self.package_installer.update_package(package.name)
                    print(f"  {'✅' if success else '⚠️'} {package.name} {'updated' if success else '- no update available'}")
                    if success:
                        updated_count += 1
                except Exception as e:
                    print(f"  ❌ {package.name} - update failed: {e}")
            print(f"✅ Updated {updated_count}/{len(installed)} packages")
        except Exception as e:
            logger.error(f"Update error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def package_settings(self):
        """Configure package settings."""
        try:
            choices = [
                Choice("📝 View Settings", "view_settings"),
                Choice("🔄 Update Repositories", "update_repos"),
                Choice("🧹 Clean Cache", "clean_cache"),
                Choice("🔧 Configure Manager", "configure"),
                Choice("🔙 Back", "back")
            ]
            action = questionary.select("⚙️ Package Settings:", choices=choices).ask()
            if action == "view_settings":
                settings = self.package_manager.get_settings()
                print("\n📝 Settings:")
                for key, value in settings.items():
                    print(f"  {key}: {value}")
            elif action == "update_repos":
                print("🔄 Updating repositories...")
                self.repository_manager.update_repositories()
                print("✅ Repositories updated")
            elif action == "clean_cache":
                print("🧹 Cleaning cache...")
                self.package_manager.clean_cache()
                print("✅ Cache cleaned")
            elif action == "configure":
                print("🔧 Configuration options not yet implemented")
        except Exception as e:
            logger.error(f"Settings error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def create_lua_vm(self):
        """Create one-shot Lua VM."""
        print("\n🌙 Interactive Lua VM (One-shot)\n💡 Temporary VM, exits on completion")
        use_packages = questionary.confirm("📦 Load installed packages?").ask()
        try:
            with self.vm_manager.create_interactive_session() as session:
                if use_packages:
                    try:
                        packages = self.package_registry.get_installed_packages()
                        for package in packages:
                            session.load_package(package.name)
                        print(f"📦 Loaded {len(packages)} packages")
                    except Exception as e:
                        logger.warning(f"Package load error: {e}")
                        print(f"⚠️ Warning: {e}")
                print("✅ Lua VM created\n💡 Type 'exit' or Ctrl+D to end")
                session.interactive_loop()
                print("👋 Lua session ended")
        except (VMManagerError, LuaVMError, InteractiveSessionError) as e:
            logger.error(f"VM error: {e}")
            print(f"❌ VM error: {e}")
        except KeyboardInterrupt:
            print("\n⚠️ Session interrupted")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def create_persistent_vm(self):
        """Create persistent Lua VM."""
        print("\n🖥️ Persistent Lua VM\n💡 Attachable multiple times")
        vm_id = questionary.text("Enter VM ID:", default=self._suggest_unique_vm_id("persistent_lua"), validate=lambda x: x.strip() != "" or "VM ID cannot be empty").ask()
        if not vm_id:
            return
        if self.vm_manager.list_sessions() and any(session.vm_id == vm_id for session in self.vm_manager.list_sessions()):
            print(f"❌ VM ID '{vm_id}' already exists")
            return
        env_choices = [Choice("Default Environment", None)] + [Choice(env.name, env.name) for env in self.env_manager.list_environments()]
        selected_env = questionary.select("Select environment:", choices=env_choices).ask()
        try:
            session = self.vm_manager.create_interactive_vm(vm_id)
            if selected_env:
                session.set_environment(selected_env)
                print(f"📦 Environment '{selected_env}' loaded")
            print(f"✅ VM '{vm_id}' created\n💡 Use 'Attach to Lua VM' to connect")
        except (SessionAlreadyExistsError, VMManagerError) as e:
            logger.error(f"VM creation error: {e}")
            print(f"❌ Error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def attach_lua_vm(self):
        """Attach to persistent Lua VM."""
        print("\n🔗 Attach to Lua VM")
        try:
            sessions = self.vm_manager.list_sessions()
            if not sessions:
                print("❌ No persistent VMs available\n💡 Create a persistent VM first")
                return
            choices = [Choice(f"🖥️ {session.vm_id}", session.vm_id) for session in sessions]
            selected_vm = questionary.select("Select VM to attach to:", choices=choices).ask()
            if not selected_vm:
                return
            print(f"🔗 Attaching to '{selected_vm}'...")
            session = self.vm_manager.attach_to_session(selected_vm)
            print("✅ Attached\n💡 Type 'exit' or Ctrl+D to detach")
            session.interactive_loop()
            print(f"👋 Detached from '{selected_vm}' (still running)")
        except (SessionNotFoundError, AttachError, DetachError) as e:
            logger.error(f"Attach error: {e}")
            print(f"❌ Error: {e}")
        except KeyboardInterrupt:
            print("\n⚠️ Detached by user")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def select_chassis(self):
        """Select biological chassis type."""
        print("\n🧬 Select Biological Chassis")
        chassis_choice = questionary.select(
            "Select chassis type:",
            choices=[
                Choice("🦠 E. coli (Prokaryotic) - Stable", ChassisType.ECOLI),
                Choice("🍄 Yeast (Eukaryotic) - PLACEHOLDER", ChassisType.YEAST),
                Choice("🧩 Orthogonal Cell (Synthetic) - Experimental", ChassisType.ORTHOGONAL),
            ]
        ).ask()
        if chassis_choice is None:
            return None
        self.chassis_type = chassis_choice
        if chassis_choice == ChassisType.ECOLI:
            print("\n✅ E. coli chassis: Prokaryotic, 80 ribosomes, 4 VMs max")
        elif chassis_choice == ChassisType.YEAST:
            print("\n⚠️ Yeast chassis (PLACEHOLDER): Eukaryotic, 200,000 ribosomes, 2 VMs max")
        elif chassis_choice == ChassisType.ORTHOGONAL:
            print("\n⚡ Orthogonal Cell chassis (EXPERIMENTAL): Synthetic, 500 ribosomes, 1 VM max")
        return chassis_choice

    def initialize_hypervisor(self):
        """Initialize BioXen hypervisor."""
        if self.hypervisor is not None:
            if not questionary.confirm("Hypervisor already initialized. Reinitialize?").ask():
                return
        print("\n🚀 Initializing BioXen Hypervisor")
        selected_chassis = self.select_chassis()
        if selected_chassis is None:
            print("❌ Chassis selection cancelled")
            return
        try:
            print(f"\n🔄 Initializing with {self.chassis_type.value} chassis...")
            self.hypervisor = BioXenHypervisor(chassis_type=self.chassis_type)
            if self.chassis_type == ChassisType.YEAST:
                print("\n⚠️ WARNING: Yeast chassis is a PLACEHOLDER implementation")
            elif self.chassis_type == ChassisType.ORTHOGONAL:
                print("\n⚡ WARNING: Orthogonal Cell chassis is EXPERIMENTAL")
            print(f"\n✅ Hypervisor initialized: {self.chassis_type.value}")
        except Exception as e:
            logger.error(f"Initialization failed: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def browse_available_genomes(self):
        """Browse available genomes."""
        print("\n🔍 Browse Available Genomes")
        genome_dir = Path("genomes")
        if not genome_dir.exists():
            print("❌ No genomes directory found.\n💡 Use 'Download New Genomes'")
            return questionary.press_any_key_to_continue().ask()
        genome_files = list(genome_dir.glob("*.genome"))
        if not genome_files:
            print("❌ No genome files found.\n💡 Use 'Download New Genomes'")
            return questionary.press_any_key_to_continue().ask()
        print(f"✅ Found {len(genome_files)} genomes\n" + "="*60)
        for i, genome_file in enumerate(genome_files, 1):
            try:
                name = genome_file.stem
                size_kb = genome_file.stat().st_size / 1024
                print(f"\n{i}. 🧬 {name}\n   📁 {genome_file.name}\n   💾 {size_kb:.1f} KB")
                try:
                    integrator = BioXenRealGenomeIntegrator(genome_file)
                    stats = integrator.get_genome_stats()
                    if stats:
                        print(f"   🔬 Genes: {stats.get('total_genes', 'Unknown')}")
                        if 'essential_genes' in stats:
                            print(f"   ⚡ Essential: {stats['essential_genes']} ({stats.get('essential_percentage', 0):.1f}%)")
                        print(f"   🦠 Organism: {stats.get('organism', 'Unknown')}")
                        template = integrator.create_vm_template()
                        if template:
                            print(f"   🖥️ VM Memory: {template.get('min_memory_kb', 'Unknown')} KB")
                            print(f"   ⏱️ Boot Time: {template.get('boot_time_ms', 'Unknown')} ms")
                except Exception as e:
                    logger.warning(f"Error reading {genome_file}: {e}")
                    print(f"   📊 Status: File available (details pending)")
            except Exception as e:
                logger.error(f"Error processing {genome_file}: {e}")
                print(f"   ❌ Error: {e}")
        print("\n" + "="*60 + f"\n📋 Total: {len(genome_files)} genomes\n💡 Use 'Load Genome' or 'Create VM'")
        questionary.press_any_key_to_continue().ask()

    def download_genomes(self):
        """Download genomes from NCBI."""
        if not self._check_hypervisor():
            return
        print("\n📥 Download Genomes from NCBI\n✅ 5 minimal bacterial genomes available")
        genome_options = [
            {"display": "🌐 All Real Bacterial Genomes", "accession": "download_all_real", "name": "all_real_genomes", "size": 0},
            {"display": "🦠 E. coli K-12 MG1655", "accession": "NC_000913.3", "name": "E_coli_K12_MG1655", "size": 4641652},
            {"display": "🍄 S. cerevisiae S288C", "accession": "NC_001133.9", "name": "S_cerevisiae_S288C", "size": 230218},
            {"display": "🔬 Mycoplasma genitalium", "accession": "NC_000908.2", "name": "M_genitalium", "size": 580076},
            {"display": "🌊 Prochlorococcus marinus", "accession": "NC_009840.1", "name": "P_marinus", "size": 1751080},
            {"display": "💀 Clostridium botulinum", "accession": "NC_009495.1", "name": "C_botulinum", "size": 3886916},
            {"display": "🧪 Custom genome", "accession": "custom", "name": "custom", "size": 1000000}
        ]
        choice = questionary.select("Select a genome to download:", choices=[Choice(opt["display"], opt) for opt in genome_options]).ask()
        if choice is None:
            return
        if choice["accession"] == "download_all_real":
            self._download_all_real_genomes()
        elif choice["accession"] == "custom":
            self._download_custom_genome()
        else:
            self._download_individual_genome(choice)
        questionary.press_any_key_to_continue().ask()

    def _download_all_real_genomes(self):
        """Download all bacterial genomes."""
        print("\n🌐 Downloading All Genomes\n📋 Includes: JCVI-Syn3A, M. genitalium, M. pneumoniae, C. ruddii, B. aphidicola")
        if not questionary.confirm("Download all 5 genomes?").ask():
            return
        try:
            import subprocess
            result = subprocess.run([sys.executable, 'download_genomes.py', 'all'], capture_output=True, text=True, cwd=Path(__file__).parent)
            if result.returncode == 0:
                print("✅ Downloaded all genomes!\n📋 Genomes: JCVI-Syn3A, M. genitalium, M. pneumoniae, C. ruddii, B. aphidicola")
            else:
                print(f"❌ Download failed: {result.stderr}\n💡 Try 'python3 download_genomes.py' manually")
        except Exception as e:
            logger.error(f"Download error: {e}")
            print(f"❌ Error: {e}\n💡 Try 'python3 download_genomes.py all' manually")
        questionary.press_any_key_to_continue().ask()

    def _download_individual_genome(self, genome_choice):
        """Download individual genome."""
        accession, name, size = genome_choice["accession"], genome_choice["name"], genome_choice["size"]
        print(f"\n🌐 Downloading {name}\n   Accession: {accession}\n   Size: {size:,} bp")
        if not questionary.confirm(f"Download {name} from NCBI?").ask():
            return
        try:
            from genome_download_helper import GenomeDownloadHelper
            download_helper = GenomeDownloadHelper("genomes")
            success, message = download_helper.download_genome(accession, name)
            genome_file = Path("genomes") / f"{name}.genome"
            if genome_file.exists() and genome_file.stat().st_size > 1000:
                print(f"✅ Downloaded {name}!\n   📊 {genome_file.stat().st_size / (1024 * 1024):.1f} MB\n   📁 {genome_file}")
            elif success:
                print(f"✅ Success: {message}")
            else:
                print(f"⚠️ {message}\n🔄 Creating simulated genome...")
                self._create_simulated_genome(accession, name, size)
        except ImportError:
            print("⚠️ Download helper unavailable\n🔄 Creating simulated genome...")
            self._create_simulated_genome(accession, name, size)
        except Exception as e:
            logger.error(f"Download error: {e}")
            print(f"❌ Error: {e}\n🔄 Creating simulated genome...")
            self._create_simulated_genome(accession, name, size)

    def _download_custom_genome(self):
        """Download custom genome."""
        accession = questionary.text("Enter NCBI accession (e.g., NC_000913.3):").ask()
        if not accession:
            return
        name = questionary.text("Enter genome name:").ask() or accession.replace(".", "_")
        self._download_individual_genome({"accession": accession, "name": name, "size": 1000000})

    def _create_simulated_genome(self, accession: str, name: str, size: int):
        """Create simulated genome for testing."""
        print(f"\n🔄 Generating simulated {name}...")
        try:
            import random
            genome_data = ''.join(random.choice(['A', 'T', 'G', 'C']) for _ in range(size))
            self.available_genomes.append({"accession": accession, "name": name, "data": genome_data})
            print(f"✅ Created {name}\n   Accession: {accession}\n   Size: {len(genome_data):,} bp\n   ⚠️ Simulated data")
        except Exception as e:
            logger.error(f"Simulated genome error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def validate_genomes(self):
        """Validate genomes."""
        if not self._check_hypervisor():
            return
        print("\n🧬 Load Genome for Analysis")
        genome_dir = Path("genomes")
        if not genome_dir.exists() or not list(genome_dir.glob("*.genome")):
            print("❌ No genomes found.\n💡 Use 'Download New Genomes'")
            return questionary.press_any_key_to_continue().ask()
        genome_files = list(genome_dir.glob("*.genome"))
        print(f"✅ Found {len(genome_files)} genomes")
        genome_choices = []
        valid_genomes = []
        for genome_file in genome_files:
            try:
                name = genome_file.stem
                size_kb = genome_file.stat().st_size / 1024
                try:
                    integrator = BioXenRealGenomeIntegrator(genome_file)
                    stats = integrator.get_genome_stats()
                    display_name = f"🧬 {stats.get('organism', name)} ({stats.get('total_genes', 'Unknown')} genes, {size_kb:.1f} KB)"
                except Exception:
                    display_name = f"🧬 {name} ({size_kb:.1f} KB)"
                genome_info = {'name': name, 'file_path': genome_file, 'display_name': display_name}
                genome_choices.append(Choice(display_name, genome_info))
                valid_genomes.append(genome_info)
            except Exception as e:
                logger.warning(f"Could not read {genome_file.name}: {e}")
                print(f"⚠️ Warning: {e}")
        if not valid_genomes:
            print("❌ No valid genomes found.\n💡 Use 'Download New Genomes'")
            return questionary.press_any_key_to_continue().ask()
        genome_choices.append(Choice("🔍 Validate all genomes", "all"))
        choice = questionary.select("Select a genome to validate:", choices=genome_choices).ask()
        if choice is None:
            return
        if choice == "all":
            self._validate_all_genomes(valid_genomes)
        else:
            self._validate_single_genome(choice)
        questionary.press_any_key_to_continue().ask()

    def _validate_all_genomes(self, valid_genomes):
        """Validate all genomes."""
        print("\n🔄 Validating all genomes...")
        all_valid = True
        for genome_info in valid_genomes:
            print(f"\n🔬 Validating {genome_info['name']}...")
            try:
                is_valid, messages = self.validator.validate_genome(genome_info['file_path'])
                if is_valid:
                    print(f"✅ Valid genome")
                else:
                    print(f"❌ Invalid genome:")
                    for msg in messages:
                        print(f"   - {msg}")
                    all_valid = False
            except Exception as e:
                logger.error(f"Validation error for {genome_info['name']}: {e}")
                print(f"❌ Error: {e}")
                all_valid = False
        print("\n" + ("✅ All genomes valid" if all_valid else "⚠️ Some genomes failed validation"))
        questionary.press_any_key_to_continue().ask()

    def _validate_single_genome(self, genome_choice):
        """Validate single genome."""
        print(f"\n🔬 Validating {genome_choice['name']}...")
        try:
            is_valid, messages = self.validator.validate_genome(genome_choice['file_path'])
            if is_valid:
                print(f"✅ Valid genome")
                self.available_genomes.append({"name": genome_choice['name'], "file_path": genome_choice['file_path'], "data": None})
                print(f"💡 Ready for VM creation")
            else:
                print(f"❌ Invalid genome:")
                for msg in messages:
                    print(f"   - {msg}")
        except Exception as e:
            logger.error(f"Validation error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def create_vm(self):
        """Create new virtual machine."""
        if not self._check_hypervisor():
            return
        print("\n⚡ Create Virtual Machine")
        genome_dir = Path("genomes")
        if not genome_dir.exists() or not list(genome_dir.glob("*.genome")):
            print("❌ No genomes found.\n💡 Use 'Download New Genomes' or 'Load Genome'")
            return questionary.press_any_key_to_continue().ask()
        genome_choices = []
        for genome_file in genome_dir.glob("*.genome"):
            try:
                integrator = BioXenRealGenomeIntegrator(genome_file)
                stats = integrator.get_genome_stats()
                genome_choices.append(Choice(f"🧬 {stats.get('organism', genome_file.stem)} ({genome_file.stem})", genome_file))
            except Exception:
                genome_choices.append(Choice(f"🧬 {genome_file.stem} (Error reading details)", genome_file))
        if not genome_choices:
            print("❌ No valid genomes found")
            return questionary.press_any_key_to_continue().ask()
        selected_genome_path = questionary.select("Select a genome to virtualize:", choices=genome_choices).ask()
        if selected_genome_path is None:
            print("❌ VM creation cancelled")
            return
        genome_name = selected_genome_path.stem
        vm_id = self._suggest_unique_vm_id(genome_name)
        print(f"\n⚙️ Configuring VM for {genome_name}")
        min_memory_kb, boot_time_ms = 1024, 100
        try:
            integrator = BioXenRealGenomeIntegrator(selected_genome_path)
            template = integrator.create_vm_template()
            if template:
                min_memory_kb = template.get('min_memory_kb', min_memory_kb)
                boot_time_ms = template.get('boot_time_ms', boot_time_ms)
        except Exception as e:
            logger.warning(f"Template load error: {e}")
            print(f"⚠️ Using default resources: {e}")
        print(f"   Suggested Memory: {min_memory_kb} KB\n   Suggested Boot Time: {boot_time_ms} ms")
        mem_input = questionary.text(f"Enter memory (KB, default: {min_memory_kb}):", default=str(min_memory_kb), validate=lambda x: x.isdigit() and int(x) > 0 or "Must be positive").ask()
        memory_kb = int(mem_input) if mem_input else min_memory_kb
        boot_input = questionary.text(f"Enter boot time (ms, default: {boot_time_ms}):", default=str(boot_time_ms), validate=lambda x: x.isdigit() and int(x) > 0 or "Must be positive").ask()
        boot_time = int(boot_input) if boot_input else boot_time_ms
        try:
            print(f"\n🔄 Creating VM '{vm_id}'...")
            self.hypervisor.create_vm(vm_id, selected_genome_path, ResourceAllocation(memory_kb=memory_kb, boot_time_ms=boot_time))
            print(f"✅ VM '{vm_id}' created\n   Genome: {genome_name}\n   Memory: {memory_kb} KB\n   Boot Time: {boot_time} ms\n   State: {self.hypervisor.get_vm_state(vm_id).value}")
        except Exception as e:
            logger.error(f"VM creation error: {e}")
            print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def show_status(self):
        """Display hypervisor and VM status."""
        if not self._check_hypervisor():
            return
        print("\n📊 BioXen Hypervisor Status\n" + "="*60)
        print(f"Chassis: {self.hypervisor.chassis_type.value}\nRibosomes: {self.hypervisor.chassis.total_ribosomes} (Available: {self.hypervisor.chassis.available_ribosomes})\nMax VMs: {self.hypervisor.chassis.max_vms}\nActive VMs: {len(self.hypervisor.vms)}")
        if not self.hypervisor.vms:
            print("No VMs running.\n💡 Use 'Create Virtual Machine'")
        else:
            print("\n🖥️ Virtual Machine States:")
            for vm_id, vm_instance in self.hypervisor.vms.items():
                state = self.hypervisor.get_vm_state(vm_id)
                print(f"   • {vm_id}\n     Status: {state.value}\n     Genome: {vm_instance.genome_name}\n     Memory: {vm_instance.resources.memory_kb} KB\n     Boot Time: {vm_instance.resources.boot_time_ms} ms")
                if state == VMState.RUNNING:
                    vm_actions = questionary.select(f"Actions for '{vm_id}':", choices=[
                        Choice("⏹️ Stop VM", "stop"), Choice("🔄 Restart VM", "restart"), Choice("🗑️ Destroy VM", "destroy"), Choice("↩️ Back", "back")
                    ]).ask()
                    if vm_actions == "stop":
                        self.hypervisor.stop_vm(vm_id)
                        print(f"✅ '{vm_id}' stopped")
                    elif vm_actions == "restart":
                        self.hypervisor.restart_vm(vm_id)
                        print(f"✅ '{vm_id}' restarted")
                    elif vm_actions == "destroy":
                        self.hypervisor.destroy_vm(vm_id)
                        print(f"✅ '{vm_id}' destroyed")
        questionary.press_any_key_to_continue().ask()

    def destroy_vm(self):
        """Destroy a virtual machine."""
        if not self._check_hypervisor():
            return
        if not self.hypervisor.vms:
            print("❌ No VMs to destroy")
            return questionary.press_any_key_to_continue().ask()
        vm_choices = [Choice(f"{vm_id} ({self.hypervisor.get_vm_state(vm_id).value})", vm_id) for vm_id in self.hypervisor.vms.keys()]
        vm_to_destroy = questionary.select("Select VM to destroy:", choices=vm_choices).ask()
        if vm_to_destroy is None:
            print("❌ Destruction cancelled")
            return
        if questionary.confirm(f"Destroy '{vm_to_destroy}'? This is irreversible.").ask():
            try:
                self.hypervisor.destroy_vm(vm_to_destroy)
                print(f"✅ '{vm_to_destroy}' destroyed")
            except Exception as e:
                logger.error(f"Destruction error: {e}")
                print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

    def toggle_terminal_visualization(self):
        """Toggle DNA visualization."""
        if not self._check_hypervisor():
            return
        if self.visualization_active:
            print("\n📺 Stopping visualization...")
            self.visualization_active = False
            if self.visualization_monitor:
                self.visualization_monitor.stop()
                self.visualization_monitor = None
            print("✅ Stopped")
        else:
            print("\n📺 Starting visualization...")
            try:
                print("⚠️ Visualization not fully implemented")
                self.visualization_active = True
                print("✅ Started (placeholder)")
            except Exception as e:
                logger.error(f"Visualization error: {e}")
                print(f"❌ Error: {e}")
        questionary.press_any_key_to_continue().ask()

if __name__ == "__main__":
    bioxen = InteractiveBioXen()
    bioxen.main_menu()