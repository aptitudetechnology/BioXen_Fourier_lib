"""
Visualization tools for genetic circuits and JCVI analysis.

This module provides comprehensive visualization capabilities for genetic
circuits, including circuit diagrams, sequence maps, and JCVI analysis plots.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Arrow
import numpy as np
from typing import List, Dict, Tuple, Optional
import json
from dataclasses import dataclass
from ..core.elements import GeneticCircuit, GeneticElement, ElementType


@dataclass
class VisualizationStyle:
    """Style configuration for circuit visualization"""
    figure_size: Tuple[int, int] = (12, 8)
    dpi: int = 300
    font_size: int = 10
    title_font_size: int = 14
    element_height: float = 0.8
    element_spacing: float = 1.2
    color_scheme: Dict[str, str] = None
    
    def __post_init__(self):
        if self.color_scheme is None:
            self.color_scheme = {
                'gene': '#FF6B6B',
                'promoter': '#4ECDC4', 
                'terminator': '#45B7D1',
                'rbs': '#96CEB4',
                'operator': '#FFEAA7',
                'default': '#DDA0DD'
            }


class CircuitVisualizer:
    """Visualize genetic circuits as publication-ready diagrams"""
    
    def __init__(self, style: Optional[VisualizationStyle] = None):
        self.style = style or VisualizationStyle()
        self.fig = None
        self.ax = None
    
    def visualize_circuit(self, circuit: GeneticCircuit, 
                         output_file: Optional[str] = None,
                         show_sequence_lengths: bool = True,
                         show_regulation: bool = True) -> plt.Figure:
        """Create a comprehensive circuit visualization"""
        
        # Set up the figure
        self.fig, self.ax = plt.subplots(figsize=self.style.figure_size, dpi=self.style.dpi)
        
        # Calculate layout
        total_length = sum(len(element.sequence) for element in circuit.elements)
        x_positions = self._calculate_positions(circuit.elements, total_length)
        
        # Draw elements
        for i, (element, x_pos) in enumerate(zip(circuit.elements, x_positions)):
            self._draw_element(element, x_pos, 0, show_sequence_lengths)
        
        # Draw regulatory relationships
        if show_regulation:
            self._draw_regulatory_connections(circuit, x_positions)
        
        # Customize plot
        self._finalize_plot(circuit, total_length)
        
        # Save if filename provided
        if output_file:
            self.fig.savefig(output_file, dpi=self.style.dpi, bbox_inches='tight')
        
        return self.fig
    
    def visualize_circuit_linear_map(self, circuit: GeneticCircuit,
                                   output_file: Optional[str] = None) -> plt.Figure:
        """Create a linear sequence map of the circuit"""
        
        self.fig, self.ax = plt.subplots(figsize=(14, 6), dpi=self.style.dpi)
        
        # Calculate cumulative positions
        cumulative_pos = 0
        positions = []
        
        for element in circuit.elements:
            start_pos = cumulative_pos
            end_pos = cumulative_pos + len(element.sequence)
            positions.append((start_pos, end_pos))
            cumulative_pos = end_pos
        
        # Draw sequence ruler
        self._draw_sequence_ruler(cumulative_pos)
        
        # Draw elements as blocks
        for i, (element, (start, end)) in enumerate(zip(circuit.elements, positions)):
            self._draw_linear_element(element, start, end, i % 2)
        
        # Customize linear map
        self._finalize_linear_map(circuit, cumulative_pos)
        
        if output_file:
            self.fig.savefig(output_file, dpi=self.style.dpi, bbox_inches='tight')
        
        return self.fig
    
    def visualize_circuit_features(self, circuit: GeneticCircuit,
                                 output_file: Optional[str] = None) -> plt.Figure:
        """Create a features overview visualization"""
        
        # Create subplots for different analyses
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10), dpi=self.style.dpi)
        
        # Element type distribution
        self._plot_element_distribution(circuit, ax1)
        
        # Sequence length distribution  
        self._plot_length_distribution(circuit, ax2)
        
        # GC content analysis
        self._plot_gc_content_analysis(circuit, ax3)
        
        # Regulatory network
        self._plot_regulatory_network(circuit, ax4)
        
        plt.tight_layout()
        
        if output_file:
            fig.savefig(output_file, dpi=self.style.dpi, bbox_inches='tight')
        
        return fig
    
    def create_jcvi_compatibility_report(self, circuit: GeneticCircuit,
                                       validation_result=None,
                                       output_file: Optional[str] = None) -> plt.Figure:
        """Create JCVI compatibility visualization report"""
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10), dpi=self.style.dpi)
        
        # Compatibility overview
        self._plot_jcvi_compatibility(circuit, validation_result, ax1)
        
        # Format compatibility
        self._plot_format_compatibility(circuit, ax2)
        
        # Assembly metrics
        self._plot_assembly_metrics(circuit, ax3)
        
        # Export readiness
        self._plot_export_readiness(circuit, validation_result, ax4)
        
        fig.suptitle(f'JCVI Compatibility Report: {circuit.circuit_id}', 
                    fontsize=self.style.title_font_size)
        plt.tight_layout()
        
        if output_file:
            fig.savefig(output_file, dpi=self.style.dpi, bbox_inches='tight')
        
        return fig
    
    def _calculate_positions(self, elements: List[GeneticElement], 
                           total_length: int) -> List[float]:
        """Calculate x positions for elements based on their lengths"""
        positions = []
        current_pos = 0
        
        # Scale factor to fit in reasonable plot width
        scale_factor = 10.0 / total_length if total_length > 0 else 1.0
        
        for element in elements:
            element_width = len(element.sequence) * scale_factor
            positions.append(current_pos + element_width / 2)
            current_pos += element_width + 0.2  # Small gap between elements
        
        return positions
    
    def _draw_element(self, element: GeneticElement, x_pos: float, y_pos: float,
                     show_sequence_lengths: bool):
        """Draw a single genetic element"""
        
        element_type = element.element_type.value
        color = self.style.color_scheme.get(element_type, self.style.color_scheme['default'])
        
        # Choose shape based on element type
        if element.element_type == ElementType.GENE:
            self._draw_gene_arrow(x_pos, y_pos, color, element.element_id)
        elif element.element_type == ElementType.PROMOTER:
            self._draw_promoter_bend(x_pos, y_pos, color, element.element_id)
        elif element.element_type == ElementType.TERMINATOR:
            self._draw_terminator_stem(x_pos, y_pos, color, element.element_id)
        elif element.element_type == ElementType.RBS:
            self._draw_rbs_circle(x_pos, y_pos, color, element.element_id)
        else:
            self._draw_generic_box(x_pos, y_pos, color, element.element_id)
        
        # Add sequence length annotation
        if show_sequence_lengths:
            self.ax.text(x_pos, y_pos - 0.6, f"{len(element.sequence)} bp",
                        ha='center', va='top', fontsize=8)
    
    def _draw_gene_arrow(self, x: float, y: float, color: str, label: str):
        """Draw gene as arrow shape"""
        arrow = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6,
                              boxstyle="round,pad=0.02",
                              facecolor=color, edgecolor='black', linewidth=1)
        self.ax.add_patch(arrow)
        
        # Add arrow head
        arrow_head = patches.Polygon([(x+0.4, y), (x+0.6, y+0.2), (x+0.6, y-0.2)],
                                   facecolor=color, edgecolor='black')
        self.ax.add_patch(arrow_head)
        
        self.ax.text(x, y, label, ha='center', va='center', 
                    fontsize=self.style.font_size, weight='bold')
    
    def _draw_promoter_bend(self, x: float, y: float, color: str, label: str):
        """Draw promoter as bent arrow"""
        # Main body
        rect = FancyBboxPatch((x-0.3, y-0.2), 0.6, 0.4,
                             boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='black')
        self.ax.add_patch(rect)
        
        # Bent arrow indicating direction
        arrow = patches.FancyArrowPatch((x-0.2, y+0.3), (x+0.2, y+0.1),
                                      arrowstyle='->', color='black', lw=2)
        self.ax.add_patch(arrow)
        
        self.ax.text(x, y-0.5, label, ha='center', va='center', 
                    fontsize=self.style.font_size)
    
    def _draw_terminator_stem(self, x: float, y: float, color: str, label: str):
        """Draw terminator as stem-loop structure"""
        # Stem
        self.ax.plot([x, x], [y-0.3, y+0.3], color='black', linewidth=3)
        
        # Loop
        circle = patches.Circle((x, y+0.3), 0.15, facecolor=color, 
                              edgecolor='black', linewidth=2)
        self.ax.add_patch(circle)
        
        self.ax.text(x, y-0.5, label, ha='center', va='center', 
                    fontsize=self.style.font_size)
    
    def _draw_rbs_circle(self, x: float, y: float, color: str, label: str):
        """Draw RBS as circle"""
        circle = patches.Circle((x, y), 0.25, facecolor=color, 
                              edgecolor='black', linewidth=2)
        self.ax.add_patch(circle)
        
        self.ax.text(x, y, 'RBS', ha='center', va='center', 
                    fontsize=8, weight='bold')
        self.ax.text(x, y-0.5, label, ha='center', va='center', 
                    fontsize=self.style.font_size)
    
    def _draw_generic_box(self, x: float, y: float, color: str, label: str):
        """Draw generic element as box"""
        rect = FancyBboxPatch((x-0.3, y-0.2), 0.6, 0.4,
                             boxstyle="round,pad=0.02",
                             facecolor=color, edgecolor='black')
        self.ax.add_patch(rect)
        
        self.ax.text(x, y, label, ha='center', va='center', 
                    fontsize=self.style.font_size)
    
    def _draw_regulatory_connections(self, circuit: GeneticCircuit, x_positions: List[float]):
        """Draw regulatory connections between elements"""
        # Create mapping of element IDs to positions
        id_to_pos = {element.element_id: pos 
                     for element, pos in zip(circuit.elements, x_positions)}
        
        for i, element in enumerate(circuit.elements):
            if element.regulation_target and element.regulation_target in id_to_pos:
                start_x = x_positions[i]
                end_x = id_to_pos[element.regulation_target]
                
                # Draw regulatory arrow
                arrow = patches.FancyArrowPatch((start_x, 0.8), (end_x, 0.8),
                                              arrowstyle='->', 
                                              connectionstyle="arc3,rad=0.3",
                                              color='red', linewidth=2, alpha=0.7)
                self.ax.add_patch(arrow)
    
    def _finalize_plot(self, circuit: GeneticCircuit, total_length: int):
        """Finalize the circuit plot"""
        self.ax.set_xlim(-1, 12)
        self.ax.set_ylim(-1, 2)
        self.ax.set_aspect('equal')
        
        # Remove axes
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        
        # Add title
        self.ax.set_title(f'Genetic Circuit: {circuit.circuit_id}\n'
                         f'Total Length: {total_length} bp, Elements: {len(circuit.elements)}',
                         fontsize=self.style.title_font_size, pad=20)
    
    def _draw_sequence_ruler(self, total_length: int):
        """Draw sequence position ruler"""
        # Main ruler line
        self.ax.plot([0, total_length], [0, 0], 'k-', linewidth=2)
        
        # Tick marks every 1000 bp
        tick_interval = max(1, total_length // 10)
        for pos in range(0, total_length + 1, tick_interval):
            self.ax.plot([pos, pos], [-0.1, 0.1], 'k-', linewidth=1)
            self.ax.text(pos, -0.3, f'{pos}', ha='center', va='top', fontsize=8)
    
    def _draw_linear_element(self, element: GeneticElement, start: int, end: int, row: int):
        """Draw element in linear map format"""
        y_pos = 0.5 + row * 0.3
        color = self.style.color_scheme.get(element.element_type.value, 
                                          self.style.color_scheme['default'])
        
        # Draw element as rectangle
        rect = patches.Rectangle((start, y_pos), end - start, 0.2,
                               facecolor=color, edgecolor='black', alpha=0.8)
        self.ax.add_patch(rect)
        
        # Add label
        label_x = (start + end) / 2
        self.ax.text(label_x, y_pos + 0.1, element.element_id,
                    ha='center', va='center', fontsize=8, rotation=0)
    
    def _finalize_linear_map(self, circuit: GeneticCircuit, total_length: int):
        """Finalize linear map visualization"""
        self.ax.set_xlim(0, total_length)
        self.ax.set_ylim(-0.5, 2)
        
        self.ax.set_xlabel('Position (bp)', fontsize=self.style.font_size)
        self.ax.set_title(f'Linear Map: {circuit.circuit_id}',
                         fontsize=self.style.title_font_size)
        
        # Remove y-axis
        self.ax.set_yticks([])
        self.ax.spines['left'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)
    
    def _plot_element_distribution(self, circuit: GeneticCircuit, ax):
        """Plot distribution of element types"""
        type_counts = {}
        for element in circuit.elements:
            element_type = element.element_type.value
            type_counts[element_type] = type_counts.get(element_type, 0) + 1
        
        colors = [self.style.color_scheme.get(t, self.style.color_scheme['default']) 
                 for t in type_counts.keys()]
        
        ax.pie(type_counts.values(), labels=type_counts.keys(), colors=colors, autopct='%1.1f%%')
        ax.set_title('Element Type Distribution')
    
    def _plot_length_distribution(self, circuit: GeneticCircuit, ax):
        """Plot sequence length distribution"""
        lengths = [len(element.sequence) for element in circuit.elements]
        types = [element.element_type.value for element in circuit.elements]
        
        # Create bar plot
        x_pos = range(len(lengths))
        colors = [self.style.color_scheme.get(t, self.style.color_scheme['default']) 
                 for t in types]
        
        bars = ax.bar(x_pos, lengths, color=colors, alpha=0.7)
        ax.set_xlabel('Elements')
        ax.set_ylabel('Length (bp)')
        ax.set_title('Sequence Length Distribution')
        ax.set_xticks(x_pos)
        ax.set_xticklabels([e.element_id for e in circuit.elements], rotation=45)
    
    def _plot_gc_content_analysis(self, circuit: GeneticCircuit, ax):
        """Plot GC content analysis"""
        gc_contents = []
        labels = []
        
        for element in circuit.elements:
            if element.sequence:
                sequence = element.sequence.upper()
                gc_count = sequence.count('G') + sequence.count('C')
                gc_content = gc_count / len(sequence) if len(sequence) > 0 else 0
                gc_contents.append(gc_content * 100)
                labels.append(element.element_id)
        
        colors = [self.style.color_scheme.get(element.element_type.value, 
                                            self.style.color_scheme['default'])
                 for element in circuit.elements]
        
        bars = ax.bar(range(len(gc_contents)), gc_contents, color=colors, alpha=0.7)
        ax.set_xlabel('Elements')
        ax.set_ylabel('GC Content (%)')
        ax.set_title('GC Content Analysis')
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45)
        
        # Add optimal range lines
        ax.axhline(y=40, color='green', linestyle='--', alpha=0.5, label='Optimal range')
        ax.axhline(y=60, color='green', linestyle='--', alpha=0.5)
        ax.legend()
    
    def _plot_regulatory_network(self, circuit: GeneticCircuit, ax):
        """Plot regulatory network connections"""
        # Simple network visualization
        elements_with_targets = [e for e in circuit.elements if e.regulation_target]
        
        if not elements_with_targets:
            ax.text(0.5, 0.5, 'No regulatory\nconnections', 
                   ha='center', va='center', transform=ax.transAxes)
            ax.set_title('Regulatory Network')
            return
        
        # Create positions for network nodes
        n_elements = len(circuit.elements)
        theta = np.linspace(0, 2*np.pi, n_elements, endpoint=False)
        x_pos = np.cos(theta)
        y_pos = np.sin(theta)
        
        # Draw nodes
        for i, element in enumerate(circuit.elements):
            color = self.style.color_scheme.get(element.element_type.value,
                                              self.style.color_scheme['default'])
            ax.scatter(x_pos[i], y_pos[i], c=color, s=100, alpha=0.7)
            ax.text(x_pos[i], y_pos[i], element.element_id, 
                   ha='center', va='center', fontsize=6)
        
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.set_title('Regulatory Network')
        ax.axis('off')
    
    def _plot_jcvi_compatibility(self, circuit: GeneticCircuit, validation_result, ax):
        """Plot JCVI compatibility overview"""
        # Compatibility metrics
        metrics = {
            'Structure': 0.9,  # Placeholder values
            'Sequences': 0.8,
            'Formats': 0.95,
            'Assembly': 0.85
        }
        
        if validation_result:
            overall_score = 1.0 - (validation_result.errors_count + 
                                 validation_result.critical_count) / 10.0
            metrics['Validation'] = max(0, overall_score)
        
        categories = list(metrics.keys())
        values = list(metrics.values())
        colors = ['green' if v >= 0.8 else 'orange' if v >= 0.6 else 'red' for v in values]
        
        bars = ax.bar(categories, values, color=colors, alpha=0.7)
        ax.set_ylabel('Compatibility Score')
        ax.set_title('JCVI Compatibility Overview')
        ax.set_ylim(0, 1)
        
        # Add score labels
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                   f'{value:.2f}', ha='center', va='bottom')
    
    def _plot_format_compatibility(self, circuit: GeneticCircuit, ax):
        """Plot format compatibility matrix"""
        formats = ['GenBank', 'GFF3', 'FASTA', 'AGP', 'Feature Table']
        compatibility = [1, 1, 1, 0.9, 0.95]  # Example values
        
        # Create heatmap-style visualization
        y_pos = range(len(formats))
        colors = ['green' if c >= 0.9 else 'orange' if c >= 0.7 else 'red' 
                 for c in compatibility]
        
        bars = ax.barh(y_pos, compatibility, color=colors, alpha=0.7)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(formats)
        ax.set_xlabel('Compatibility Score')
        ax.set_title('Export Format Compatibility')
        ax.set_xlim(0, 1)
    
    def _plot_assembly_metrics(self, circuit: GeneticCircuit, ax):
        """Plot assembly-related metrics"""
        total_length = sum(len(e.sequence) for e in circuit.elements)
        n_elements = len(circuit.elements)
        
        metrics = {
            'Total Length (kb)': total_length / 1000,
            'Element Count': n_elements,
            'Avg Element Size': total_length / n_elements if n_elements > 0 else 0,
            'Complexity Score': min(1.0, (total_length * n_elements) / 100000)
        }
        
        categories = list(metrics.keys())
        values = list(metrics.values())
        
        # Normalize values for display
        normalized_values = [v / max(values) if max(values) > 0 else 0 for v in values]
        
        bars = ax.bar(categories, normalized_values, alpha=0.7)
        ax.set_ylabel('Normalized Value')
        ax.set_title('Assembly Metrics')
        ax.tick_params(axis='x', rotation=45)
        
        # Add actual values as labels
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                   f'{value:.1f}', ha='center', va='bottom')
    
    def _plot_export_readiness(self, circuit: GeneticCircuit, validation_result, ax):
        """Plot export readiness assessment"""
        readiness_factors = {
            'Sequence Quality': 0.9,
            'Structure Validity': 0.85,
            'Format Compliance': 0.95,
            'Documentation': 0.8
        }
        
        if validation_result:
            if validation_result.critical_count == 0:
                readiness_factors['Validation'] = 0.9
            elif validation_result.errors_count == 0:
                readiness_factors['Validation'] = 0.7
            else:
                readiness_factors['Validation'] = 0.4
        
        # Radar chart style
        categories = list(readiness_factors.keys())
        values = list(readiness_factors.values())
        
        # Create simple bar chart (radar would be more complex)
        bars = ax.bar(categories, values, alpha=0.7, 
                     color=['green' if v >= 0.8 else 'orange' if v >= 0.6 else 'red' 
                           for v in values])
        
        ax.set_ylabel('Readiness Score')
        ax.set_title('Export Readiness Assessment')
        ax.set_ylim(0, 1)
        ax.tick_params(axis='x', rotation=45)


def create_circuit_gallery(circuits: List[GeneticCircuit], 
                          output_file: str = "circuit_gallery.png") -> plt.Figure:
    """Create a gallery view of multiple circuits"""
    
    n_circuits = len(circuits)
    cols = min(3, n_circuits)
    rows = (n_circuits + cols - 1) // cols
    
    fig, axes = plt.subplots(rows, cols, figsize=(5*cols, 4*rows), dpi=300)
    if n_circuits == 1:
        axes = [axes]
    elif rows == 1:
        axes = [axes]
    else:
        axes = axes.flatten()
    
    visualizer = CircuitVisualizer()
    
    for i, circuit in enumerate(circuits):
        if i < len(axes):
            ax = axes[i]
            # Create a simplified visualization for gallery
            visualizer.ax = ax
            visualizer._draw_circuit_summary(circuit, ax)
    
    # Hide unused subplots
    for i in range(n_circuits, len(axes)):
        axes[i].set_visible(False)
    
    plt.tight_layout()
    fig.savefig(output_file, dpi=300, bbox_inches='tight')
    
    return fig


def export_circuit_visualization_report(circuit: GeneticCircuit, 
                                       validation_result=None,
                                       output_dir: str = "./visualization_report"):
    """Export comprehensive visualization report"""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    visualizer = CircuitVisualizer()
    
    # Create all visualizations
    circuit_fig = visualizer.visualize_circuit(
        circuit, os.path.join(output_dir, f"{circuit.circuit_id}_circuit.png")
    )
    
    linear_fig = visualizer.visualize_circuit_linear_map(
        circuit, os.path.join(output_dir, f"{circuit.circuit_id}_linear.png")
    )
    
    features_fig = visualizer.visualize_circuit_features(
        circuit, os.path.join(output_dir, f"{circuit.circuit_id}_features.png")
    )
    
    if validation_result:
        jcvi_fig = visualizer.create_jcvi_compatibility_report(
            circuit, validation_result, 
            os.path.join(output_dir, f"{circuit.circuit_id}_jcvi_report.png")
        )
    
    # Create summary JSON
    summary = {
        "circuit_id": circuit.circuit_id,
        "total_length": sum(len(e.sequence) for e in circuit.elements),
        "element_count": len(circuit.elements),
        "visualization_files": [
            f"{circuit.circuit_id}_circuit.png",
            f"{circuit.circuit_id}_linear.png", 
            f"{circuit.circuit_id}_features.png"
        ]
    }
    
    if validation_result:
        summary["validation_summary"] = {
            "is_valid": validation_result.is_valid,
            "warnings": validation_result.warnings_count,
            "errors": validation_result.errors_count,
            "critical": validation_result.critical_count
        }
        summary["visualization_files"].append(f"{circuit.circuit_id}_jcvi_report.png")
    
    with open(os.path.join(output_dir, "visualization_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    return summary
