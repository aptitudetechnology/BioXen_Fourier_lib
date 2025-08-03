"""
JCVI format export functionality for genetic circuits.

This module provides conversion from BioXen genetic circuits to JCVI-compatible
formats for genome assembly, annotation, and analysis workflows.
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from ..core.elements import GeneticCircuit, GeneticElement, ElementType


@dataclass
class JCVIFeature:
    """JCVI-compatible feature representation"""
    feature_type: str
    start: int
    end: int
    strand: str  # '+' or '-'
    attributes: Dict[str, str]
    sequence: str = ""


@dataclass
class JCVIAnnotation:
    """JCVI annotation metadata"""
    gene_id: str
    product: str
    gene_symbol: Optional[str] = None
    ec_number: Optional[str] = None
    go_terms: List[str] = None
    note: Optional[str] = None


@dataclass
class JCVIGenomeRecord:
    """Complete JCVI genome record"""
    accession: str
    organism: str
    sequence: str
    length: int
    features: List[JCVIFeature]
    annotations: List[JCVIAnnotation]
    metadata: Dict[str, str]


class JCVIFormatExporter:
    """Export genetic circuits to JCVI-compatible formats"""
    
    def __init__(self, organism: str = "Synthetic genome", version: str = "1.0"):
        self.organism = organism
        self.version = version
        self.feature_counter = 1
    
    def export_circuit_to_genbank(self, circuit: GeneticCircuit, 
                                 filename: Optional[str] = None) -> str:
        """Export circuit to GenBank format compatible with JCVI tools"""
        
        # Build complete sequence
        complete_sequence = "".join(element.sequence for element in circuit.elements)
        
        # Generate GenBank header
        genbank_content = self._generate_genbank_header(circuit, complete_sequence)
        
        # Add features
        current_position = 1
        for element in circuit.elements:
            feature_block = self._element_to_genbank_feature(element, current_position)
            genbank_content += feature_block
            current_position += len(element.sequence)
        
        # Add sequence section
        genbank_content += self._generate_sequence_section(complete_sequence)
        
        # Add terminator
        genbank_content += "//\n"
        
        # Write to file if filename provided
        if filename:
            with open(filename, 'w') as f:
                f.write(genbank_content)
        
        return genbank_content
    
    def export_circuit_to_gff3(self, circuit: GeneticCircuit,
                              filename: Optional[str] = None) -> str:
        """Export circuit to GFF3 format for JCVI annotation pipeline"""
        
        # GFF3 header
        gff3_content = "##gff-version 3\n"
        gff3_content += f"##sequence-region {circuit.circuit_id} 1 {self._calculate_circuit_length(circuit)}\n"
        
        # Add features
        current_position = 1
        for element in circuit.elements:
            gff3_line = self._element_to_gff3_line(element, current_position, circuit.circuit_id)
            gff3_content += gff3_line
            current_position += len(element.sequence)
        
        # Add FASTA sequence section
        gff3_content += "##FASTA\n"
        gff3_content += f">{circuit.circuit_id}\n"
        complete_sequence = "".join(element.sequence for element in circuit.elements)
        gff3_content += self._format_fasta_sequence(complete_sequence)
        
        # Write to file if filename provided
        if filename:
            with open(filename, 'w') as f:
                f.write(gff3_content)
        
        return gff3_content
    
    def export_circuit_to_jcvi_json(self, circuit: GeneticCircuit,
                                   filename: Optional[str] = None) -> str:
        """Export circuit to JCVI JSON format for computational analysis"""
        
        # Build JCVI genome record
        genome_record = self._circuit_to_jcvi_record(circuit)
        
        # Convert to JSON
        json_data = {
            "genome_record": asdict(genome_record),
            "export_info": {
                "exporter": "BioXen JCVI Exporter",
                "version": self.version,
                "timestamp": datetime.now().isoformat(),
                "source_circuit": circuit.circuit_id
            }
        }
        
        json_content = json.dumps(json_data, indent=2)
        
        # Write to file if filename provided
        if filename:
            with open(filename, 'w') as f:
                f.write(json_content)
        
        return json_content
    
    def export_for_jcvi_assembly(self, circuit: GeneticCircuit, 
                                output_dir: str = "./jcvi_export") -> Dict[str, str]:
        """Export circuit files for JCVI genome assembly pipeline"""
        import os
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        files_created = {}
        
        # Export sequence FASTA
        fasta_file = os.path.join(output_dir, f"{circuit.circuit_id}.fasta")
        fasta_content = self._export_circuit_fasta(circuit)
        with open(fasta_file, 'w') as f:
            f.write(fasta_content)
        files_created["fasta"] = fasta_file
        
        # Export feature table
        feature_file = os.path.join(output_dir, f"{circuit.circuit_id}.tbl")
        feature_content = self._export_feature_table(circuit)
        with open(feature_file, 'w') as f:
            f.write(feature_content)
        files_created["features"] = feature_file
        
        # Export AGP file for assembly
        agp_file = os.path.join(output_dir, f"{circuit.circuit_id}.agp")
        agp_content = self._export_agp_file(circuit)
        with open(agp_file, 'w') as f:
            f.write(agp_content)
        files_created["agp"] = agp_file
        
        # Export metadata
        metadata_file = os.path.join(output_dir, f"{circuit.circuit_id}_metadata.json")
        metadata = self._export_circuit_metadata(circuit)
        with open(metadata_file, 'w') as f:
            f.write(json.dumps(metadata, indent=2))
        files_created["metadata"] = metadata_file
        
        return files_created
    
    def _circuit_to_jcvi_record(self, circuit: GeneticCircuit) -> JCVIGenomeRecord:
        """Convert circuit to JCVI genome record"""
        
        complete_sequence = "".join(element.sequence for element in circuit.elements)
        features = []
        annotations = []
        
        current_position = 1
        for element in circuit.elements:
            # Create JCVI feature
            feature = JCVIFeature(
                feature_type=self._element_type_to_jcvi_type(element.element_type),
                start=current_position,
                end=current_position + len(element.sequence) - 1,
                strand='+',
                attributes={
                    "ID": element.element_id,
                    "Name": element.element_id,
                    "note": f"BioXen {element.element_type.value}"
                },
                sequence=element.sequence
            )
            features.append(feature)
            
            # Create annotation if it's a gene
            if element.element_type == ElementType.GENE:
                annotation = JCVIAnnotation(
                    gene_id=element.element_id,
                    product=f"Synthetic {element.element_id}",
                    note="Generated by BioXen hypervisor"
                )
                annotations.append(annotation)
            
            current_position += len(element.sequence)
        
        # Create genome record
        return JCVIGenomeRecord(
            accession=circuit.circuit_id,
            organism=self.organism,
            sequence=complete_sequence,
            length=len(complete_sequence),
            features=features,
            annotations=annotations,
            metadata={
                "source": "BioXen Hypervisor",
                "version": self.version,
                "topology": "linear",
                "molecule_type": "DNA"
            }
        )
    
    def _generate_genbank_header(self, circuit: GeneticCircuit, sequence: str) -> str:
        """Generate GenBank format header"""
        header = f"LOCUS       {circuit.circuit_id:<16} {len(sequence):>8} bp    DNA     linear   SYN {datetime.now().strftime('%d-%b-%Y').upper()}\n"
        header += f"DEFINITION  {circuit.circuit_id} - Synthetic genetic circuit from BioXen\n"
        header += f"ACCESSION   {circuit.circuit_id}\n"
        header += f"VERSION     {circuit.circuit_id}.1\n"
        header += "KEYWORDS    synthetic biology; genetic circuit; BioXen hypervisor\n"
        header += f"SOURCE      {self.organism}\n"
        header += f"  ORGANISM  {self.organism}\n"
        header += "            synthetic construct.\n"
        header += "FEATURES             Location/Qualifiers\n"
        
        return header
    
    def _element_to_genbank_feature(self, element: GeneticElement, start_pos: int) -> str:
        """Convert element to GenBank feature"""
        end_pos = start_pos + len(element.sequence) - 1
        feature_type = self._element_type_to_genbank_type(element.element_type)
        
        feature = f"     {feature_type:<15} {start_pos}..{end_pos}\n"
        feature += f"                     /label=\"{element.element_id}\"\n"
        feature += f"                     /note=\"BioXen {element.element_type.value}\"\n"
        
        if element.element_type == ElementType.GENE:
            feature += f"                     /product=\"{element.element_id} protein\"\n"
            feature += f"                     /gene=\"{element.element_id}\"\n"
        
        if element.regulation_target:
            feature += f"                     /regulatory_target=\"{element.regulation_target}\"\n"
        
        return feature
    
    def _element_to_gff3_line(self, element: GeneticElement, start_pos: int, seqid: str) -> str:
        """Convert element to GFF3 line"""
        end_pos = start_pos + len(element.sequence) - 1
        feature_type = self._element_type_to_gff3_type(element.element_type)
        
        # GFF3 format: seqid, source, type, start, end, score, strand, phase, attributes
        attributes = f"ID={element.element_id};Name={element.element_id}"
        
        if element.regulation_target:
            attributes += f";Target={element.regulation_target}"
        
        attributes += f";Note=BioXen {element.element_type.value}"
        
        gff3_line = f"{seqid}\tBioXen\t{feature_type}\t{start_pos}\t{end_pos}\t.\t+\t.\t{attributes}\n"
        
        return gff3_line
    
    def _export_circuit_fasta(self, circuit: GeneticCircuit) -> str:
        """Export circuit as FASTA sequence"""
        complete_sequence = "".join(element.sequence for element in circuit.elements)
        
        fasta_content = f">{circuit.circuit_id} BioXen synthetic circuit\n"
        fasta_content += self._format_fasta_sequence(complete_sequence)
        
        return fasta_content
    
    def _export_feature_table(self, circuit: GeneticCircuit) -> str:
        """Export feature table for JCVI tools"""
        feature_table = ">Feature " + circuit.circuit_id + "\n"
        
        current_position = 1
        for element in circuit.elements:
            end_pos = current_position + len(element.sequence) - 1
            feature_type = self._element_type_to_feature_table_type(element.element_type)
            
            feature_table += f"{current_position}\t{end_pos}\t{feature_type}\n"
            feature_table += f"\t\t\tlabel\t{element.element_id}\n"
            feature_table += f"\t\t\tnote\tBioXen {element.element_type.value}\n"
            
            current_position += len(element.sequence)
        
        return feature_table
    
    def _export_agp_file(self, circuit: GeneticCircuit) -> str:
        """Export AGP file for genome assembly"""
        agp_content = ""
        
        current_position = 1
        for i, element in enumerate(circuit.elements, 1):
            end_pos = current_position + len(element.sequence) - 1
            
            # AGP format: object, object_beg, object_end, part_number, component_type, ...
            agp_line = f"{circuit.circuit_id}\t{current_position}\t{end_pos}\t{i}\tW\t"
            agp_line += f"{element.element_id}\t1\t{len(element.sequence)}\t+\n"
            
            agp_content += agp_line
            current_position += len(element.sequence)
        
        return agp_content
    
    def _export_circuit_metadata(self, circuit: GeneticCircuit) -> Dict:
        """Export circuit metadata for JCVI processing"""
        return {
            "circuit_id": circuit.circuit_id,
            "organism": self.organism,
            "total_length": self._calculate_circuit_length(circuit),
            "element_count": len(circuit.elements),
            "elements": [
                {
                    "id": element.element_id,
                    "type": element.element_type.value,
                    "length": len(element.sequence),
                    "regulation_target": element.regulation_target
                }
                for element in circuit.elements
            ],
            "export_timestamp": datetime.now().isoformat(),
            "exporter_version": self.version
        }
    
    def _calculate_circuit_length(self, circuit: GeneticCircuit) -> int:
        """Calculate total circuit length"""
        return sum(len(element.sequence) for element in circuit.elements)
    
    def _format_fasta_sequence(self, sequence: str, line_length: int = 70) -> str:
        """Format sequence for FASTA output"""
        formatted = ""
        for i in range(0, len(sequence), line_length):
            formatted += sequence[i:i+line_length] + "\n"
        return formatted
    
    def _element_type_to_jcvi_type(self, element_type: ElementType) -> str:
        """Convert element type to JCVI feature type"""
        mapping = {
            ElementType.GENE: "CDS",
            ElementType.PROMOTER: "promoter",
            ElementType.TERMINATOR: "terminator",
            ElementType.RBS: "ribosome_binding_site",
            ElementType.OPERATOR: "operator"
        }
        return mapping.get(element_type, "misc_feature")
    
    def _element_type_to_genbank_type(self, element_type: ElementType) -> str:
        """Convert element type to GenBank feature type"""
        mapping = {
            ElementType.GENE: "CDS",
            ElementType.PROMOTER: "promoter", 
            ElementType.TERMINATOR: "terminator",
            ElementType.RBS: "RBS",
            ElementType.OPERATOR: "regulatory"
        }
        return mapping.get(element_type, "misc_feature")
    
    def _element_type_to_gff3_type(self, element_type: ElementType) -> str:
        """Convert element type to GFF3 feature type"""
        mapping = {
            ElementType.GENE: "gene",
            ElementType.PROMOTER: "promoter",
            ElementType.TERMINATOR: "terminator", 
            ElementType.RBS: "ribosome_entry_site",
            ElementType.OPERATOR: "operator"
        }
        return mapping.get(element_type, "biological_region")
    
    def _element_type_to_feature_table_type(self, element_type: ElementType) -> str:
        """Convert element type to feature table type"""
        mapping = {
            ElementType.GENE: "gene",
            ElementType.PROMOTER: "regulatory",
            ElementType.TERMINATOR: "regulatory",
            ElementType.RBS: "regulatory", 
            ElementType.OPERATOR: "regulatory"
        }
        return mapping.get(element_type, "misc_feature")


def export_multiple_circuits_to_jcvi(circuits: List[GeneticCircuit], 
                                    output_dir: str = "./jcvi_batch_export") -> Dict[str, Dict[str, str]]:
    """Export multiple circuits for JCVI batch processing"""
    import os
    
    os.makedirs(output_dir, exist_ok=True)
    exporter = JCVIFormatExporter()
    
    results = {}
    for circuit in circuits:
        circuit_dir = os.path.join(output_dir, circuit.circuit_id)
        files = exporter.export_for_jcvi_assembly(circuit, circuit_dir)
        results[circuit.circuit_id] = files
    
    return results


def create_jcvi_assembly_script(circuit: GeneticCircuit, output_file: str = "assemble.sh") -> str:
    """Create shell script for JCVI assembly workflow"""
    
    script_content = f"""#!/bin/bash
# JCVI Assembly Script for {circuit.circuit_id}
# Generated by BioXen JCVI Exporter

echo "Starting JCVI assembly for {circuit.circuit_id}"

# Set up paths
CIRCUIT_ID="{circuit.circuit_id}"
FASTA_FILE="${circuit.circuit_id}.fasta"
FEATURE_FILE="${circuit.circuit_id}.tbl"
AGP_FILE="${circuit.circuit_id}.agp"

# Validate input files
if [ ! -f "$FASTA_FILE" ]; then
    echo "Error: FASTA file not found: $FASTA_FILE"
    exit 1
fi

if [ ! -f "$FEATURE_FILE" ]; then
    echo "Error: Feature file not found: $FEATURE_FILE"
    exit 1
fi

# Run JCVI assembly validation
echo "Validating assembly..."
python -m jcvi.assembly.base validate $FASTA_FILE

# Generate assembly statistics
echo "Generating assembly statistics..."
python -m jcvi.assembly.base stats $FASTA_FILE

# Process features if available
if [ -f "$FEATURE_FILE" ]; then
    echo "Processing feature annotations..."
    python -m jcvi.annotation.base process $FEATURE_FILE $FASTA_FILE
fi

# Generate final assembly report
echo "Generating assembly report..."
python -m jcvi.assembly.base report $FASTA_FILE > ${{CIRCUIT_ID}}_assembly_report.txt

echo "Assembly processing complete for $CIRCUIT_ID"
"""

    with open(output_file, 'w') as f:
        f.write(script_content)
    
    # Make script executable
    import os
    os.chmod(output_file, 0o755)
    
    return script_content
