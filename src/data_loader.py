import pandas as pd
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt


def load_data(path):
    ext = Path(path).suffix.lower()

    if ext == ".csv":
        return pd.read_csv(path)

    elif ext == ".txt":
        return pd.read_csv(path, sep=",")  # или sep=",", если это текст с запятыми

    else:
        raise ValueError("Неподдерживаемый формат")

df = load_data("data/raw/nq_rth_30.txt")


df["datetime"] = pd.to_datetime(
    df["Date"] + " " + df["Time"],
    format="%m/%d/%Y %H:%M:%S"
    )
df.sort_values("datetime")

df = df[
    ["datetime",
     "Open",
     "High",
     "Low",
     "Close",
     "Volume"
    ]
]

df["date"] = df["datetime"].dt.date

df["time"] = df["datetime"].dt.time

opening = df[
    (df["datetime"].dt.time >= pd.to_datetime("15:30").time())
    &
    (df["datetime"].dt.time < pd.to_datetime("16:00").time())
]

opening_range = opening.groupby("date").agg(
    OR_high=("High", "max"),
    OR_low=("Low", "min"),
    OR_volume=("Volume", "sum")
)

opening_range["OR_size"] = (
    opening_range["OR_high"] -
    opening_range["OR_low"]
)

print(df[df["date"] == df["date"].iloc[0]].head(20))

print(opening_range.head())

print(df["datetime"].dt.time.min())
print(df["datetime"].dt.time.max())

print(df["datetime"].dt.date.nunique())