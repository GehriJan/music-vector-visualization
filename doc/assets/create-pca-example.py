import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from sklearn.decomposition import PCA

# Generate random data with denser points in the middle
np.random.seed(0)
n_points = 100
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 20}
matplotlib.rc('font', **font)
# Clustered points with more density near the center
x = np.concatenate(
    [
        np.random.normal(scale=1, size=n_points // 2),
        np.random.normal(scale=3, size=n_points // 2),
    ]
)
y = 0.5 * x + np.random.normal(scale=1, size=n_points)
data = np.vstack((x, y)).T

# Apply PCA
pca = PCA(n_components=2)
pca.fit(data)
data_pca = pca.transform(data)

# Get the principal components
mean = pca.mean_
components = pca.components_

# Plot the original data
plt.figure(figsize=(10, 8))
plt.scatter(data[:, 0], data[:, 1], alpha=0.5, color="blue", label="Originale Daten")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.title("PCA illustratives Beispiel", pad=25)

# Plot the principal components as lines with labels
for i, (length, vector) in enumerate(zip(pca.explained_variance_, components)):
    v = vector * 3 * np.sqrt(length)  # Scale for visualization
    plt.plot(
        [mean[0], 0.7 * (mean[0] + v[0])],
        [mean[1], 0.7 * (mean[1] + v[1])],
        color="red",
        linewidth=2,
    )
    plt.arrow(
        mean[0],
        mean[1],
        0.7*v[0],
        0.7*v[1],
        color="red",
        width=0.05,
        head_width=0.3,
        head_length=0.3,
    )

    # Add text label for each principal component
    plt.text(
        mean[0] + v[0] * 0.85,
        mean[1] + v[1] * 0.85,
        f"PC{i + 1}",
        color="red",
        fontsize=20,
        ha="center",
        va="center",
        fontweight="bold",
    )

# Legend and plot adjustments
plt.axhline(0, color="grey", lw=0.5)
plt.axvline(0, color="grey", lw=0.5)
plt.legend(loc="upper left")
plt.grid(True)

plt.show()
