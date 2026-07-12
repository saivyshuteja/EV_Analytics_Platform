from pathlib import Path

import pandas as pd


DATASET_PATH = Path(__file__).resolve().parent / "backend" / "data" / "raw" / "ev_data.csv"


df = pd.read_csv(DATASET_PATH)
print(df.shape)
