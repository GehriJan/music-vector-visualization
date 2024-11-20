from db import DB
from plot import plot
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from utils import normalize, getDataframe


# Execute db operations
db = DB()
db.insertCSVtoDB("data/train.csv")
genreConfigs = {
    "config1": ["sad", "sleep", "piano", "dubstep"],
    "config2": ["electronic", "acoustic", "opera", "k-pop"],
    "config3": ["iranian", "brazil", "german", "british"],
}
genres = genreConfigs["config3"]
vectors, labels = db.selectSongs(["metal", "sleep", "classical", "dubstep"])
vectors = normalize(vectors)

# Setup PCA and t-SNE functions
pca = PCA(2)
tsne = TSNE(2)

# Execute functions
outputVectorsPCA = pca.fit_transform(vectors)
outputVectorsTSNE = tsne.fit_transform(vectors)

# Prepare Dataframe-datastructure for plotting
df_pca = getDataframe(labels, outputVectorsPCA)
df_tsne = getDataframe(labels, outputVectorsTSNE)

# Plot
print(f"% Stats\n% Number of Genres: {len(genres)}\n% Number of Songs: {len(vectors)}")
plot("PCA",df_pca)
plot("TSNE",df_tsne)
