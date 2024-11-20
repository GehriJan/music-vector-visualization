import numpy as np

def normalize(vectors):
    vectors = vectors / vectors.max(axis=0)
    vectors = np.abs(vectors)
    return vectors


def getDataframe(labels, outputVectors: np.ndarray):
    x_coords =list(map(lambda coord: coord[0], outputVectors))
    y_coords =list(map(lambda coord: coord[1], outputVectors))
    dataframe = labels.copy().assign(x=x_coords,y=y_coords)
    return dataframe