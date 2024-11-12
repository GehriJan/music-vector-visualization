import csv
def get_songs_from_csv(path: str):
    output: list = []
    with open(path, mode="r") as file:
        csvFile = csv.reader(file)
        csvData = list(csvFile)[1:]
        for line in csvData:
            vector = line[8:19]
            track_name = line[4]
            artist_names = line[2]
            track_id = line[1]
            genre_name = line[len(line)-1]
            #output+= f"\n('{track_name}','{artist_names}','{genre_name}','{vector}'),"
            output.append({"track_id": track_id, "track_name": track_name, "artist_names": artist_names, "genre_name": genre_name, "embedding": vector})
    return output