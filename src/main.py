from db import DB
from plot import plot
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd

def normalize(vectors):
    vectors = vectors / vectors.max(axis=0)
    vectors = np.abs(vectors)
    return vectors

db = DB()

db.insertCSVtoDB("data/train.csv")

genres = ["sleep", "dubstep", "funk", "german"]
vectors, labels = db.selectSongs(genres)
print(db.getGenres())
# Setup PCA and t-SNE functions
pca = PCA(2)
tsne = TSNE(2)

# Execute functions
vectors = normalize(vectors)
outputVectorsPCA = pca.fit_transform(vectors)
outputVectorsTSNE = tsne.fit_transform(vectors)
print(pca.explained_variance_)
print(pca.explained_variance_ratio_)
print(pca.singular_values_)
# Prepare Dataframe-datastructure for plotting
df_pca = labels.copy().assign(
    x=list(map(lambda coord: coord[0], outputVectorsPCA)),
    y=list(map(lambda coord: coord[1], outputVectorsPCA)),
)
df_tsne = labels.copy().assign(
    x=list(map(lambda coord: coord[0], outputVectorsTSNE)),
    y=list(map(lambda coord: coord[1], outputVectorsTSNE)),
)

print(f"% Stats\n% Number of Genres: {len(genres)}\n% Number of Songs: {len(vectors)}")
plot("PCA",df_pca)
plot("TSNE",df_tsne)
