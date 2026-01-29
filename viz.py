import json
import numpy as np
import matplotlib.pyplot as plt

# Load data
with open("iteration_results_20260129_114041.json", "r") as f:
    data = json.load(f)

random_vals = np.array(data["random"])
clifford_vals = np.array(data["clifford"])

# Define common bins (important for fair comparison)
bins = np.linspace(-0.2, 1.05, 40)

plt.figure(figsize=(8, 5))

plt.hist(
    random_vals,
    bins=bins,
    alpha=0.6,
    density=True,
    label="Random",
    edgecolor="black"
)

plt.hist(
    clifford_vals,
    bins=bins,
    alpha=0.6,
    density=True,
    label="Clifford",
    edgecolor="black"
)

plt.xlabel("Estimated value")
plt.ylabel("Density")
plt.title("Estimator distribution: Clifford vs Random")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
