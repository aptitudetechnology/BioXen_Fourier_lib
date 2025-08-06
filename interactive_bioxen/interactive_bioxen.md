# Plan to Modularize `interactive_bioxen.py`

## Motivation
- The current `interactive_bioxen.py` is over 1500 lines and difficult to maintain, test, and extend.
- Modularization will improve readability, enable unit testing, and allow for easier feature development and bug fixes.

## High-Level Goals
- Split the monolithic CLI into logical modules by responsibility.
- Use clear interfaces and separation of concerns.
- Enable future extensibility (e.g., plugins, new chassis, visualization modes).

## Proposed Modules

### 1. CLI Core
- **File:** `cli/core.py`
- **Responsibility:** Main menu loop, user interaction, command dispatch.
- **Contents:** Main CLI class, menu logic, error handling.

### 2. Genome Management
- **File:** `cli/genome.py`
- **Responsibility:** Browse, validate, download, and simulate genomes.
- **Contents:** Genome loading, validation, download helpers, simulated genome creation.

### 3. Hypervisor & VM Management
- **File:** `cli/hypervisor.py`
- **Responsibility:** Chassis selection, hypervisor initialization, VM creation, destruction, status reporting.
- **Contents:** Chassis logic, resource allocation, VM lifecycle management.

### 4. Visualization
- **File:** `cli/visualization.py`
- **Responsibility:** Terminal DNA visualization, integration with Rich-based and legacy visualizers.
- **Contents:** Visualization launchers, data adapters, CLI hooks.

### 5. Lua VM Integration
- **File:** `cli/lua_vm.py`
- **Responsibility:** Lua VM creation, socket/server/client/P2P logic, script generation and cleanup.
- **Contents:** Lua subprocess management, script templates, error handling.

### 6. Utilities & Helpers
- **File:** `cli/utils.py`
- **Responsibility:** Common utility functions, file management, error reporting.
- **Contents:** Path helpers, file cleanup, logging.

## Refactoring Steps
1. **Identify logical boundaries:** Mark regions in `interactive_bioxen.py` for each responsibility.
2. **Extract classes/functions:** Move code into new module files, preserving interfaces.
3. **Update imports:** Refactor imports to use new module structure.
4. **Test incrementally:** After each extraction, run CLI and unit tests to ensure stability.
5. **Document interfaces:** Add docstrings and usage examples for each module.
6. **Enable plugin/extensibility:** Consider using entry points or hooks for future features.

## Example Directory Structure
```
cli/
  core.py
  genome.py
  hypervisor.py
  visualization.py
  lua_vm.py
  utils.py
```

## Benefits
- Easier maintenance and onboarding for new contributors
- Improved testability and reliability
- Faster feature development and bug fixing
- Clear separation of concerns for future growth

## Next Steps
- Review and approve this plan
- Begin incremental extraction, starting with CLI core and genome management
- Track progress in this markdown file
