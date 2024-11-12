import numpy as np
import matplotlib.pyplot as plt

def plot(method: str, tuples):
    plt.title(f"Dimensionality Reduction with {method}")
    plt.rcParams['figure.dpi'] = 300
    x, y = zip(*tuples)
    plt.scatter(x, y)
    plt.show()