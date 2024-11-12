import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

print("hello world")
X = np.array([[-1, -1, 3, 4], [-2, -1, 3, -2], [-3, -2, 0, 1], [1, 1, -2, -4], [2, 1, 2, 1], [3, 2, 0, 4]])
pca = PCA(2)
tsne = TSNE(2)
Y_pca = pca.fit_transform(X)
Y_tsne = tsne.fit_transform(X)

print(Y_pca)
print(Y_tsne)
plot("PCA", Y_pca)
plot("t-SNE", Y_tsne)
