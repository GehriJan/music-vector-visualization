from pgvector.psycopg import register_vector
from pgvector.sqlalchemy import Vector
#import psycopg
from load import get_songs_from_csv
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

from sqlalchemy import create_engine, text, Table, MetaData, Column, Integer, VARCHAR

def get_db_engine():
    return create_engine('postgresql://user:password@localhost:5432/vector')

with get_db_engine().connect() as conn:
    print(conn)
    conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
    conn.commit()
    print("created extension")
    # Create table
    conn.execute(text("DROP TABLE IF EXISTS songs"))
    conn.commit()
    print("dropd")

    m = MetaData()
    t = Table("songs", m, Column("track_id", VARCHAR),Column("track_name", VARCHAR), Column("artist_names", VARCHAR), Column("genre_name", VARCHAR), Column("embedding", Vector))
    print("created")

    # Insert data to DB
    data = get_songs_from_csv("data/train.csv")
    conn.execute(t.insert(),data)
    conn.commit()
    print("inserted")

    # Get data for dimensionality reduction
    data = conn.execute(text("SELECT * FROM songs"))
    conn.commit()
    print("im here")
    #print(data)

    # Setup PCA and t-SNE functions
    pca = PCA(2)
    tsne = TSNE(2)

