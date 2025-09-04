import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure and axis
fig, ax = plt.subplots(figsize=(14, 10))

# Define positions for components
positions = {
    'Cellular VM\n(circuits.py)': (0.25, 0.85),
    'Redis Stream\n(olfi_stream)': (0.5, 0.7),
    'Lua VM 1\n(ol_fi_visualizer.lua)': (0.85, 0.85),
    'Ol-Fi Modem 1\n(ol_fi_visualizer.lua)': (0.85, 0.75),
    'Lua VM 2\n(ol_fi_visualizer.lua)': (0.85, 0.45),
    'Ol-Fi Modem 2\n(ol_fi_visualizer.lua)': (0.85, 0.35),
    'GabbyLua\n(main.lua)': (0.65, 0.55)
}

# Colors for components
colors = {
    'Cellular VM\n(circuits.py)': '#FF6B6B',
    'Redis Stream\n(olfi_stream)': '#4ECDC4',
    'Lua VM 1\n(ol_fi_visualizer.lua)': '#45B7D1',
    'Ol-Fi Modem 1\n(ol_fi_visualizer.lua)': '#96CEB4',
    'Lua VM 2\n(ol_fi_visualizer.lua)': '#45B7D1',
    'Ol-Fi Modem 2\n(ol_fi_visualizer.lua)': '#96CEB4',
    'GabbyLua\n(main.lua)': '#FFEAA7'
}

# Draw rectangles for components
for label, (x, y) in positions.items():
    width, height = 0.25, 0.1
    if 'Lua VM' in label:
        ax.add_patch(patches.FancyBboxPatch(
            (x - 0.15, y - 0.15), 0.3, 0.3,
            boxstyle="round,pad=0.02", facecolor=colors[label], edgecolor='black', alpha=0.3
        ))
    ax.add_patch(patches.FancyBboxPatch(
        (x - 0.1, y - 0.05), width, height,
        boxstyle="round,pad=0.02", facecolor=colors[label], edgecolor='black'
    ))
    ax.text(x, y, label, ha='center', va='center', fontsize=10, wrap=True)

# Draw arrows for data flow with detailed labels
arrows = [
    (
        ('Cellular VM\n(circuits.py)', 'Redis Stream\n(olfi_stream)'),
        'Push MVOC & Ol-Fi Frame\n(OlFiNetworkCircuit, redis-py)',
        (0.35, 0.8, 0.4, 0.7)
    ),
    (
        ('Redis Stream\n(olfi_stream)', 'Ol-Fi Modem 1\n(ol_fi_visualizer.lua)'),
        'Read MVOC & Frame\n(lua-redis)',
        (0.6, 0.7, 0.75, 0.75)
    ),
    (
        ('Redis Stream\n(olfi_stream)', 'Ol-Fi Modem 2\n(ol_fi_visualizer.lua)'),
        'Read MVOC & Frame\n(lua-redis)',
        (0.6, 0.65, 0.75, 0.35)
    ),
    (
        ('Ol-Fi Modem 1\n(ol_fi_visualizer.lua)', 'GabbyLua\n(main.lua)'),
        'Encode & Send Ol-Fi Frame\n(TCP, luasocket, lua-cjson)',
        (0.75, 0.7, 0.7, 0.6)
    ),
    (
        ('Ol-Fi Modem 2\n(ol_fi_visualizer.lua)', 'GabbyLua\n(main.lua)'),
        'Receive & Decode Ol-Fi Frame\n(TCP, luasocket, lua-cjson)',
        (0.75, 0.4, 0.7, 0.5)
    ),
    (
        ('Ol-Fi Modem 1\n(ol_fi_visualizer.lua)', 'Ol-Fi Modem 2\n(ol_fi_visualizer.lua)'),
        'UDP Peer Discovery\n(discovery_service.lua)',
        (0.85, 0.65, 0.85, 0.45)
    ),
    (
        ('Lua VM 1\n(ol_fi_visualizer.lua)', 'Ol-Fi Modem 1\n(ol_fi_visualizer.lua)'),
        'Visualize Frame\n(Love2D)',
        (0.85, 0.8, 0.85, 0.75)
    ),
    (
        ('Lua VM 2\n(ol_fi_visualizer.lua)', 'Ol-Fi Modem 2\n(ol_fi_visualizer.lua)'),
        'Visualize Frame\n(Love2D)',
        (0.85, 0.4, 0.85, 0.35)
    )
]

for (start, end), label, (x1, y1, x2, y2) in arrows:
    ax.add_patch(patches.FancyArrowPatch(
        (positions[start][0], positions[start][1]),
        (positions[end][0], positions[end][1]),
        connectionstyle="arc3,rad=0.2", arrowstyle="->", color='black', linewidth=1.5
    ))
    ax.text((x1 + x2) / 2, (y1 + y2) / 2, label, ha='center', va='center', fontsize=9, wrap=True)

# Add title and annotations
plt.title('BioXen-jcvi: Lua VM Communication with Ol-Fi Modems via GabbyLua', fontsize=14, pad=20)
ax.text(0.5, 0.95, 'Data Flow: MVOC & Ol-Fi Frames (preamble, payload, checksum)', 
        ha='center', va='center', fontsize=10, color='darkblue')

# Set limits and hide axes
ax.set_xlim(0, 1.1)
ax.set_ylim(0, 1)
ax.axis('off')

# Save diagram
plt.savefig('diagrams/lua_ol_fi_gabby_modem_communication.png', dpi=300, bbox_inches='tight')
plt.close()
print("Diagram saved to diagrams/lua_ol_fi_gabby_modem_communication.png")