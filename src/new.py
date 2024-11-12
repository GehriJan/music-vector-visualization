import psycopg
import os
from pgvector.psycopg import register_vector
from load import get_insert_statement
from plot import plot
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import numpy as np

# Setup database
conn = psycopg.connect(
    f"dbname='{os.environ["POSTGRES_DB"]}'\
    user='{os.environ["POSTGRES_USER"]}'\
    password='{os.environ["POSTGRES_PASSWORD"]}'\
    host='localhost' port='5432'"
)
cur = conn.cursor()
cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
register_vector(conn)

# Create table
cur.execute("DROP TABLE IF EXISTS songs")
cur.execute(
    "CREATE TABLE songs (\
    id bigserial PRIMARY KEY,\
    name varchar(1000),\
    artist varchar(1000),\
    genre varchar(50),\
    embedding vector(11)\
)")

# Insert data to DB
insertStatement = get_insert_statement("data/train.csv")
cur.execute(insertStatement)

# Get data for analysis
selectStatement = """
SELECT *
FROM songs
WHERE genre in ('world-music', 'afrobeat', 'alt-rock', 'hard-style')
"""
# todo: change, so that genre-selection is possible
def getVectors(data: list) -> list:
    vectors: list[list[float]] = []
    for song in data:
        vectorString: str = song[len(song)-1]
        vectorString = vectorString[1:len(vectorString)-1]
        stringList: list[str] = vectorString.split(",")
        vector: list[float] = list(map(lambda string: float(string), stringList))
        vectors.append(vector)
    return np.array(vectors)

cur.execute(selectStatement)
data = cur.fetchall()
vectors = getVectors(data)
names = list(map(lambda song: song[1], data))
artists = list(map(lambda song: song[2], data))
print(vectors)
# Setup PCA and t-SNE functions
pca = PCA(2)
tsne = TSNE(2)

# Execute functions
outputVectorsPCA = pca.fit_transform(vectors)
outputVectorsTSNE = tsne.fit_transform(vectors)

plot("",outputVectorsPCA)
plot("",outputVectorsTSNE)
