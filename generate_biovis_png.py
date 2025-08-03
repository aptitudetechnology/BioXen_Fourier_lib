#!/usr/bin/env python3
"""
BioXen Visualization PNG Generator
Generates comprehensive biological system diagrams as PNG files for headless systems
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import json
import os
from datetime import datetime

def create_comprehensive_biovis():
    """Create a comprehensive biological visualization similar to Love2D but as static PNG"""
    
    # Create figure with subplots
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('BioXen Biological Hypervisor - Real-time System State', fontsize=16, fontweight='bold')
    
    # Create grid layout
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. System Overview (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    create_system_overview(ax1)
    
    # 2. VM Cells Grid (top center and right)
    ax2 = fig.add_subplot(gs[0, 1:])
    create_vm_cells_grid(ax2)
    
    # 3. ATP Flow System (middle left)
    ax3 = fig.add_subplot(gs[1, 0])
    create_atp_flow_system(ax3)
    
    # 4. Genetic Circuits (middle center and right)
    ax4 = fig.add_subplot(gs[1, 1:])
    create_genetic_circuits(ax4)
    
    # 5. Resource Monitor (bottom left)
    ax5 = fig.add_subplot(gs[2, 0])
    create_resource_monitor(ax5)
    
    # 6. Performance Metrics (bottom center and right)
    ax6 = fig.add_subplot(gs[2, 1:])
    create_performance_metrics(ax6)
    
    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bioxen_biovis_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Biological visualization saved as: {filename}")
    
    return filename

def create_system_overview(ax):
    """Create system overview panel"""
    ax.set_title("System Overview", fontweight='bold')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Chassis representation
    chassis = patches.Rectangle((1, 7), 8, 2, linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.7)
    ax.add_patch(chassis)
    ax.text(5, 8, 'E. coli Chassis', ha='center', va='center', fontweight='bold')
    
    # Hypervisor layer
    hypervisor = patches.Rectangle((1, 5), 8, 1.5, linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.7)
    ax.add_patch(hypervisor)
    ax.text(5, 5.75, 'BioXen Hypervisor', ha='center', va='center', fontweight='bold')
    
    # VM instances
    vm_colors = ['orange', 'purple', 'red']
    vm_names = ['VM-SYN3A', 'VM-CIRCUIT', 'VM-SENSOR']
    for i, (color, name) in enumerate(zip(vm_colors, vm_names)):
        vm = patches.Rectangle((1 + i*2.5, 2), 2, 2.5, linewidth=2, edgecolor=color, facecolor=color, alpha=0.3)
        ax.add_patch(vm)
        ax.text(2 + i*2.5, 3.25, name, ha='center', va='center', fontsize=8, fontweight='bold')
    
    # System stats
    ax.text(1, 1, f"Active VMs: 3\nRibosomes: 245/1000\nStatus: Running", fontsize=9, verticalalignment='top')
    
    ax.set_xticks([])
    ax.set_yticks([])

def create_vm_cells_grid(ax):
    """Create VM cells visualization"""
    ax.set_title("Virtual Machine Cells", fontweight='bold')
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    
    # VM cell data
    vms = [
        {"name": "SYN3A", "pos": (1, 5), "size": 3, "color": "orange", "activity": 0.8},
        {"name": "CIRCUIT", "pos": (5, 5), "size": 3, "color": "purple", "activity": 0.6},
        {"name": "SENSOR", "pos": (9, 5), "size": 3, "color": "red", "activity": 0.9},
        {"name": "FACTORY", "pos": (3, 1), "size": 3, "color": "blue", "activity": 0.4}
    ]
    
    for vm in vms:
        x, y = vm["pos"]
        size = vm["size"]
        
        # Cell membrane
        cell = patches.Circle((x + size/2, y + size/2), size/2, 
                             linewidth=2, edgecolor=vm["color"], facecolor=vm["color"], alpha=0.3)
        ax.add_patch(cell)
        
        # Nucleus
        nucleus = patches.Circle((x + size/2, y + size/2), size/4, 
                               linewidth=1, edgecolor='black', facecolor='yellow', alpha=0.6)
        ax.add_patch(nucleus)
        
        # Activity indicator
        activity_height = vm["activity"] * 2
        activity_bar = patches.Rectangle((x + size + 0.2, y + size/2 - 1), 0.3, activity_height,
                                       facecolor=vm["color"], alpha=0.8)
        ax.add_patch(activity_bar)
        
        # Labels
        ax.text(x + size/2, y - 0.3, vm["name"], ha='center', fontweight='bold', fontsize=10)
        ax.text(x + size + 0.8, y + size/2, f"{vm['activity']*100:.0f}%", va='center', fontsize=8)
    
    ax.set_xticks([])
    ax.set_yticks([])

def create_atp_flow_system(ax):
    """Create ATP flow visualization"""
    ax.set_title("ATP Flow System", fontweight='bold')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    
    # Mitochondria (ATP sources)
    for i in range(3):
        x, y = 2, 8 - i*2.5
        mito = patches.Ellipse((x, y), 1.5, 0.8, linewidth=2, edgecolor='darkgreen', facecolor='lightgreen')
        ax.add_patch(mito)
        ax.text(x, y, 'ATP', ha='center', va='center', fontweight='bold', fontsize=8)
    
    # ATP flow arrows
    arrow_props = dict(arrowstyle='->', lw=2, color='red')
    for i in range(3):
        y = 8 - i*2.5
        ax.annotate('', xy=(6, y), xytext=(3, y), arrowprops=arrow_props)
        
        # Flow particles
        for j in range(3):
            particle_x = 3.5 + j*0.8
            particle = patches.Circle((particle_x, y), 0.1, facecolor='red', alpha=0.8)
            ax.add_patch(particle)
    
    # ATP consumers (VMs)
    consumers = [(7, 8), (7, 5.5), (7, 3)]
    for i, (x, y) in enumerate(consumers):
        consumer = patches.Rectangle((x, y-0.4), 1.5, 0.8, linewidth=2, edgecolor='blue', facecolor='lightblue')
        ax.add_patch(consumer)
        ax.text(x+0.75, y, f'VM{i+1}', ha='center', va='center', fontweight='bold', fontsize=8)
    
    # Energy levels
    ax.text(1, 1, "Energy Status:\n• Production: High\n• Consumption: Normal\n• Efficiency: 87%", 
            fontsize=9, verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.5))
    
    ax.set_xticks([])
    ax.set_yticks([])

def create_genetic_circuits(ax):
    """Create genetic circuits visualization"""
    ax.set_title("Genetic Circuits", fontweight='bold')
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 8)
    
    # Circuit types
    circuits = [
        {"name": "NOT Gate", "pos": (1, 6), "inputs": 1, "outputs": 1, "active": True},
        {"name": "AND Gate", "pos": (5, 6), "inputs": 2, "outputs": 1, "active": False},
        {"name": "OR Gate", "pos": (9, 6), "inputs": 2, "outputs": 1, "active": True},
        {"name": "Oscillator", "pos": (1, 3), "inputs": 0, "outputs": 1, "active": True},
        {"name": "Amplifier", "pos": (5, 3), "inputs": 1, "outputs": 2, "active": True},
        {"name": "Memory", "pos": (9, 3), "inputs": 1, "outputs": 1, "active": False}
    ]
    
    for circuit in circuits:
        x, y = circuit["pos"]
        color = 'green' if circuit["active"] else 'gray'
        alpha = 0.8 if circuit["active"] else 0.3
        
        # Circuit box
        box = patches.Rectangle((x, y), 3, 1.5, linewidth=2, edgecolor=color, facecolor=color, alpha=alpha)
        ax.add_patch(box)
        
        # Circuit name
        ax.text(x + 1.5, y + 0.75, circuit["name"], ha='center', va='center', 
                fontweight='bold', fontsize=9, color='white' if circuit["active"] else 'black')
        
        # Input/output indicators
        for i in range(circuit["inputs"]):
            input_y = y + 0.3 + i*0.9
            ax.plot([x-0.2, x], [input_y, input_y], 'k-', linewidth=2)
            ax.plot(x-0.3, input_y, 'ko', markersize=4)
        
        for i in range(circuit["outputs"]):
            output_y = y + 0.3 + i*0.9
            ax.plot([x+3, x+3.2], [output_y, output_y], 'k-', linewidth=2)
            ax.plot(x+3.3, output_y, 'ko', markersize=4)
    
    # Signal flow lines
    ax.plot([4, 5], [6.75, 6.75], 'b-', linewidth=2, alpha=0.7)
    ax.plot([8, 9], [6.75, 6.75], 'b-', linewidth=2, alpha=0.7)
    ax.plot([4, 5], [3.75, 3.75], 'r-', linewidth=2, alpha=0.7)
    
    ax.set_xticks([])
    ax.set_yticks([])

def create_resource_monitor(ax):
    """Create resource monitoring visualization"""
    ax.set_title("Resource Monitor", fontweight='bold')
    
    # Resource usage data
    resources = {
        'Ribosomes': {'used': 245, 'total': 1000, 'color': 'blue'},
        'tRNA': {'used': 450, 'total': 500, 'color': 'green'},
        'ATP': {'used': 780, 'total': 1000, 'color': 'red'},
        'Amino Acids': {'used': 320, 'total': 400, 'color': 'orange'}
    }
    
    y_pos = np.arange(len(resources))
    names = list(resources.keys())
    used_values = [resources[name]['used'] for name in names]
    total_values = [resources[name]['total'] for name in names]
    percentages = [used/total*100 for used, total in zip(used_values, total_values)]
    colors = [resources[name]['color'] for name in names]
    
    # Horizontal bar chart
    bars = ax.barh(y_pos, percentages, color=colors, alpha=0.7)
    
    # Add percentage labels
    for i, (bar, percentage, used, total) in enumerate(zip(bars, percentages, used_values, total_values)):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, 
                f'{percentage:.1f}% ({used}/{total})', 
                va='center', fontsize=9)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names)
    ax.set_xlabel('Resource Utilization (%)')
    ax.set_xlim(0, 120)
    
    # Add warning line at 90%
    ax.axvline(x=90, color='red', linestyle='--', alpha=0.5)
    ax.text(92, len(resources)-0.5, 'Warning\nThreshold', fontsize=8, color='red')

def create_performance_metrics(ax):
    """Create performance metrics visualization"""
    ax.set_title("Performance Metrics", fontweight='bold')
    
    # Time series data simulation
    time_points = np.linspace(0, 60, 100)  # 60 seconds
    
    # Simulated metrics
    protein_synthesis = 50 + 20 * np.sin(0.1 * time_points) + 5 * np.random.randn(100)
    energy_efficiency = 85 + 10 * np.sin(0.05 * time_points) + 2 * np.random.randn(100)
    vm_activity = 70 + 15 * np.sin(0.08 * time_points) + 3 * np.random.randn(100)
    
    # Plot metrics
    ax.plot(time_points, protein_synthesis, 'b-', label='Protein Synthesis Rate', linewidth=2)
    ax.plot(time_points, energy_efficiency, 'g-', label='Energy Efficiency', linewidth=2)
    ax.plot(time_points, vm_activity, 'r-', label='VM Activity Level', linewidth=2)
    
    ax.set_xlabel('Time (seconds)')
    ax.set_ylabel('Performance (%)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 60)
    ax.set_ylim(0, 100)
    
    # Current values annotation
    current_values = f"Current Values:\n• Protein: {protein_synthesis[-1]:.1f}%\n• Energy: {energy_efficiency[-1]:.1f}%\n• Activity: {vm_activity[-1]:.1f}%"
    ax.text(0.02, 0.98, current_values, transform=ax.transAxes, 
            verticalalignment='top', bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.8))

if __name__ == "__main__":
    print("🎨 Generating BioXen biological visualization...")
    filename = create_comprehensive_biovis()
    print(f"📁 File saved in: {os.path.abspath(filename)}")
    print("📋 You can copy this file via SSH using: scp user@host:/path/to/file .")
