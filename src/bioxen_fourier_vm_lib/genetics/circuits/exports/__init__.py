"""
Exports module for genetic circuits.

This module provides export functionality to JCVI-compatible formats
and comprehensive visualization tools for circuit analysis.
"""

from .jcvi_format import (
    JCVIFormatExporter,
    JCVIFeature,
    JCVIAnnotation,
    JCVIGenomeRecord,
    export_multiple_circuits_to_jcvi,
    create_jcvi_assembly_script
)

# Visualization imports with fallback for missing matplotlib
try:
    from .visualization import (
        CircuitVisualizer,
        VisualizationStyle,
        create_circuit_gallery,
        export_circuit_visualization_report
    )
    HAS_VISUALIZATION = True
except ImportError:
    # Matplotlib not available
    HAS_VISUALIZATION = False
    CircuitVisualizer = None
    VisualizationStyle = None
    create_circuit_gallery = None
    export_circuit_visualization_report = None

__all__ = [
    # JCVI Format Export
    "JCVIFormatExporter",
    "JCVIFeature", 
    "JCVIAnnotation",
    "JCVIGenomeRecord",
    "export_multiple_circuits_to_jcvi",
    "create_jcvi_assembly_script",
    
    # Visualization (if available)
    "CircuitVisualizer",
    "VisualizationStyle", 
    "create_circuit_gallery",
    "export_circuit_visualization_report",
    "HAS_VISUALIZATION"
]


def export_circuit_complete(circuit, output_dir="./export", 
                          include_visualization=True, include_jcvi=True):
    """
    Complete export function for genetic circuits.
    
    Args:
        circuit: GeneticCircuit to export
        output_dir: Directory for output files
        include_visualization: Whether to create visualizations
        include_jcvi: Whether to create JCVI-compatible files
        
    Returns:
        dict: Summary of exported files
    """
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    exported_files = {}
    
    # JCVI Export
    if include_jcvi:
        exporter = JCVIFormatExporter()
        
        # Export JCVI assembly files
        jcvi_files = exporter.export_for_jcvi_assembly(circuit, output_dir)
        exported_files.update(jcvi_files)
        
        # Export individual formats
        genbank_file = os.path.join(output_dir, f"{circuit.circuit_id}.gb")
        gff3_file = os.path.join(output_dir, f"{circuit.circuit_id}.gff3")
        json_file = os.path.join(output_dir, f"{circuit.circuit_id}.json")
        
        exporter.export_circuit_to_genbank(circuit, genbank_file)
        exporter.export_circuit_to_gff3(circuit, gff3_file)
        exporter.export_circuit_to_jcvi_json(circuit, json_file)
        
        exported_files.update({
            "genbank": genbank_file,
            "gff3": gff3_file,
            "json": json_file
        })
        
        # Create assembly script
        script_file = os.path.join(output_dir, "assemble.sh")
        create_jcvi_assembly_script(circuit, script_file)
        exported_files["assembly_script"] = script_file
    
    # Visualization Export
    if include_visualization and HAS_VISUALIZATION:
        viz_dir = os.path.join(output_dir, "visualizations")
        viz_summary = export_circuit_visualization_report(circuit, None, viz_dir)
        exported_files["visualizations"] = viz_summary
    elif include_visualization and not HAS_VISUALIZATION:
        print("Warning: Visualization requested but matplotlib not available")
    
    return exported_files


def get_export_formats():
    """Get list of available export formats"""
    formats = {
        "jcvi": {
            "genbank": "GenBank format for JCVI tools",
            "gff3": "GFF3 format for annotation",
            "fasta": "FASTA sequence format",
            "feature_table": "NCBI feature table format",
            "agp": "Assembly AGP format",
            "json": "JCVI JSON format"
        }
    }
    
    if HAS_VISUALIZATION:
        formats["visualization"] = {
            "circuit_diagram": "Publication-ready circuit diagram",
            "linear_map": "Linear sequence map",
            "features_analysis": "Features overview plots",
            "jcvi_compatibility": "JCVI compatibility report"
        }
    
    return formats


def validate_export_requirements(circuit):
    """
    Validate that circuit meets export requirements.
    
    Args:
        circuit: GeneticCircuit to validate
        
    Returns:
        dict: Validation results with recommendations
    """
    requirements = {
        "has_elements": len(circuit.elements) > 0,
        "has_sequences": all(element.sequence for element in circuit.elements),
        "valid_ids": all(element.element_id for element in circuit.elements),
        "reasonable_length": sum(len(e.sequence) for e in circuit.elements) < 1000000
    }
    
    recommendations = []
    
    if not requirements["has_elements"]:
        recommendations.append("Add genetic elements to the circuit")
    
    if not requirements["has_sequences"]:
        recommendations.append("Ensure all elements have valid DNA sequences")
    
    if not requirements["valid_ids"]:
        recommendations.append("Provide unique IDs for all elements")
    
    if not requirements["reasonable_length"]:
        recommendations.append("Consider splitting very large circuits")
    
    all_valid = all(requirements.values())
    
    return {
        "is_exportable": all_valid,
        "requirements": requirements,
        "recommendations": recommendations,
        "export_readiness": sum(requirements.values()) / len(requirements)
    }


def create_export_manifest(circuit, export_files):
    """
    Create manifest file describing all exported files.
    
    Args:
        circuit: Source GeneticCircuit
        export_files: Dictionary of exported file paths
        
    Returns:
        dict: Manifest data
    """
    from datetime import datetime
    
    manifest = {
        "manifest_version": "1.0",
        "creation_timestamp": datetime.now().isoformat(),
        "source_circuit": {
            "circuit_id": circuit.circuit_id,
            "element_count": len(circuit.elements),
            "total_length": sum(len(e.sequence) for e in circuit.elements)
        },
        "exported_files": export_files,
        "export_summary": {
            "total_files": len(export_files),
            "jcvi_compatible": True,
            "visualization_included": HAS_VISUALIZATION,
            "formats": list(export_files.keys())
        },
        "usage_instructions": {
            "jcvi_assembly": "Use assemble.sh script to run JCVI assembly pipeline",
            "genbank": "Import .gb file into genomics tools",
            "gff3": "Use for genome annotation workflows", 
            "visualizations": "View .png files for circuit analysis"
        }
    }
    
    return manifest
