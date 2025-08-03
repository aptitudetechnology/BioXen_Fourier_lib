#!/usr/bin/env python3
"""
BioXen Terminal Visualization using Rich
Real-time DNA transcription and cellular process monitoring
"""

import json
import time
import random
from datetime import datetime
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich import box
from rich.spinner import Spinner


class DNAVisualizationBar:
    """Custom DNA strand visualization with transcription activity"""
    
    def __init__(self, length=40):
        self.length = length
        self.segments = ['░'] * length  # Inactive DNA segments
        self.transcription_bubbles = [False] * length
        
    def update(self, active_genes, gene_expression_rate):
        """Update DNA strand based on gene activity"""
        # Reset segments
        self.segments = ['░'] * self.length
        
        # Mark active segments
        active_count = min(int(active_genes * self.length / 20), self.length)
        for i in range(active_count):
            self.segments[i] = '█'  # Active DNA
            
        # Add transcription bubbles (animated)
        for i in range(active_count):
            if random.random() < gene_expression_rate / 100:
                self.transcription_bubbles[i] = random.random() > 0.5
            else:
                self.transcription_bubbles[i] = False
                
    def render(self):
        """Render DNA strand with transcription bubbles"""
        dna_str = ""
        bubble_str = ""
        
        for i, segment in enumerate(self.segments):
            if segment == '█':
                dna_str += f"[red]{segment}[/red]"  # Active DNA in red
            else:
                dna_str += f"[dim]{segment}[/dim]"  # Inactive DNA dimmed
                
            # Add transcription bubble above if active
            if i < len(self.transcription_bubbles) and self.transcription_bubbles[i]:
                bubble_str += "[yellow]●[/yellow]"
            else:
                bubble_str += " "
                
        return f"{bubble_str}\n{dna_str}"


class RibosomeActivity:
    """Visual representation of ribosome activity"""
    
    def __init__(self, max_ribosomes=80):
        self.max_ribosomes = max_ribosomes
        self.active_ribosomes = []
        
    def update(self, allocated_ribosomes, utilization_rate):
        """Update ribosome activity"""
        self.active_ribosomes = []
        
        for i in range(allocated_ribosomes):
            is_active = random.random() < (utilization_rate / 100)
            self.active_ribosomes.append(is_active)
            
    def render(self):
        """Render ribosome activity as colored dots"""
        ribosome_display = ""
        for i, active in enumerate(self.active_ribosomes):
            if active:
                ribosome_display += "[green]●[/green]"
            else:
                ribosome_display += "[dim]○[/dim]"
                
            # Add space every 10 for readability
            if (i + 1) % 10 == 0:
                ribosome_display += " "
                
        return ribosome_display


class BioXenTerminalMonitor:
    """Main terminal monitor for BioXen biological processes"""
    
    def __init__(self, data_source="bioxen_data.json"):
        self.console = Console()
        self.data_source = data_source
        self.dna_visualizers = {}
        self.ribosome_monitors = {}
        self.last_update = time.time()
        
    def load_data(self):
        """Load BioXen data from JSON file"""
        try:
            if Path(self.data_source).exists():
                with open(self.data_source, 'r') as f:
                    return json.load(f)
            else:
                # Return mock data if file doesn't exist
                return self.generate_mock_data()
        except Exception as e:
            self.console.print(f"[red]Error loading data: {e}[/red]")
            return self.generate_mock_data()
            
    def generate_mock_data(self):
        """Generate realistic mock data for demonstration"""
        return {
            "system": {
                "chassis_type": "E_coli_MG1655",
                "total_ribosomes": 80,
                "available_ribosomes": random.randint(20, 60),
                "timestamp": datetime.now().isoformat(),
                "atp_pool": random.randint(60, 95)
            },
            "vms": {
                f"vm_{i}": {
                    "vm_id": f"vm_{i}",
                    "atp_percentage": random.randint(50, 95),
                    "ribosomes": random.randint(5, 25),
                    "active_genes": random.randint(3, 15),
                    "protein_count": random.randint(20, 80),
                    "mrna_count": random.randint(2, 12),
                    "gene_expression_rate": random.randint(20, 90),
                    "ribosome_utilization": random.randint(40, 95)
                } for i in range(1, 5)
            }
        }
        
    def create_vm_panel(self, vm_id, vm_data):
        """Create a rich panel for a single VM"""
        # Initialize visualizers if needed
        if vm_id not in self.dna_visualizers:
            self.dna_visualizers[vm_id] = DNAVisualizationBar()
            self.ribosome_monitors[vm_id] = RibosomeActivity()
            
        # Update visualizers
        dna_viz = self.dna_visualizers[vm_id]
        ribo_mon = self.ribosome_monitors[vm_id]
        
        dna_viz.update(vm_data.get('active_genes', 0), 
                      vm_data.get('gene_expression_rate', 0))
        ribo_mon.update(vm_data.get('ribosomes', 0),
                       vm_data.get('ribosome_utilization', 0))
        
        # Create VM info table
        vm_table = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        vm_table.add_column("Metric", style="cyan")
        vm_table.add_column("Value", style="white")
        vm_table.add_column("Visual", style="white")
        
        # ATP level with progress bar
        atp_level = vm_data.get('atp_percentage', 0)
        atp_bar = "█" * int(atp_level / 5) + "░" * (20 - int(atp_level / 5))
        atp_color = "green" if atp_level > 70 else "yellow" if atp_level > 40 else "red"
        
        vm_table.add_row("ATP Level", f"{atp_level}%", f"[{atp_color}]{atp_bar}[/{atp_color}]")
        vm_table.add_row("Ribosomes", f"{vm_data.get('ribosomes', 0)}/80", ribo_mon.render())
        vm_table.add_row("Active Genes", f"{vm_data.get('active_genes', 0)}", f"[green]{vm_data.get('active_genes', 0)}[/green] genes")
        vm_table.add_row("Proteins", f"{vm_data.get('protein_count', 0)}", "🧬 " * min(vm_data.get('protein_count', 0) // 10, 8))
        vm_table.add_row("mRNA", f"{vm_data.get('mrna_count', 0)}", "📋 " * min(vm_data.get('mrna_count', 0), 6))
        
        # DNA transcription visualization
        dna_panel = Panel(
            Align.center(dna_viz.render()),
            title="DNA Transcription",
            border_style="blue"
        )
        
        # Combine VM table and DNA visualization
        vm_content = f"{vm_table}\n\n{dna_panel}"
        
        return Panel(
            vm_content,
            title=f"[bold cyan]{vm_id.upper()}[/bold cyan]",
            border_style="cyan"
        )
        
    def create_system_overview(self, data):
        """Create system overview panel"""
        system_data = data.get('system', {})
        
        overview_table = Table(show_header=True, box=box.ROUNDED)
        overview_table.add_column("System Metric", style="bold magenta")
        overview_table.add_column("Value", style="white")
        overview_table.add_column("Status", style="white")
        
        # System stats
        chassis = system_data.get('chassis_type', 'Unknown')
        total_ribosomes = system_data.get('total_ribosomes', 0)
        available_ribosomes = system_data.get('available_ribosomes', 0)
        atp_pool = system_data.get('atp_pool', 0)
        
        # Calculate VM stats
        vm_count = len(data.get('vms', {}))
        total_active_genes = sum(vm.get('active_genes', 0) for vm in data.get('vms', {}).values())
        avg_atp = sum(vm.get('atp_percentage', 0) for vm in data.get('vms', {}).values()) / max(vm_count, 1)
        
        overview_table.add_row("Chassis Type", chassis, "🦠 Active")
        overview_table.add_row("Active VMs", str(vm_count), f"{'🟢' if vm_count > 0 else '🔴'} {vm_count} running")
        overview_table.add_row("Ribosome Pool", f"{available_ribosomes}/{total_ribosomes}", 
                              f"{'🟢' if available_ribosomes > 20 else '🟡' if available_ribosomes > 10 else '🔴'}")
        overview_table.add_row("System ATP", f"{atp_pool}%", 
                              f"{'🟢' if atp_pool > 70 else '🟡' if atp_pool > 40 else '🔴'}")
        overview_table.add_row("Total Active Genes", str(total_active_genes), "🧬 Transcribing")
        overview_table.add_row("Avg VM ATP", f"{avg_atp:.1f}%", 
                              f"{'🟢' if avg_atp > 70 else '🟡' if avg_atp > 40 else '🔴'}")
        
        return Panel(
            overview_table,
            title="[bold green]BioXen Hypervisor Status[/bold green]",
            border_style="green"
        )
        
    def create_gene_activity_chart(self, data):
        """Create a visual chart of gene activity across VMs"""
        chart_table = Table(show_header=True, box=box.SIMPLE)
        chart_table.add_column("VM", style="cyan")
        chart_table.add_column("Gene Expression", style="white")
        chart_table.add_column("Transcription Rate", style="white")
        
        for vm_id, vm_data in data.get('vms', {}).items():
            active_genes = vm_data.get('active_genes', 0)
            expression_rate = vm_data.get('gene_expression_rate', 0)
            
            # Visual gene activity bar
            gene_bar = "█" * min(active_genes, 15) + "░" * (15 - min(active_genes, 15))
            
            # Expression rate visualization
            rate_color = "green" if expression_rate > 70 else "yellow" if expression_rate > 40 else "red"
            rate_bar = "▓" * int(expression_rate / 10) + "░" * (10 - int(expression_rate / 10))
            
            chart_table.add_row(
                vm_id,
                f"[red]{gene_bar}[/red] ({active_genes})",
                f"[{rate_color}]{rate_bar}[/{rate_color}] {expression_rate}%"
            )
            
        return Panel(
            chart_table,
            title="[bold yellow]Gene Expression Activity[/bold yellow]",
            border_style="yellow"
        )
        
    def create_layout(self, data):
        """Create the main terminal layout"""
        layout = Layout()
        
        # Split into header and body
        layout.split_column(
            Layout(name="header", size=12),
            Layout(name="body")
        )
        
        # Split body into overview and VMs
        layout["body"].split_row(
            Layout(name="overview", ratio=1),
            Layout(name="vms", ratio=2)
        )
        
        # Split overview into system status and gene activity
        layout["overview"].split_column(
            Layout(name="system"),
            Layout(name="genes")
        )
        
        # Create VM grid (2x2)
        vm_data = data.get('vms', {})
        vm_ids = list(vm_data.keys())[:4]  # Max 4 VMs for display
        
        if len(vm_ids) >= 2:
            layout["vms"].split_column(
                Layout(name="vm_row1"),
                Layout(name="vm_row2")
            )
            
            # Top row
            if len(vm_ids) >= 2:
                layout["vm_row1"].split_row(
                    Layout(self.create_vm_panel(vm_ids[0], vm_data[vm_ids[0]])),
                    Layout(self.create_vm_panel(vm_ids[1], vm_data[vm_ids[1]]))
                )
            
            # Bottom row
            if len(vm_ids) >= 4:
                layout["vm_row2"].split_row(
                    Layout(self.create_vm_panel(vm_ids[2], vm_data[vm_ids[2]])),
                    Layout(self.create_vm_panel(vm_ids[3], vm_data[vm_ids[3]]))
                )
            elif len(vm_ids) == 3:
                layout["vm_row2"].split_row(
                    Layout(self.create_vm_panel(vm_ids[2], vm_data[vm_ids[2]])),
                    Layout(Panel("", border_style="dim"))
                )
        else:
            # Single VM display
            if vm_ids:
                layout["vms"].update(self.create_vm_panel(vm_ids[0], vm_data[vm_ids[0]]))
        
        # Add header
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header_text = Text(f"BioXen DNA Transcription Monitor - {current_time}", style="bold blue")
        layout["header"].update(Panel(Align.center(header_text), border_style="blue"))
        
        # Add overview panels
        layout["system"].update(self.create_system_overview(data))
        layout["genes"].update(self.create_gene_activity_chart(data))
        
        return layout
        
    def run(self, refresh_rate=2.0):
        """Run the terminal monitor"""
        self.console.print("[bold green]Starting BioXen DNA Transcription Monitor...[/bold green]")
        time.sleep(1)
        
        try:
            with Live(self.create_layout(self.load_data()), refresh_per_second=refresh_rate, console=self.console) as live:
                while True:
                    time.sleep(1.0 / refresh_rate)
                    data = self.load_data()
                    live.update(self.create_layout(data))
                    
        except KeyboardInterrupt:
            self.console.print("\n[bold red]Monitor stopped by user[/bold red]")
        except Exception as e:
            self.console.print(f"\n[bold red]Error: {e}[/bold red]")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="BioXen Terminal DNA Transcription Monitor")
    parser.add_argument("--data", default="bioxen_data.json", help="Path to BioXen data file")
    parser.add_argument("--refresh", type=float, default=2.0, help="Refresh rate in Hz")
    
    args = parser.parse_args()
    
    monitor = BioXenTerminalMonitor(args.data)
    monitor.run(args.refresh)
