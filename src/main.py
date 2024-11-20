from db import DB
from plot import plot
from utils import normalize, getDataframe
from utils import getOptions, methodDict


genreArgs, methodArgs = getOptions()

# Execute db operations
db = DB()
db.insertCSVtoDB("data/train.csv")

genreConfigs = {
    "config1": ["sad", "sleep", "piano", "dubstep"],
    "config2": ["electronic", "acoustic", "opera", "k-pop"],
    "config3": ["iranian", "brazil", "german", "british"],
}
vectors, labels = db.selectSongs(genreArgs)
vectors = normalize(vectors)

for method in methodArgs:
    func = methodDict[method][1]
    name = methodDict[method][0]
    # perform dimensionality reduction
    output = func.fit_transform(vectors)

    # plot
    dataframe = getDataframe(labels, output)
    plot(name, dataframe)

# give statistic
print(f"% Stats\n% Number of Genres: {len(genreArgs)}\n% Number of Songs: {len(vectors)}")