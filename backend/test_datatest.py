from core.config import settings

print(settings.APP_NAME)


from core.logger import logger

logger.info("Application Started")

import pandas as pd

df = pd.read_csv(
    "data/raw/ev_data.csv"
)

print(df.shape)

print(df.head())
import pandas as pd

df = pd.read_parquet(
    "data/processed/processed_data.parquet"
)

print(df.head())

print(df.shape)