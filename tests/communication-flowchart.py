import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 8))

# Define positions for components (x, y coordinates)
positions = {
    'Cellular VM\n(circuits.py)': (0.2, 0.8),
    'Redis Stream\n(olfi_stream)': (0.5, 0.7),
    'Lua VM 1\n(ol_fi_visualizer.lua)': (0.8, 0.8),
    'Lua VM 2\n(ol_fi_visualizer.lua)': (0.8, 0.4),
    'GabbyLua\n(main.lua)': (0.65, 0.6)
}

# Colors for components
colors = {
    'Cellular VM\n(circuits.py)': '#FF6B6B',
    'Redis Stream\n(olfi_stream)': '#4ECDC4',
    'Lua VM 1\n(ol_fi_visualizer.lua)': '#45B7D1',
    'Lua VM 2\n(ol_fi_visualizer.lua)': '#96CEB4',
    'GabbyLua\n(main.lua)': '#FFEAA7'
}

# Draw rectangles for components
for label, (x, y) in positions.items():
    ax.add_patch(patches.FancyBboxPatch(
        (x - 0.1, y - 0.05), 0.2, 0.1,
        boxstyle="round,pad=0.02", facecolor=colors[label], edgecolor='black'
    ))
    ax.text(x, y, label, ha='center', va='center', fontsize=10, wrap=True)

# Draw arrows for data flow
arrows = [
    (('Cellular VM\n(circuits.py)', 'Redis Stream\n(olfi_stream)'), 'Push MVOC\n& Ol-Fi Frame', (0.3, 0.75, 0.4, 0.7)),
    (('Redis Stream\n(olfi_stream)', 'Lua VM 1\n(ol_fi_visualizer.lua)'), 'Read MVOC\n& Frame', (0.6, 0.7, 0.7, 0.75)),
    (('Redis Stream\n(olfi_stream)', 'Lua VM 2\n(ol_fi_visualizer.lua)'), 'Read MVOC\n& Frame', (0.6, 0.65, 0.7, 0.45)),
    (('Lua VM 1\n(ol_fi_visualizer.lua)', 'GabbyLua\n(main.lua)'), 'Send Ol-Fi\nFrame (TCP)', (0.75, 0.75, 0.7, 0.65)),
    (('Lua VM 2\n(ol_fi_visualizer.lua)', 'GabbyLua\n(main.lua)'), 'Receive Ol-Fi\nFrame (TCP)', (0.75, 0.45, 0.7, 0.55)),
    (('Lua VM 1\n(ol_fi_visualizer.lua)', 'Lua VM 2\n(ol_fi_visualizer.lua)'), 'UDP Peer\nDiscovery', (0.8, 0.7, 0.8, 0.5))
]

for (start, end), label, (x1, y1, x2, y2) in arrows:
    ax.add_patch(patches.FancyArrowPatch(
        (positions[start][0], positions[start][1]),
        (positions[end][0], positions[end][1]),
        connectionstyle="arc3,rad=0.2", arrowstyle="->", color='black'
    ))
    ax.text((x1 + x2) / 2, (y1 + y2) / 2, label, ha='center', va='center', fontsize=8)

# Set limits and hide axes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Save diagram
plt.savefig('diagrams/lua_ol_fi_gabby_communication.png', dpi=300, bbox_inches='tight')
plt.close()
print("Diagram saved to diagrams/lua_ol_fi_gabby_communication.png")