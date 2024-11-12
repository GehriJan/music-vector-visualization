import numpy as np
import plotly.express as px
#def plot(method: str, tuples):
#    plt.title(f"Dimensionality Reduction with {method}")
#    plt.rcParams['figure.dpi'] = 3000
#    x, y = zip(*tuples)
#    plt.scatter(x, y)
#    plt.show()

def plot(method: str, coords: np.ndarray) -> None:
    X = list(map(lambda coord: coord[0], coords))
    Y = list(map(lambda coord: coord[1], coords))
   
    fig = px.scatter(X, Y)
    fig.show()
