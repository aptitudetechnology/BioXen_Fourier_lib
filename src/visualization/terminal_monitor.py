import sys
import time

class TerminalMonitor:
    def __init__(self, hypervisor):
        self.hypervisor = hypervisor
        self.running = False

    def start(self):
        self.running = True
        print("[TerminalMonitor] Visualization started. Press Ctrl+C to stop.")
        try:
            while self.running:
                self.display()
                time.sleep(1)
        except KeyboardInterrupt:
            print("[TerminalMonitor] Visualization stopped by user.")
            self.stop()

    def stop(self):
        self.running = False
        print("[TerminalMonitor] Visualization stopped.")

    def display(self):
        # Example: print VM states and a fake DNA activity bar
        if not self.hypervisor or not hasattr(self.hypervisor, 'vms'):
            print("No hypervisor or VMs available.")
            return
        print("\n=== DNA Visualization ===")
        for vm_id, vm in self.hypervisor.vms.items():
            state = getattr(vm, 'state', 'UNKNOWN')
            genome = getattr(vm, 'genome_name', 'N/A')
            print(f"VM: {vm_id} | State: {state} | Genome: {genome}")
            print("DNA: " + self._fake_dna_bar())
        print("========================\n")

    def _fake_dna_bar(self):
        # Simulate DNA activity with a random bar
        import random
        length = random.randint(20, 60)
        return ''.join(random.choice(['A','T','G','C']) for _ in range(length))
