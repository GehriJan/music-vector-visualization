from db import DB
from plot import plot
from utils import normalize, getDataframe
from utils import getOptions, methodDict

# Get command line options
genreArgs, methodArgs = getOptions()

# Setup Database
db = DB()

# Insert data from csv to database
db.insertCSVtoDB("data/train.csv")

# get songs from requested genres
vectors, labels = db.selectSongs(genreArgs)

# Normalize Vectors
vectors = normalize(vectors)

for method in methodArgs:
    func = methodDict[method][1]
    name = methodDict[method][0]
    # Perform dimensionality reduction
    output = func.fit_transform(vectors)

    # Plot
    dataframe = getDataframe(labels, output)
    plot(name, dataframe)

# Give statistic
print(f"% Stats\n% Number of Genres: {len(genreArgs)}\n% Number of Songs: {len(vectors)}")