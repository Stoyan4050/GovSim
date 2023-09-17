import numpy as np
import matplotlib.pyplot as plt

# Plot results:

TOKEN_BASED_W = []
QUAD_BASED_W = []
REP_BASED_W = []


TOKEN_BASED_REP = []
QUAD_BASED_REP = []
REP_BASED_REP = []

REP_BASED_PEN = []
QUAD_BASED_PEN = []
TOKEN_BASED_PEN = []


x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.sin(x + 1)
y3 = np.sin(x + 2)
y4 = np.sin(x + 3)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x, y1, label='Token-based voting', color='blue', linewidth=2, linestyle='-')
plt.plot(x, y2, label='Quadratic voting', color='red', linewidth=2, linestyle='--')
plt.plot(x, y4, label='Reputation voting', color='purple', linewidth=2, linestyle=':')

# Add title and labels
plt.title('Rate of change of the number of participants whithout incentive', fontsize=16)
plt.xlabel('Rate of change', fontsize=14)
plt.ylabel('Number of iterations', fontsize=14)

# Add legend
plt.legend(loc='upper right', fontsize=12)

# Add grid
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Display the plot
plt.tight_layout()
plt.show()