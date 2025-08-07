Here's the prompt for your next session:

---

**Context**: We're working with the pylua-bioxen-vm library (https://github.com/aptitudetechnology/pylua-bioxen-vm) to refactor an interactive BioXen CLI application. The current `interactive_bioxen.py` file is over 1500 lines, with a `create_lua_vm()` function that's ~300 lines of manual subprocess management and Lua code generation.

**Current Problem**: The `create_lua_vm()` function manually handles:
- Lua socket server/client/P2P code generation as strings
- Direct subprocess calls to lua interpreter
- Temporary file creation and cleanup
- Custom socket communication logic

**Goal**: Refactor the `create_lua_vm()` function to use the pylua-bioxen-vm library instead of manual implementation, reducing it from ~300 lines to ~50-100 lines.

**Key Library Features to Use**:
- `VMManager()` context manager
- `create_vm(vm_id, networked=True/False)`
- `start_server_vm(vm_id, port)`
- `start_client_vm(vm_id, ip, port, message)`
- `start_p2p_vm(vm_id, local_port, peer_ip, peer_port)`
- `execute_code(vm_id, lua_code)` 
- `execute_script(vm_id, script_path)`

**Request**: Please rewrite the `create_lua_vm()` function to be much more concise by leveraging the pylua-bioxen-vm library's built-in functionality instead of reinventing subprocess management.

**Files**: I'll provide the current bloated function implementation for reference.

---

This should give you a clean starting point for the refactoring work!