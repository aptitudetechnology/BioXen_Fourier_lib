#!/usr/bin/env python3
"""
BioXen Data Generator for Terminal Visualization
Generates realistic biological hypervisor data for testing
"""

import json
import random
import time
from datetime import datetime
from pathlib import Path


class BioXenDataGenerator:
    """Generate realistic BioXen biological data"""
    
    def __init__(self, num_vms=4):
        self.num_vms = num_vms
        self.vm_states = {}
        
        # Initialize VM states
        for i in range(1, num_vms + 1):
            vm_id = f"vm_{i}"
            self.vm_states[vm_id] = {
                'atp_trend': random.choice(['stable', 'increasing', 'decreasing']),
                'gene_activity_cycle': random.uniform(0, 6.28),  # 2π for sine wave
                'ribosome_base': random.randint(10, 20),
                'last_atp': random.randint(60, 90)
            }
    
    def simulate_dna_transcription(self, vm_state, time_factor):
        """Simulate realistic DNA transcription patterns"""
        # Gene expression follows circadian-like cycles
        cycle_position = (vm_state['gene_activity_cycle'] + time_factor * 0.1) % 6.28
        base_expression = 8 + 6 * abs(math.sin(cycle_position))
        
        # Add some randomness for realism
        noise = random.uniform(-2, 2)
        active_genes = max(1, int(base_expression + noise))
        
        # Gene expression rate correlates with active genes but has independent variation
        expression_rate = min(95, max(20, active_genes * 6 + random.randint(-15, 15)))
        
        vm_state['gene_activity_cycle'] = cycle_position
        return active_genes, expression_rate
    
    def simulate_atp_dynamics(self, vm_state):
        """Simulate ATP level changes based on cellular activity"""
        current_atp = vm_state['last_atp']
        
        if vm_state['atp_trend'] == 'increasing':
            change = random.uniform(0.5, 3.0)
            new_atp = min(95, current_atp + change)
            if new_atp >= 90:
                vm_state['atp_trend'] = random.choice(['stable', 'decreasing'])
        elif vm_state['atp_trend'] == 'decreasing':
            change = random.uniform(0.5, 2.5)
            new_atp = max(40, current_atp - change)
            if new_atp <= 45:
                vm_state['atp_trend'] = random.choice(['stable', 'increasing'])
        else:  # stable
            change = random.uniform(-1.0, 1.0)
            new_atp = max(40, min(95, current_atp + change))
            if random.random() < 0.1:  # 10% chance to change trend
                vm_state['atp_trend'] = random.choice(['increasing', 'decreasing'])
        
        vm_state['last_atp'] = new_atp
        return int(new_atp)
    
    def simulate_ribosome_allocation(self, vm_state, atp_level):
        """Simulate ribosome allocation based on energy availability"""
        base_ribosomes = vm_state['ribosome_base']
        
        # Higher ATP allows for more ribosomes
        atp_factor = atp_level / 100.0
        max_additional = int(15 * atp_factor)
        
        actual_ribosomes = base_ribosomes + random.randint(0, max_additional)
        utilization = min(95, max(30, int(atp_factor * 85 + random.randint(-10, 10))))
        
        return actual_ribosomes, utilization
    
    def simulate_protein_synthesis(self, ribosomes, utilization, active_genes):
        """Simulate protein synthesis based on ribosome activity and gene expression"""
        # Protein count depends on active ribosomes and gene expression
        active_ribosome_count = ribosomes * (utilization / 100.0)
        base_proteins = int(active_ribosome_count * 2.5)
        gene_factor = active_genes / 10.0
        
        proteins = max(5, int(base_proteins * gene_factor + random.randint(-10, 10)))
        
        # mRNA count is related to gene activity
        mrna = max(1, int(active_genes * 0.8 + random.randint(-2, 3)))
        
        return proteins, mrna
    
    def generate_data(self, output_file="bioxen_data.json"):
        """Generate a complete BioXen data snapshot"""
        import math
        
        current_time = time.time()
        
        # System-level data
        total_ribosomes = 80
        allocated_ribosomes = 0
        total_proteins = 0
        total_genes = 0
        
        vms = {}
        
        # Generate data for each VM
        for i in range(1, self.num_vms + 1):
            vm_id = f"vm_{i}"
            vm_state = self.vm_states[vm_id]
            
            # Simulate biological processes
            atp_level = self.simulate_atp_dynamics(vm_state)
            active_genes, expression_rate = self.simulate_dna_transcription(vm_state, current_time)
            ribosomes, utilization = self.simulate_ribosome_allocation(vm_state, atp_level)
            proteins, mrna = self.simulate_protein_synthesis(ribosomes, utilization, active_genes)
            
            allocated_ribosomes += ribosomes
            total_proteins += proteins
            total_genes += active_genes
            
            vms[vm_id] = {
                "vm_id": vm_id,
                "atp_percentage": atp_level,
                "ribosomes": ribosomes,
                "active_genes": active_genes,
                "protein_count": proteins,
                "mrna_count": mrna,
                "gene_expression_rate": expression_rate,
                "ribosome_utilization": utilization
            }
        
        # Calculate system metrics
        available_ribosomes = max(0, total_ribosomes - allocated_ribosomes)
        system_atp = sum(vm['atp_percentage'] for vm in vms.values()) // len(vms)
        
        data = {
            "system": {
                "chassis_type": "E_coli_MG1655",
                "total_ribosomes": total_ribosomes,
                "available_ribosomes": available_ribosomes,
                "timestamp": datetime.now().isoformat(),
                "atp_pool": system_atp,
                "total_active_genes": total_genes,
                "total_proteins": total_proteins
            },
            "vms": vms
        }
        
        # Write to file
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return data
    
    def run_continuous(self, output_file="bioxen_data.json", interval=1.0):
        """Continuously generate data at specified interval"""
        print(f"Starting continuous data generation to {output_file}")
        print(f"Update interval: {interval} seconds")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                data = self.generate_data(output_file)
                print(f"Updated {output_file} - {len(data['vms'])} VMs, "
                      f"ATP: {data['system']['atp_pool']}%, "
                      f"Active genes: {data['system']['total_active_genes']}")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nData generation stopped")


if __name__ == "__main__":
    import argparse
    import math
    
    parser = argparse.ArgumentParser(description="BioXen Data Generator")
    parser.add_argument("--output", default="bioxen_data.json", help="Output file path")
    parser.add_argument("--vms", type=int, default=4, help="Number of VMs to simulate")
    parser.add_argument("--continuous", action="store_true", help="Run continuously")
    parser.add_argument("--interval", type=float, default=1.0, help="Update interval for continuous mode")
    
    args = parser.parse_args()
    
    generator = BioXenDataGenerator(args.vms)
    
    if args.continuous:
        generator.run_continuous(args.output, args.interval)
    else:
        data = generator.generate_data(args.output)
        print(f"Generated data file: {args.output}")
        print(f"VMs: {len(data['vms'])}, System ATP: {data['system']['atp_pool']}%")
