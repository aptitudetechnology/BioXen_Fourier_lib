# BioLib2D Library Issues & Requirements

## 📋 **Current Status**

**BioLib2D Version**: 1.0-1 (installed via LuaRocks)  
**Installation Location**: `/home/chris/.luarocks/lib/luarocks/rocks-5.1/biolib2d/1.0-1/`  
**Library Status**: ⚠️ **Missing Required Submodules**  
**Demo Status**: ✅ **Standalone demo created as workaround**

## 🚨 **Primary Issues with BioLib2D Library**

### **1. Missing Submodule Dependencies**

The main BioLib2D module (`init.lua`) attempts to require several submodules that are **not included** in the LuaRocks package:

```lua
-- From biolib2d/init.lua (lines 15-19):
local BioXenConnector = require("biolib2d.connector")    -- ❌ MISSING
local VMCell = require("biolib2d.vmcell")                -- ❌ MISSING  
local ATPSystem = require("biolib2d.atpsystem")          -- ❌ MISSING
local GeneticCircuits = require("biolib2d.circuits")     -- ❌ MISSING
local utils = require("biolib2d.utils")                  -- ❌ MISSING
```

**Error Result**: When trying to use the library, Lua throws:
```
module 'biolib2d.connector' not found
module 'biolib2d.vmcell' not found
module 'biolib2d.atpsystem' not found
module 'biolib2d.circuits' not found
module 'biolib2d.utils' not found
```

### **2. Incomplete Package Structure**

**Expected Structure** (based on `init.lua` requirements):
```
biolib2d/
├── init.lua                    ✅ Present
├── connector.lua               ❌ Missing - BioXen data connection
├── vmcell.lua                  ❌ Missing - Virtual machine cell visualization
├── atpsystem.lua               ❌ Missing - ATP particle system
├── circuits.lua                ❌ Missing - Genetic circuit visualization
├── utils.lua                   ❌ Missing - Utility functions
└── biolib2d-1.0.0-1.rockspec  ✅ Present
```

**Actual Structure** (installed via LuaRocks):
```
biolib2d/
├── init.lua                    ✅ Present (but non-functional)
└── biolib2d-1.0.0-1.rockspec  ✅ Present
```

### **3. No Standalone Love2D Application**

The library provides a **module interface** but lacks a **standalone demo application**:

- ❌ **No `main.lua`** for direct Love2D execution
- ❌ **No sample data files** for testing
- ❌ **No demo configuration** examples

**Current Workaround**: Created standalone demo at `/home/chris/BioXen-jcvi/libs/biolib2d/main.lua`

## 🔧 **Required Fixes for BioLib2D Library**

### **Fix 1: Create Missing Submodules**

The following Lua modules need to be implemented:

#### **A. `biolib2d/connector.lua`**
```lua
-- Required functions based on init.lua usage:
local BioXenConnector = {}

function BioXenConnector:new(data_source)
    -- Load data from JSON file or BioXen API
end

function BioXenConnector:update(dt)
    -- Update connection to BioXen data
end

function BioXenConnector:getSystemData()
    -- Return structured data for visualization
    return {
        chassis_type = "ecoli",
        total_ribosomes = 80,
        allocated_ribosomes = 65,
        vms = { /* VM data */ }
    }
end

return BioXenConnector
```

#### **B. `biolib2d/vmcell.lua`**
```lua
-- Required for VM visualization
local VMCell = {}

function VMCell:new(x, y, width, height, vm_id)
    -- Create VM cell visual representation
end

function VMCell:update(dt, vm_data)
    -- Update VM state and animations
end

function VMCell:draw()
    -- Render VM cell with Love2D graphics
end

return VMCell
```

#### **C. `biolib2d/atpsystem.lua`**
```lua
-- Required for ATP particle system
local ATPSystem = {}

function ATPSystem:new()
    -- Initialize ATP particle system
end

function ATPSystem:update(dt, system_data)
    -- Update ATP flow animations
end

function ATPSystem:draw()
    -- Render ATP particles and flow
end

return ATPSystem
```

#### **D. `biolib2d/circuits.lua`**
```lua
-- Required for genetic circuit visualization
local GeneticCircuits = {}

function GeneticCircuits:new()
    -- Initialize genetic circuit display
end

function GeneticCircuits:update(dt, vm_data)
    -- Update circuit animations
end

function GeneticCircuits:draw(x, y)
    -- Render genetic circuits
end

return GeneticCircuits
```

#### **E. `biolib2d/utils.lua`**
```lua
-- Required utility functions
local utils = {}

function utils.table_length(t)
    local count = 0
    for _ in pairs(t) do count = count + 1 end
    return count
end

-- Add other utility functions as needed

return utils
```

### **Fix 2: Update LuaRocks Package**

The `biolib2d-1.0.0-1.rockspec` needs to include all required files:

```lua
package = "biolib2d"
version = "1.0-1"

source = {
   url = "https://github.com/aptitudetechnology/BioLib2D/archive/v1.0.tar.gz"
}

description = {
   summary = "Real-time biological process visualization for Love2D",
   detailed = "BioLib2D provides real-time visualization of cellular processes, ATP flow, genetic circuits, and virtual machine states for the BioXen biological hypervisor.",
   license = "MIT"
}

dependencies = {
   "lua >= 5.1"
}

build = {
   type = "builtin",
   modules = {
      ["biolib2d"] = "init.lua",
      ["biolib2d.connector"] = "connector.lua",      -- ← ADD THESE
      ["biolib2d.vmcell"] = "vmcell.lua",           -- ← ADD THESE  
      ["biolib2d.atpsystem"] = "atpsystem.lua",     -- ← ADD THESE
      ["biolib2d.circuits"] = "circuits.lua",       -- ← ADD THESE
      ["biolib2d.utils"] = "utils.lua"              -- ← ADD THESE
   }
}
```

### **Fix 3: Add Demo Application**

Include a `demo/main.lua` file for standalone testing:

```lua
-- demo/main.lua
local BioLib2D = require("biolib2d")

function love.load()
    biovis = BioLib2D:new({
        data_source = "sample_data.json"
    })
end

function love.update(dt)
    biovis:update(dt)
end

function love.draw()
    biovis:draw()
end

function love.keypressed(key)
    biovis:keypressed(key)
end
```

### **Fix 4: Add Sample Data File**

Include `sample_data.json` for testing:

```json
{
    "system": {
        "chassis_type": "ecoli",
        "total_ribosomes": 80,
        "allocated_ribosomes": 65
    },
    "vms": {
        "syn3a_vm1": {
            "vm_id": "syn3a_vm1",
            "state": "running",
            "genome": "JCVI-Syn3A",
            "genes": 187,
            "active_genes": 68,
            "ribosomes": 25,
            "atp_percentage": 75.4,
            "cellular_activity": {
                "transcription_rate": 30.0,
                "translation_rate": 25.0,
                "active_genes": ["dnaA", "rpoA", "gyrA"]
            }
        }
    }
}
```

## 🚀 **Recommended Repository Structure**

For the complete BioLib2D library:

```
BioLib2D/
├── README.md                   # Installation and usage guide
├── LICENSE                     # License file
├── biolib2d-1.0.0-1.rockspec  # LuaRocks package specification
├── init.lua                    # Main library entry point
├── connector.lua               # BioXen data connection
├── vmcell.lua                  # VM cell visualization
├── atpsystem.lua               # ATP particle system
├── circuits.lua                # Genetic circuit display
├── utils.lua                   # Utility functions
├── demo/
│   ├── main.lua               # Standalone Love2D demo
│   ├── sample_data.json       # Sample BioXen data
│   └── README.md              # Demo instructions
└── docs/
    ├── API.md                 # API documentation
    └── examples/              # Usage examples
```

## 🧪 **Testing Requirements**

After fixes, the library should support:

1. **Module Loading**: `local BioLib2D = require("biolib2d")` should work without errors
2. **Initialization**: `biovis = BioLib2D:new(config)` should create working instance
3. **Love2D Integration**: Should work with standard Love2D callbacks
4. **Data Connection**: Should handle both JSON files and live BioXen API data
5. **Interactive Controls**: SPACE, G, I, +/- keys should work as documented

## 🎯 **Success Criteria**

The library will be considered **fixed** when:

- ✅ All submodules load without errors
- ✅ Demo application runs successfully with `love demo/`
- ✅ Real-time visualization displays properly
- ✅ Interactive controls function correctly
- ✅ Integration with BioXen data works seamlessly

## 💡 **Alternative Solutions**

Until the library is fixed:

1. **Use Standalone Demo**: The created `/home/chris/BioXen-jcvi/libs/biolib2d/main.lua` provides full functionality
2. **Create Local Modules**: Implement missing modules locally for development
3. **Fork and Fix**: Fork the BioLib2D repository and implement missing components

## 📞 **Contact Information**

For BioLib2D library fixes, contact the maintainer at:
- **Repository**: https://github.com/aptitudetechnology/BioLib2D
- **LuaRocks**: https://luarocks.org/modules/caston1981/biolib2d

---

**Note**: The standalone demo in `main.lua` demonstrates what the **complete BioLib2D library should provide** when properly implemented. This serves as both a workaround and a specification for the required functionality.
