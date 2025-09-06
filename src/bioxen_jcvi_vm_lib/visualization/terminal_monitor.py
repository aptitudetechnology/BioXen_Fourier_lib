import sys
import time
import random
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn
from rich.panel import Panel
from rich.text import Text

class TerminalMonitor:
    def __init__(self, hypervisor):
        self.hypervisor = hypervisor
        self.running = False
        self.console = Console()

    def start(self):
        self.running = True
        self.console.clear()
        self.console.print("[bold magenta][TerminalMonitor][/bold magenta] Visualization started. Press Ctrl+C to stop.")
        try:
            while self.running:
                self.display()
                time.sleep(1)
        except KeyboardInterrupt:
            self.console.print("[bold yellow][TerminalMonitor][/bold yellow] Visualization stopped by user.")
            self.stop()

    def stop(self):
        self.running = False
        self.console.print("[bold magenta][TerminalMonitor][/bold magenta] Visualization stopped.")

    def display(self):
        self.console.clear()
        if not self.hypervisor or not hasattr(self.hypervisor, 'vms') or not self.hypervisor.vms:
            self.console.print(Panel("No hypervisor or VMs available.", title="DNA Visualization", style="red"))
            return

        table = Table(title="DNA Transcription Monitor", show_header=True, header_style="bold blue")
        table.add_column("VM ID", style="cyan", no_wrap=True)
        table.add_column("State", style="green")
        table.add_column("Genome", style="magenta")
        table.add_column("DNA Activity", style="yellow")
        table.add_column("ATP", style="bold")

        for vm_id, vm in self.hypervisor.vms.items():
            state = getattr(vm, 'state', 'UNKNOWN')
            genome = getattr(vm, 'genome_name', 'N/A')
            dna_bar = self._fake_dna_bar()
            atp = self._fake_atp_level()
            table.add_row(str(vm_id), str(state), str(genome), dna_bar, f"{atp}%")

        self.console.print(table)
        self.console.print(Text("Press Ctrl+C to stop visualization.", style="bold white"))

    def _fake_dna_bar(self):
        # Simulate DNA activity with a colored bar
        length = random.randint(20, 60)
        bases = ['A','T','G','C']
        colors = {'A': 'red', 'T': 'green', 'G': 'yellow', 'C': 'blue'}
        bar = Text()
        for _ in range(length):
            base = random.choice(bases)
            bar.append(base, style=colors[base])
        return bar

    def _fake_atp_level(self):
        # Simulate ATP level as a percentage
        return random.randint(50, 100)
