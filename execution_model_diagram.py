import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, ArrowStyle

# Define execution model stages
stages = [
    "Initialization",
    "Resource Allocation",
    "Signal Acquisition",
    "Lens Selection",
    "Analysis/Computation",
    "Validation",
    "Output/Reporting"
]

# Box positions (x, y)
positions = [
    (0, 6),
    (0, 5),
    (0, 4),
    (0, 3),
    (0, 2),
    (0, 1),
    (0, 0)
]

fig, ax = plt.subplots(figsize=(7, 8))
ax.set_xlim(-1, 2)
ax.set_ylim(-1, 7)
ax.axis('off')

# Draw boxes for each stage
for i, (stage, pos) in enumerate(zip(stages, positions)):
    box = FancyBboxPatch((pos[0], pos[1]), 1.8, 0.8,
                         boxstyle="round,pad=0.1", fc="#e0f7fa", ec="#00796b", lw=2)
    ax.add_patch(box)
    ax.text(pos[0]+0.9, pos[1]+0.4, stage, ha='center', va='center', fontsize=13, color="#004d40", weight='bold')
    # Draw arrow to next box
    if i < len(positions)-1:
        ax.annotate('', xy=(pos[0]+0.9, pos[1]), xytext=(pos[0]+0.9, pos[1]-0.2),
                    arrowprops=dict(arrowstyle=ArrowStyle("-|>", head_length=1.2, head_width=0.8), lw=2, color="#00796b"))

# Title and legend
plt.title("BioXen VM Execution Model - Research-Enhanced Stages", fontsize=15, color="#00695c", weight='bold', pad=20)
plt.text(0.9, -0.5, "Lens Selection: Fourier, Wavelet, Laplace, Z-Transform", ha='center', fontsize=11, color="#00796b")
plt.tight_layout()
plt.show()
