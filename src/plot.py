import numpy as np
import plotly.express as px
import pandas as pd

def plot(method: str, df: pd.DataFrame) -> None:
    fig = px.scatter(
        data_frame=df,
        x="x",
        y="y",
        color="genre",
        title=f"Dimensionionality Reduction with {method}",
        hover_name="name",
        hover_data=["artists", "genre"],
    )
    fig.show()
