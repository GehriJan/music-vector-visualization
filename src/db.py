import csv
import os
from pgvector.psycopg import register_vector
import psycopg
from psycopg import sql
import numpy as np
import pandas as pd


class DB():
    def __init__(self):
        config ={
            'user': os.environ["POSTGRES_USER"],
            'dbname':os.environ["POSTGRES_DB"],
            'password':os.environ["POSTGRES_PASSWORD"],
            'host':'localhost',
            'port':'5432'
        }
        conn = psycopg.connect(**config)
        cur = conn.cursor()
        cur.execute(sql.SQL("CREATE EXTENSION IF NOT EXISTS vector"))
        register_vector(conn)

        # Create table
        cur.execute(sql.SQL("DROP TABLE IF EXISTS songs"))
        cur.execute(sql.SQL(
            "CREATE TABLE songs (\
            id bigserial PRIMARY KEY,\
            name varchar(1000),\
            artist varchar(1000),\
            genre varchar(50),\
            embedding vector(8)\
        )"))
        self.conn = conn
        self.cur = cur

    def insertCSVtoDB(self, path: str):
        insertStatement = get_insert_statement(path)
        self.cur.execute(sql.SQL(insertStatement))

    def selectSongs(self,genres: list[str]):
        genreSelection: str = str()
        for genre in genres:
            genreSelection+=f"'{genre}',"
        genreSelection = genreSelection[:len(genreSelection)-1]
        selectStatement = f"""
            SELECT *
            FROM songs
            WHERE genre in ({genreSelection})
            ORDER BY name
        """
        self.cur.execute(sql.SQL(selectStatement))
        data = self.cur.fetchall()
        vectors = getVectors(data)
        labels = pd.DataFrame({
            "name": list(map(lambda song: song[1], data)),
            "artists": list(map(lambda song: song[2], data)),
            "genre": list(map(lambda song: song[3], data))
        })
        return vectors, labels
    def getGenres(self):
        selectStatement = f"""
            SELECT DISTINCT genre
            FROM songs
            ORDER BY genre ASC
        """
        self.cur.execute(sql.SQL(selectStatement))
        data = self.cur.fetchall()
        genres = list(map(lambda genreTuple: genreTuple[0], data))
        return genres






def get_insert_statement(path: str):
    output: str = "INSERT INTO songs (name, artist, genre, embedding)\nVALUES"
    with open(path, mode="r") as file:
        csvFile = csv.reader(file)
        csvData = list(csvFile)[1:]
        for line in csvData:
            vector = line[8:10] + line[11:12] + line[13:18]
            vector = vector.__repr__().replace("'", "").replace(" ", "")
            track_name = line[4].replace("'", "")
            artist_names = line[2].replace("'", "")
            genre_name = line[len(line) - 1]
            output += f"\n('{track_name}','{artist_names}','{genre_name}','{vector}'),"
    return output[:len(output)-1]

def getVectors(data: list) -> list:
    vectors: list[list[float]] = []
    for song in data:
        vectorString: str = song[len(song)-1]
        vectorString = vectorString[1:len(vectorString)-1]
        stringList: list[str] = vectorString.split(",")
        vector: list[float] = list(map(lambda string: float(string), stringList))
        vectors.append(vector)
    return np.array(vectors)