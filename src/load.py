import csv

def get_insert_statement(path: str):
    output: str = "INSERT INTO songs (name, artist, genre, embedding)\nVALUES"
    with open(path, mode="r") as file:
        csvFile = csv.reader(file)
        csvData = list(csvFile)[1:]
        for line in csvData:
            vector = line[8:19]
            vector = vector.__repr__().replace("'", "").replace(" ", "")
            track_name = line[4].replace("'", "")
            artist_names = line[2].replace("'", "")
            genre_name = line[len(line) - 1]
            output += f"\n('{track_name}','{artist_names}','{genre_name}','{vector}'),"
    return output[:len(output)-1]
