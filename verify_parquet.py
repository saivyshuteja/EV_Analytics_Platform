from pathlib import Path

import pandas as pd


PARQUET_PATH = (
    Path(__file__).resolve().parent
    / "backend"
    / "data"
    / "processed"
    / "processed_data.parquet"
)


df = pd.read_parquet(PARQUET_PATH)
print(df.head())
print(df.shape)
