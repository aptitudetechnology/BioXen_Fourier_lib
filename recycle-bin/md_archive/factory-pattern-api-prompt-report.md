# Factory Pattern API Prompt Report

## Prompt Requirements

1. `create_bio_vm()` factory function supporting vm_type ("syn3a", "ecoli", "minimal_cell")
2. Base `BiologicalVM` abstract class with:
   - `start_transcription(genes)`
   - `allocate_ribosomes(count)`
   - `get_atp_level()`
   - `execute_metabolic_pathway(pathway)`
   - `get_vm_status()`
3. Concrete `Syn3AVM` and `EColiVM` classes inheriting from `BiologicalVM`
4. `BioResourceManager` class for resource allocation
5. Config management similar to `pylua_bioxen_vm_lib` (config dicts)

## Codebase Findings

- The codebase has advanced VM management, resource tracking (ribosomes, ATP), and state management (see `src/hypervisor/core.py`, `interactive_bioxen.py`).
- VM creation is genome-driven, with resource allocation and ATP/ribosome management (see `create_vm` in `interactive_bioxen.py`).
- There is no explicit MVP factory function named `create_bio_vm()` for biological VMs; VM creation is handled via hypervisor and genome integrator logic.
- No abstract `BiologicalVM` class or unified interface for biological VMs; VM logic is distributed across hypervisor, resource allocation, and genome integrator classes.
- No concrete `Syn3AVM` or `EColiVM` classes; VMs are instantiated generically based on genome data and chassis type.
- Resource management is present (ribosome, ATP, memory), but not via a standalone `BioResourceManager` class.
- Config management uses dictionaries and templates, but not in a unified class pattern as in `pylua_bioxen_vm_lib`.

## Recommendations

- Implement a `BiologicalVM` base class and concrete `Syn3AVM`, `EColiVM` classes for unified biological VM interface.
- Add a `create_bio_vm()` factory function to instantiate VMs by type.
- Refactor resource management into a dedicated `BioResourceManager` class.
- Centralize config management for VMs using config dicts/classes.
- Adapt existing hypervisor and genome logic to use the new factory/API pattern for biological VMs.

## Summary

The codebase contains most biological VM features (transcription, ribosome allocation, ATP, metabolic pathways, status), but does not implement the requested factory pattern or unified API. Refactoring is needed to meet the prompt requirements.
