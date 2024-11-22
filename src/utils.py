import numpy as np
import argparse
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA, KernelPCA, SparsePCA, IncrementalPCA, FastICA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

methodDict = {
    "pca": ["PCA", PCA(2)],
    "tsne": ["t-SNE", TSNE(2)],
    "kernelpca": ["KernelPCA", KernelPCA(2)],
    "sparsepca": ["SparsePCA", SparsePCA(2)],
    "incrementalpca":["IncrementalPCA", IncrementalPCA(2)],
    "fastica": ["FastICA", FastICA(2)],
}

# normalize vectors (as numpy arrays)
def normalize(vectors):
    vectors = vectors / vectors.max(axis=0)
    vectors = np.abs(vectors)
    return vectors

# prepare data for visualization
def getDataframe(labels, outputVectors: np.ndarray):
    x_coords =list(map(lambda coord: coord[0], outputVectors))
    y_coords =list(map(lambda coord: coord[1], outputVectors))
    dataframe = labels.copy().assign(x=x_coords,y=y_coords)
    return dataframe

# process commandline options
def getOptions():
    parser = argparse.ArgumentParser()
    arguments = [
        ["-g", "--genres"],
        ["-m", "--methods", ],
    ]
    for argument in arguments:
        parser.add_argument(
            argument[0],
            argument[1],
            required=True,
            type=str,
            nargs="+"
        )
    args = parser.parse_args()
    argsDict = vars(args)
    genres = argsDict["genres"]
    methods = argsDict["methods"]

    # Raise exception when false method is given
    for method in methods:
        if not method in methodDict.keys():
            raise Exception(f"Sorry, {method} is not a supported method.")

    return genres, methods