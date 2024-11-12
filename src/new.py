import psycopg
import os
from pgvector.psycopg import register_vector
from load import get_insert_statement

conn = psycopg.connect(
    f"dbname='{os.environ["POSTGRES_DB"]}' user='{os.environ["POSTGRES_USER"]}' password='{os.environ["POSTGRES_PASSWORD"]}' host='localhost' port='5432'"
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
# Get data for dimensionality reduction
cur.execute("SELECT count(*) FROM songs")
print("im here")
data = cur.fetchall()
print(data)

# Setup PCA and t-SNE functions
#pca = PCA(2)
#tsne = TSNE(2)
