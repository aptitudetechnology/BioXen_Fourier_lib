# communication-flowchart.py
#
# Below is Python code using Matplotlib to generate a clear flowchart diagram illustrating the 
# communication flow between the Cellular VM (via circuits.py), Redis Stream, and Lua VM 
# (software-defined Ol-Fi modem) in the BioXen-jcvi project for MVOC data exchange. This will
# produce a PNG file saved to the diagrams/ directory.


import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines

# Create figure and axis
fig, ax = plt.subplots(figsize=(10, 6))

# Define positions for components (x, y coordinates)
positions = {
    'Cellular VM': (0.2, 0.8),
    'OlFiNetworkCircuit': (0.2, 0.6),
    'Redis Stream': (0.5, 0.7),
    'Lua VM': (0.8, 0.8),
    'Ol-Fi Modem': (0.8, 0.6)
}

# Colors for components
colors = {
    'Cellular VM': '#FF6B6B',
    'OlFiNetworkCircuit': '#96CEB4',
    'Redis Stream': '#4ECDC4',
    'Lua VM': '#45B7D1',
    'Ol-Fi Modem': '#FFEAA7'
}

# Draw rectangles for components
for label, (x, y) in positions.items():
    ax.add_patch(patches.FancyBboxPatch(
        (x - 0.1, y - 0.05), 0.2, 0.1,
        boxstyle="round,pad=0.02", facecolor=colors[label], edgecolor='black'
    ))
    ax.text(x, y, label, ha='center', va='center', fontsize=10)

# Draw arrows for data flow
arrows = [
    (('OlFiNetworkCircuit', 'Redis Stream'), 'Send MVOC\n& Frame Data', (0.3, 0.65, 0.4, 0.7)),
    (('Redis Stream', 'Ol-Fi Modem'), 'Read MVOC\n& Frame', (0.6, 0.7, 0.7, 0.65)),
    (('Cellular VM', 'OlFiNetworkCircuit'), 'Generate MVOC', (0.2, 0.75, 0.2, 0.65)),
    (('Ol-Fi Modem', 'Lua VM'), 'Visualize Frame', (0.8, 0.65, 0.8, 0.75))
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
plt.savefig('./diagrams/ol_fi_communication_flow.png', dpi=300, bbox_inches='tight')
plt.close()
print("Diagram saved to diagrams/ol_fi_communication_flow.png")