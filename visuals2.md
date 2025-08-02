# BioXen MVP Visualizer with Dual MP4 Export - Implementation Specifications

## Updated Requirements Analysis

Based on the comprehensive analysis document, BioXen already has mature data export capabilities and sophisticated biological modeling. This significantly simplifies our visualization implementation while maintaining high scientific accuracy.

## Revised MVP Scope

### Leveraging Existing BioXen Infrastructure

#### Already Available Data Streams
```python
# From existing hypervisor core
vm_status = {
    "vm_id": "research-vm",
    "state": "running",
    "genome_template": "syn3a_minimal", 
    "resources": {
        "ribosomes": 25,
        "atp_percentage": 35.0,
        "memory_kb": 150,
        "priority": 3
    },
    "uptime_seconds": 145.2,
    "health_status": "healthy"
}

system_resources = {
    "total_ribosomes": 80,
    "available_ribosomes": 15,
    "allocated_ribosomes": 65,
    "active_vms": 3,
    "chassis_type": "ecoli"
}
```

#### Enhanced Data Export (Minimal Python Changes)
```python
# Add to existing hypervisor export
def export_visualization_data(self):
    base_data = self.get_system_status()  # Existing method
    
    # Add cellular activity simulation
    for vm_id, vm in self.vms.items():
        base_data['vms'][vm_id]['cellular_activity'] = {
            'transcription_rate': vm.resources.ribosomes * 1.2,  # Based on ribosome allocation
            'active_genes': min(50, vm.resources.ribosomes * 2), # Gene expression simulation
            'metabolic_activity': vm.resources.atp_percentage / 100.0
        }
    
    return base_data
```

## Love2D Implementation Specifications

### Core Visualization Components

#### 1. VM Cellular Compartments
```lua
-- VM representation as cellular compartments
local VM = {
    x = 0, y = 0,
    width = 300, height = 200,
    id = "",
    state = "created",
    genome = "",
    
    -- Cellular elements
    dna_helix = {},
    ribosomes = {},  -- Particle positions
    atp_particles = {},
    transcription_bubbles = {}
}

function VM:draw()
    -- Draw cellular membrane
    love.graphics.setColor(0.8, 0.9, 1.0, 0.3)
    love.graphics.rectangle("fill", self.x, self.y, self.width, self.height)
    
    -- Draw DNA helix (two parallel lines)
    love.graphics.setColor(0.2, 0.6, 1.0)
    love.graphics.line(self.x + 20, self.y + 50, self.x + self.width - 20, self.y + 50)
    love.graphics.line(self.x + 20, self.y + 60, self.x + self.width - 20, self.y + 60)
    
    -- Draw gene expression activity
    self:drawGeneExpression()
    self:drawRibosomes()
    self:drawATPFlow()
end

function VM:drawGeneExpression()
    -- Animate transcription bubbles based on active_genes count
    local bubble_count = math.floor(self.data.cellular_activity.active_genes / 10)
    
    for i = 1, bubble_count do
        local x = self.x + 30 + (i * 40) % (self.width - 60)
        local y = self.y + 55
        local time_offset = love.timer.getTime() + i * 0.5
        local pulse = math.sin(time_offset * 2) * 0.3 + 0.7
        
        love.graphics.setColor(1.0, 0.8, 0.2, pulse)
        love.graphics.circle("fill", x, y, 8)
    end
end
```

#### 2. Dual Recording System Implementation
```lua
-- Recording manager supporting both methods
local RecordingManager = {
    method = "auto", -- "canvas", "external", "auto"
    canvas_recorder = nil,
    external_recorder = nil,
    active = false,
    current_method = nil
}

function RecordingManager:init()
    -- Initialize canvas recording system
    self.canvas_recorder = CanvasRecorder:new()
    self.external_recorder = ExternalRecorder:new()
end

function RecordingManager:startRecording(config)
    local method = config.method or self.method
    local success = false
    
    -- Try canvas recording first (high quality)
    if method == "canvas" or method == "auto" then
        success = self.canvas_recorder:start(config)
        if success then
            self.current_method = "canvas"
            print("Started canvas recording")
        end
    end
    
    -- Fallback to external recording
    if not success and (method == "external" or method == "auto") then
        success = self.external_recorder:start(config)
        if success then
            self.current_method = "external" 
            print("Started external recording")
        end
    end
    
    self.active = success
    return success
end
```

#### 3. Canvas Recording Implementation
```lua
local CanvasRecorder = {}
CanvasRecorder.__index = CanvasRecorder

function CanvasRecorder:new()
    local recorder = {
        canvas = nil,
        frames = {},
        frame_count = 0,
        target_fps = 30,
        recording = false,
        output_file = "",
        temp_dir = "temp_frames/"
    }
    setmetatable(recorder, CanvasRecorder)
    return recorder
end

function CanvasRecorder:start(config)
    -- Create recording canvas
    self.canvas = love.graphics.newCanvas(config.width or 1280, config.height or 720)
    self.output_file = config.filename
    self.recording = true
    self.frame_count = 0
    
    -- Create temp directory
    love.filesystem.createDirectory(self.temp_dir)
    
    return true
end

function CanvasRecorder:captureFrame()
    if not self.recording then return end
    
    -- Render current frame to canvas
    love.graphics.setCanvas(self.canvas)
    love.graphics.clear()
    
    -- Draw all visualization elements
    drawBackground()
    drawAllVMs()
    drawSystemStatus()
    drawUI()
    
    love.graphics.setCanvas()
    
    -- Save frame as PNG
    local image_data = self.canvas:newImageData()
    local filename = self.temp_dir .. string.format("frame_%06d.png", self.frame_count)
    image_data:encode("png", filename)
    
    self.frame_count = self.frame_count + 1
end

function CanvasRecorder:stop()
    if not self.recording then return end
    
    self.recording = false
    
    -- Convert frames to MP4 using FFmpeg
    local ffmpeg_cmd = string.format(
        'ffmpeg -r %d -i "%sframe_%%06d.png" -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p "%s"',
        self.target_fps, self.temp_dir, self.output_file
    )
    
    local success = os.execute(ffmpeg_cmd)
    
    if success then
        -- Clean up temp frames
        self:cleanupFrames()
        print("Video saved:", self.output_file)
        return true
    else
        print("Error: FFmpeg conversion failed")
        return false
    end
end
```

#### 4. External Recording Implementation
```lua
local ExternalRecorder = {}
ExternalRecorder.__index = ExternalRecorder

function ExternalRecorder:new()
    local recorder = {
        process = nil,
        recording = false,
        output_file = ""
    }
    setmetatable(recorder, ExternalRecorder)
    return recorder
end

function ExternalRecorder:start(config)
    local cmd = self:getFFmpegCommand(config)
    if not cmd then
        print("Error: Unsupported OS for external recording")
        return false
    end
    
    -- Start FFmpeg process
    self.process = io.popen(cmd .. " 2>&1", "r")
    self.recording = true
    self.output_file = config.filename
    
    print("Started external recording:", config.filename)
    return true
end

function ExternalRecorder:getFFmpegCommand(config)
    local os_name = love.system.getOS()
    local duration = config.duration or 60
    local framerate = config.framerate or 30
    
    if os_name == "Windows" then
        return string.format(
            'ffmpeg -f gdigrab -framerate %d -t %d -i title="BioXen Cellular Visualizer" -c:v libx264 -preset fast "%s"',
            framerate, duration, config.filename
        )
    elseif os_name == "Linux" then
        return string.format(
            'ffmpeg -f x11grab -framerate %d -t %d -i :0.0 -s 1280x720 -c:v libx264 -preset fast "%s"',
            framerate, duration, config.filename
        )
    elseif os_name == "OS X" then
        return string.format(
            'ffmpeg -f avfoundation -framerate %d -t %d -i "1:none" -c:v libx264 -preset fast "%s"',
            framerate, duration, config.filename
        )
    end
    
    return nil
end

function ExternalRecorder:stop()
    if self.process then
        self.process:close()
        self.process = nil
    end
    self.recording = false
    print("External recording stopped")
end
```

### Python Integration (Minimal Changes Required)

#### Enhanced Visualization Export
```python
# Add to existing BioXen hypervisor class
class BioXenHypervisor:
    def __init__(self, chassis_type=ChassisType.ECOLI):
        # ... existing init code ...
        self.visualization_enabled = False
        self.viz_export_interval = 1.0  # seconds
        self.last_viz_export = 0
    
    def enable_visualization(self, export_interval=1.0):
        """Enable visualization data export"""
        self.visualization_enabled = True
        self.viz_export_interval = export_interval
    
    def export_visualization_data(self):
        """Export current system state for visualization"""
        if not self.visualization_enabled:
            return
        
        current_time = time.time()
        if current_time - self.last_viz_export < self.viz_export_interval:
            return
        
        viz_data = {
            "timestamp": current_time,
            "chassis": {
                "type": self.chassis.chassis_type.value,
                "total_ribosomes": self.chassis.capabilities.max_ribosomes,
                "available_ribosomes": self.chassis.current_resources.available_ribosomes
            },
            "vms": {}
        }
        
        # Export VM data with cellular activity simulation
        for vm_id, vm in self.vms.items():
            viz_data["vms"][vm_id] = {
                "id": vm_id,
                "state": vm.state.value,
                "genome": vm.genome_template,
                "resources": {
                    "ribosomes": vm.resources.ribosomes,
                    "atp_percentage": vm.resources.atp_percentage,
                    "memory_kb": vm.resources.memory_kb
                },
                "cellular_activity": self._simulate_cellular_activity(vm),
                "uptime": current_time - (vm.start_time or current_time)
            }
        
        # Write to file for Love2D to read
        with open("bioxen_visualization.json", "w") as f:
            json.dump(viz_data, f, indent=2)
        
        self.last_viz_export = current_time
    
    def _simulate_cellular_activity(self, vm):
        """Generate realistic cellular activity based on VM resources"""
        if vm.state != VMState.RUNNING:
            return {
                "active_genes": 0,
                "transcription_rate": 0,
                "metabolic_activity": 0
            }
        
        # Base activity on resource allocation
        base_activity = vm.resources.atp_percentage / 100.0
        ribosome_factor = vm.resources.ribosomes / 30.0  # Normalize to typical allocation
        
        return {
            "active_genes": int(vm.resources.ribosomes * 1.5 * base_activity),
            "transcription_rate": vm.resources.ribosomes * 0.8 * base_activity,
            "metabolic_activity": base_activity
        }

# Recording control methods
def start_visualization_recording(self, duration=60, method="auto", filename=None):
    """Start recording visualization"""
    if not filename:
        timestamp = int(time.time())
        filename = f"bioxen_recording_{timestamp}.mp4"
    
    recording_command = {
        "action": "start_recording",
        "method": method,
        "duration": duration,
        "filename": filename,
        "timestamp": time.time()
    }
    
    with open("bioxen_recording_command.json", "w") as f:
        json.dump(recording_command, f)
    
    return filename

def stop_visualization_recording(self):
    """Stop current recording"""
    stop_command = {
        "action": "stop_recording",
        "timestamp": time.time()
    }
    
    with open("bioxen_recording_command.json", "w") as f:
        json.dump(stop_command, f)
```

## Implementation Timeline

### Week 1: MVP Development
- **Day 1-2**: Love2D basic structure with VM compartments
- **Day 3**: Python integration and JSON data pipeline  
- **Day 4**: Basic cellular animation (gene expression)
- **Day 5**: Testing and polish

### Week 2: Recording Implementation
- **Day 1-2**: Canvas recording system
- **Day 3**: External recording system
- **Day 4**: Recording controls and UI
- **Day 5**: Cross-platform testing

### Week 3: Enhancement and Polish
- **Day 1-2**: Advanced cellular animations
- **Day 3**: Performance optimization
- **Day 4-5**: Documentation and examples

## Quality Assurance

### Testing Strategy
- **Unit Tests**: Individual recording methods
- **Integration Tests**: Python-Love2D communication
- **Platform Tests**: Windows, macOS, Linux recording
- **Performance Tests**: Long-duration recordings, multiple VMs

### Success Metrics
- ✅ 60 FPS visualization with 4 active VMs
- ✅ Both recording methods produce valid MP4 files
- ✅ <5% impact on BioXen performance when visualizing
- ✅ Cross-platform compatibility confirmed

This specification leverages BioXen's existing sophisticated architecture while adding compelling visualizations and robust video recording capabilities through a dual-method approach.