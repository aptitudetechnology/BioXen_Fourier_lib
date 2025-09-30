# GitHub Copilot Codebase Analysis Prompt

## Objective
Analyze the existing BioXen_jcvi_vm_lib codebase to understand the current architecture and inform the development of a comprehensive specification document that aligns with the pylua_bioxen_vm_lib patterns (see `pylua_bioxen_vm_lib_specificationversion-0-1-22.markdown`).

## Analysis Request

Please examine the BioXen_jcvi_vm_lib codebase and provide a detailed report covering the following areas:

### 1. **Current Architecture Analysis**
- What is the existing directory structure under `src/`?
- What core modules currently exist (hypervisor, genome integrator, resource management)?
- What are the main classes and their relationships?
- How does the current hypervisor system work?
- What genome-related functionality already exists?

### 2. **Existing API Surface**
- What public functions/classes are currently available?
- How do users currently interact with the biological VMs?
- What configuration patterns are already in place?
- Are there any existing factory patterns or VM creation methods?
- What resource management capabilities exist?

### 3. **FASTA/Genomic Integration**
- How does the system currently handle FASTA files?
- What genomic data processing capabilities exist?
- How are different genome types (syn3a, ecoli) currently differentiated?
- What cellular simulation or virtualization features are implemented?

### 4. **Resource Management System**
- What resource allocation mechanisms exist (ribosome, ATP, memory)?
- How is biological resource tracking currently implemented?
- What are the existing resource manager classes/functions?
- How does resource allocation integrate with VM lifecycle?

### 5. **Configuration and Setup**
- What configuration files or patterns are currently used?
- How are VM parameters currently managed?
- What initialization processes exist for biological VMs?
- Are there existing config validation mechanisms?

### 6. **Integration Points for Factory Pattern**
- Where in the existing code would the factory pattern API layer integrate?
- What existing methods could be wrapped by the new API?
- Which classes would need minimal modification for factory integration?
- What are the key integration points mentioned in the GitHub Copilot report?

### 7. **Compatibility Assessment**
- What existing functionality must remain unchanged (backward compatibility)?
- Which files are mentioned as requiring no modification (`src/hypervisor/core.py`, `interactive_bioxen.py`)?
- What are the current entry points and user interfaces?
- How do existing workflows currently operate?

### 8. **Missing Components for MVP**
- What components from pylua_bioxen_vm_lib patterns (see `pylua_bioxen_vm_lib_specificationversion-0-1-22.markdown`) are missing?
- What CLI infrastructure exists or needs to be created?
- What session management capabilities need development?
- What inter-VM communication infrastructure exists?

### 9. **Dependencies and External Integrations**
- What external libraries does the project currently use?
- How does it integrate with JCVI tools or other biological software?
- What are the current system requirements?
- Are there existing packaging or distribution mechanisms?

### 10. **Code Quality and Testing**
- What testing infrastructure exists?
- What documentation is currently available?
- What error handling and logging mechanisms are in place?
- What are the current code quality standards?

## Report Format

Please structure your analysis as a comprehensive report with:

1. **Executive Summary** - Key findings and current state
2. **Architecture Overview** - Current system design and components
3. **API Assessment** - Existing interfaces and capabilities
4. **Integration Readiness** - How prepared the code is for factory pattern implementation
5. **Gap Analysis** - What needs to be developed for MVP alignment with pylua_bioxen_vm_lib (see `pylua_bioxen_vm_lib_specificationversion-0-1-22.markdown`)
6. **Implementation Recommendations** - Specific steps for achieving the architectural goals

## Context for Analysis

The goal is to transform BioXen_jcvi_vm_lib into a comprehensive biological VM management system that:
- Virtualizes cellular processes from FASTA genomic data
- Provides multi-cellular VM types (syn3a, ecoli, minimal_cell)
- Includes interactive CLI management
- Supports biological resource allocation
- Enables future inter-VM bio-communication protocols
- Follows the successful architectural patterns of pylua_bioxen_vm_lib (see `pylua_bioxen_vm_lib_specificationversion-0-1-22.markdown`)

This analysis will inform the creation of a detailed specification document that guides the development of a robust biological hypervisor system for computational biology workflows.