# BioXen VM Cellular Process Visualization Requirements

## Project Overview
Extend BioXen's biological hypervisor with real-time visualization of cellular processes occurring inside each Virtual Machine (VM). The visualization system should provide intuitive, scientifically accurate representations of molecular biology processes while maintaining the educational and research value of the platform.

## Technical Architecture Requirements

### Integration Approach
- **Hybrid Architecture**: Maintain existing Python codebase for core hypervisor functionality
- **Visualization Layer**: Implement Love2D/Lua as a separate visualization client
- **Communication Bridge**: Establish real-time data exchange between Python backend and Lua frontend

### Communication Protocol
- **Inter-Process Communication (IPC)**: Use named pipes, sockets, or shared memory
- **Data Format**: JSON or MessagePack for structured data exchange
- **Update Frequency**: Real-time updates (30-60 FPS) for smooth cellular animations
- **Bidirectional Communication**: Allow Lua frontend to send commands back to Python backend

## Cellular Process Visualization Requirements

### Core Biological Processes to Visualize

#### 1. **DNA Transcription**
- **Visual Elements**: DNA double helix, RNA polymerase movement, mRNA synthesis
- **Real-time Data**: Gene expression levels, transcription rates, active genes
- **Interactive Features**: Zoom into specific genes, highlight essential vs non-essential
- **Scientific Accuracy**: Show actual gene sequences from loaded bacterial genomes

#### 2. **Protein Translation** 
- **Visual Elements**: Ribosomes, mRNA, tRNA, growing protein chains
- **Real-time Data**: Ribosome allocation per VM, translation efficiency, protein production rates
- **Interactive Features**: Follow specific proteins from synthesis to function
- **Resource Tracking**: Show ribosome scheduling and competition between VMs

#### 3. **ATP Energy Metabolism**
- **Visual Elements**: ATP molecules, energy gradients, metabolic pathways
- **Real-time Data**: ATP levels per VM, energy consumption patterns
- **Interactive Features**: Trace energy flow through cellular processes
- **Dynamic Updates**: Show ATP depletion and regeneration cycles

#### 4. **Cellular Resource Competition**
- **Visual Elements**: Resource pools (ribosomes, ATP, enzymes), allocation flows
- **Real-time Data**: Resource utilization per VM, scheduling decisions
- **Interactive Features**: Adjust resource allocation, observe impact on VM performance
- **Hypervisor Visualization**: Show scheduling algorithms in action

#### 5. **VM Isolation Mechanisms**
- **Visual Elements**: Genetic barriers, protein tags, compartmentalization
- **Real-time Data**: Isolation effectiveness, crosstalk prevention
- **Interactive Features**: Toggle isolation systems, observe interference
- **Educational Value**: Demonstrate synthetic biology containment strategies

### Visual Design Requirements

#### **Scientific Accuracy**
- **Molecular Scale**: Accurate relative sizes and shapes of biological molecules
- **Process Dynamics**: Realistic timing and mechanics of cellular processes
- **Color Coding**: Consistent, intuitive color schemes for different molecule types
- **Educational Labels**: Clear identification of molecular components and processes

#### **User Experience**
- **Multi-Scale Views**: Zoom from cellular overview to molecular detail
- **Real-time Performance**: Smooth animations without impacting Python backend
- **Interactive Controls**: Pan, zoom, select, pause, step-through capabilities
- **Information Overlays**: Contextual information panels and tooltips

#### **Aesthetic Appeal**
- **Modern Graphics**: High-quality 2D graphics with particle effects
- **Smooth Animations**: Fluid molecular movements and process transitions
- **Visual Hierarchy**: Clear focus on important processes, subtle background elements
- **Customizable Views**: Multiple visualization modes for different use cases

## Implementation Strategy

### Phase 1: Communication Infrastructure
- **Python Data Export**: Modify existing BioXen to export VM state data
- **Lua Data Import**: Create Love2D client that receives and processes Python data
- **Protocol Definition**: Establish standardized message formats for cellular data
- **Performance Testing**: Ensure minimal impact on existing Python performance

### Phase 2: Basic Cellular Visualization
- **Static Cellular Layout**: Create 2D cellular environment with organelles and structures
- **VM Compartments**: Visual representation of different VMs within the cell
- **Basic Molecular Graphics**: Simple representations of DNA, RNA, proteins, ATP
- **Real-time Updates**: Connect visualizations to live Python data streams

### Phase 3: Interactive Process Animation
- **Gene Expression Flows**: Animated transcription and translation processes
- **Resource Competition**: Visual representation of scheduling and resource allocation
- **User Interaction**: Click-to-inspect, zoom controls, process highlighting
- **Educational Overlays**: Information panels explaining biological processes

### Phase 4: Advanced Features
- **Multi-VM Comparison**: Side-by-side visualization of different bacterial genomes
- **Historical Tracking**: Time-series visualization of cellular process evolution
- **Performance Metrics**: Real-time monitoring of hypervisor efficiency
- **Export Capabilities**: Save visualizations and data for research/education

## Technical Specifications

### Love2D/Lua Requirements
- **Love2D Version**: 11.x or later for modern graphics capabilities
- **Performance Target**: 60 FPS with multiple VMs active
- **Memory Management**: Efficient handling of large molecular datasets
- **Cross-Platform**: Support for Windows, macOS, Linux deployment

### Python Integration
- **Minimal Backend Changes**: Preserve existing BioXen architecture
- **Data Streaming**: Efficient export of VM state without performance degradation
- **Configuration Integration**: Use existing BioXen configuration systems
- **Error Handling**: Graceful degradation if visualization client unavailable

### Data Exchange Format
```json
{
  "timestamp": 1234567890,
  "vms": {
    "vm_syn3a": {
      "state": "running",
      "active_genes": ["dnaA", "rpoA", "atpA"],
      "ribosome_usage": 18,
      "atp_level": 85.2,
      "protein_synthesis_rate": 42.1
    }
  },
  "chassis": {
    "available_ribosomes": 62,
    "total_atp": 1000,
    "metabolic_activity": 0.73
  }
}
```

## Success Metrics

### Technical Performance
- **Rendering Performance**: Maintain >30 FPS with 4 active VMs
- **Memory Usage**: <500MB total for visualization client
- **Backend Impact**: <5% performance overhead on existing Python code
- **Startup Time**: Visualization ready within 10 seconds of Python backend

### Educational Value
- **Scientific Accuracy**: Peer review by computational biology experts
- **User Engagement**: Intuitive interface requiring minimal training
- **Learning Outcomes**: Demonstrable improvement in understanding of cellular processes
- **Research Utility**: Useful for actual synthetic biology research and education

### User Experience
- **Responsiveness**: Real-time updates reflect Python backend changes immediately
- **Stability**: Handle VM creation/destruction without crashes
- **Accessibility**: Clear visual indicators and optional text descriptions
- **Customization**: User-configurable visualization preferences and layouts

## Future Considerations

### Extensibility
- **Plugin Architecture**: Allow custom visualization modules for new cellular processes
- **Data Export**: Integration with scientific visualization tools (matplotlib, plotly)
- **VR/AR Support**: Potential future extension to immersive visualization
- **Web Deployment**: Possible Love2D to web compilation for browser-based access

### Scientific Applications
- **Research Integration**: Tools for computational biology researchers
- **Educational Deployment**: Classroom and laboratory teaching applications
- **Publication Quality**: Generate figures suitable for scientific papers
- **Collaboration Features**: Multi-user visualization sessions for research teams

This specification provides a comprehensive framework for adding sophisticated cellular process visualization to BioXen while maintaining the existing Python architecture and adding significant educational and research value through Love2D-powered interactive graphics.

# BioXen MVP Cellular Process Visualizer

## Minimum Viable Prototype Requirements

### Core Objective
Create a simple Love2D visualization that shows **basic cellular activity inside VMs** with minimal but engaging visuals. Focus on getting the Python-to-Lua pipeline working with one compelling cellular process.

## MVP Scope (Phase 1 Only)

### Single Process Focus: **Gene Expression**
- **Visual**: Simple DNA strand with moving "transcription bubble"
- **Data**: Active gene count per VM from Python backend
- **Animation**: RNA polymerase dots moving along DNA, producing mRNA particles
- **Interaction**: Click VM to see which genes are "active"

### Minimal VM Representation
- **Layout**: 2-4 rectangular boxes representing VMs in a simple grid
- **Labels**: VM ID, genome type (syn3A, pneumoniae, etc.)
- **Status Colors**: Green=running, Yellow=paused, Red=stopped, Gray=created
- **Activity Indicator**: Particle density shows "metabolic activity"

### Basic Python Integration
- **Communication**: Simple file-based exchange (JSON file Python writes, Lua reads)
- **Update Frequency**: 1-2 updates per second (not real-time)
- **Data Format**: Minimal VM status + gene activity counts
- **Fallback**: Static demo data if Python not running

## Technical Implementation

### Love2D Components
```lua
-- Core visual elements needed:
- VM boxes with labels
- Simple DNA helix graphics (just parallel lines)
- Moving particles for RNA polymerase
- Basic particle system for "cellular activity"
- Simple UI text overlays
```

### Python Data Export
```python
# Add to existing BioXen hypervisor:
def export_visualization_data():
    return {
        "timestamp": time.time(),
        "vms": {
            vm_id: {
                "state": vm.state.value,
                "genome": vm.genome_template,
                "active_genes": random.randint(10, 50),  # Placeholder
                "activity_level": random.uniform(0.2, 1.0)
            }
            for vm_id, vm in self.vms.items()
        }
    }
```

### File-Based Communication
- **Python writes**: `visualization_data.json` every 1-2 seconds
- **Love2D reads**: Check file modification time, reload when changed
- **Error handling**: Use default/demo data if file missing or corrupt

## Visual Design (Minimal)

### VM Layout
```
┌─────────────┐  ┌─────────────┐
│   VM_SYN3A  │  │ VM_PNEUMO   │
│   ●●●●○○○○  │  │  ●●●●●●●○   │ 
│   Running   │  │   Running   │
└─────────────┘  └─────────────┘

┌─────────────┐  ┌─────────────┐
│   VM_TEST   │  │  (unused)   │
│   ○○○○○○○○  │  │             │
│   Paused    │  │             │
└─────────────┘  └─────────────┘
```

### Gene Expression Animation
- **DNA**: Two parallel lines across each VM box
- **Activity**: Small dots moving along DNA lines
- **Speed**: Proportional to `active_genes` count
- **Color**: Different colors for different VMs

### Particle Effects
- **Simple**: Basic Love2D particle system
- **Purpose**: Show "metabolic activity" as floating dots
- **Density**: More particles = higher activity level
- **Colors**: Match VM color scheme

## Development Steps

### Step 1: Love2D Standalone (1-2 days)
- Create basic Love2D app with demo data
- Draw VM boxes, labels, basic animations
- Implement simple particle system
- Test visual appeal and performance

### Step 2: Python Integration (1 day)
- Add JSON export function to BioXen
- Test file-based communication
- Handle missing/corrupt data gracefully

### Step 3: Polish (1 day)
- Smooth animations and transitions
- Basic click interaction (show VM details)
- Simple on-screen instructions
- Performance optimization

## Success Criteria

### Functional Requirements
- ✅ Shows 2-4 VM boxes with current status
- ✅ Animated particles represent cellular activity
- ✅ Updates automatically when Python data changes
- ✅ Runs independently with demo data if Python unavailable

### Visual Quality
- ✅ Smooth 60 FPS animation
- ✅ Clear, readable labels and status indicators
- ✅ Engaging but not distracting particle effects
- ✅ Intuitive color coding and layout

### Technical Performance
- ✅ <50MB memory usage
- ✅ <5 second startup time
- ✅ Graceful handling of missing/corrupted data
- ✅ No crashes during normal operation

## Deliverables

### Love2D Application
- **Single executable**: Self-contained Love2D app
- **Demo mode**: Works without Python backend
- **Config file**: Simple settings for visualization preferences

### Python Integration
- **Single function**: `export_visualization_data()` in hypervisor
- **JSON file**: Standardized data format
- **Documentation**: How to enable visualization export

### User Documentation
- **Setup guide**: How to run visualization alongside BioXen
- **Controls**: Basic interaction instructions
- **Troubleshooting**: Common issues and solutions

## Future Extension Points

### Easy Additions (for later phases)
- **More processes**: Add ribosome animation, ATP flow
- **Better graphics**: Replace simple particles with molecular sprites
- **Real-time updates**: Switch from file-based to socket communication
- **User controls**: Pause, speed up, zoom into specific VMs

### Architecture Considerations
- **Modular design**: Easy to add new visualization types
- **Data structure**: Extensible JSON format for additional cellular data
- **Performance hooks**: Ready for optimization when adding complexity

This MVP focuses on **proving the concept** with minimal complexity while creating something visually engaging that demonstrates the cellular activity inside BioXen's VMs. The goal is to validate the Python-Love2D integration approach and create a foundation for more sophisticated visualizations later.

# BioXen MVP Visualizer with MP4 Export

## Video Recording Requirements

### Core Video Export Features
- **Real-time Recording**: Capture Love2D visualization as it runs
- **MP4 Output**: Standard format compatible with presentations, research papers
- **Quality Options**: Configurable resolution and frame rate
- **Duration Control**: Record specific time periods or full sessions
- **Automation**: Start/stop recording via Python commands or Love2D hotkeys

## Technical Implementation Options

### Option 1: Love2D Built-in Canvas Recording
```lua
-- Love2D approach using canvas and external tool
local canvas = love.graphics.newCanvas(1920, 1080)
local frameCount = 0
local recording = false

function love.draw()
    if recording then
        love.graphics.setCanvas(canvas)
        -- Draw all visualization content
        drawVMs()
        drawParticles()
        love.graphics.setCanvas()
        
        -- Save frame as PNG
        canvas:newImageData():encode("png", "frames/frame_" .. string.format("%06d", frameCount) .. ".png")
        frameCount = frameCount + 1
    end
end
```

### Option 2: External Screen Recording Integration
- **FFmpeg integration**: Launch FFmpeg from Love2D to record window
- **OBS integration**: Automated OBS recording via command line
- **System calls**: Platform-specific screen recording tools

### Option 3: Python-Controlled Recording
```python
# Python backend controls recording
def start_visualization_recording(duration_seconds=60):
    export_data = {
        "command": "start_recording",
        "duration": duration_seconds,
        "output_file": f"bioxen_viz_{timestamp}.mp4"
    }
    with open("visualization_commands.json", "w") as f:
        json.dump(export_data, f)
```

## Recommended Approach: FFmpeg Integration

### Love2D Implementation
```lua
-- Recording state management
local recording = {
    active = false,
    ffmpeg_process = nil,
    output_file = "",
    start_time = 0
}

function startRecording(filename, duration)
    -- Launch FFmpeg to record Love2D window
    local cmd = string.format(
        'ffmpeg -f x11grab -s 1280x720 -r 30 -i :0.0+100,100 -t %d -c:v libx264 -preset fast %s',
        duration, filename
    )
    recording.ffmpeg_process = io.popen(cmd)
    recording.active = true
    recording.output_file = filename
end
```

### Python Integration
```python
# Add to BioXen hypervisor
def record_visualization(duration=30, filename=None):
    if not filename:
        filename = f"bioxen_cellular_activity_{int(time.time())}.mp4"
    
    command = {
        "action": "start_recording",
        "duration": duration,
        "filename": filename,
        "timestamp": time.time()
    }
    
    with open("visualization_commands.json", "w") as f:
        json.dump(command, f)
    
    return filename
```

## Video Export Features

### Recording Controls
- **Hotkeys**: F9 to start/stop recording, F10 for screenshot
- **Python API**: `hypervisor.record_visualization(duration=60)`
- **Automatic**: Start recording when VM state changes occur
- **Scheduled**: Record at specific intervals for time-lapse

### Output Options
```json
{
    "recording_settings": {
        "resolution": "1280x720",
        "framerate": 30,
        "quality": "high",
        "format": "mp4",
        "duration": 60,
        "auto_timestamp": true
    }
}
```

### Video Content Enhancements
- **Timestamp Overlay**: Show simulation time in video
- **VM Status Overlay**: Current VM states and resource usage
- **Process Labels**: Text annotations explaining cellular processes
- **Watermark**: BioXen logo and version info

## Use Cases for Video Export

### Research Applications
```python
# Record specific experimental conditions
hypervisor.create_vm("test_vm", "syn3a")
hypervisor.start_vm("test_vm")

# Record the VM boot and stabilization process
video_file = hypervisor.record_visualization(
    duration=120,  # 2 minutes
    filename="syn3a_boot_sequence.mp4"
)
```

### Educational Content
- **Lecture Materials**: Generate videos showing cellular processes
- **Student Demonstrations**: Record different bacterial genome behaviors
- **Time-lapse**: Speed up long cellular processes for teaching
- **Comparison Videos**: Side-by-side VM behavior differences

### Documentation
- **Software Demos**: Show BioXen capabilities for presentations
- **Bug Reports**: Record unexpected behavior for debugging
- **Progress Updates**: Document development milestones
- **Publication Figures**: Generate supplementary video materials

## Implementation Steps

### Step 1: Basic Recording (FFmpeg)
- Add FFmpeg dependency check to Love2D startup
- Implement window recording with fixed duration
- Test MP4 output quality and file size
- Add basic recording status indicators

### Step 2: Python Integration
- Add recording commands to visualization data exchange
- Implement automatic recording triggers
- Add recording status feedback to Python
- Test full pipeline: Python → Love2D → MP4

### Step 3: Quality and Controls
- Add resolution and quality options
- Implement recording hotkeys and UI
- Add timestamp and annotation overlays
- Optimize file size and performance

### Step 4: Advanced Features
- Screenshot capture functionality
- Batch recording for multiple scenarios
- Time-lapse and speed control options
- Integration with BioXen test suite for automated video generation

## Technical Specifications

### Dependencies
- **FFmpeg**: Required for video encoding
- **Love2D 11.x**: Canvas and file I/O support
- **Cross-platform**: Windows (GDI), macOS (AVFoundation), Linux (X11)

### Performance Considerations
- **Recording overhead**: ~10-20% performance impact during recording
- **File size**: ~10-50MB per minute depending on activity and quality
- **Memory usage**: Additional ~100MB for frame buffering
- **Storage**: Automatic cleanup of old recordings

### Output Specifications
```
Video Format: MP4 (H.264)
Resolution: 1280x720 (configurable)
Frame Rate: 30 FPS
Audio: None (cellular processes are silent!)
Duration: 30 seconds to 10 minutes
File Size: ~5-25MB per minute
```

## Success Criteria

### Functional Requirements
- ✅ Record Love2D visualization to MP4 file
- ✅ Start/stop recording from Python or Love2D
- ✅ Configurable duration and quality settings
- ✅ Automatic file naming with timestamps

### Quality Requirements
- ✅ Smooth 30 FPS recording without frame drops
- ✅ Clear, readable text and animations in video
- ✅ Reasonable file sizes (<50MB for 2-minute videos)
- ✅ Compatible with standard video players

### Integration Requirements
- ✅ Works alongside existing Python visualization pipeline
- ✅ No impact on BioXen performance when not recording
- ✅ Graceful fallback if FFmpeg not available
- ✅ Cross-platform compatibility (Windows, macOS, Linux)

This video recording capability transforms the BioXen visualizer from a real-time demonstration tool into a content creation platform for research, education, and documentation purposes.