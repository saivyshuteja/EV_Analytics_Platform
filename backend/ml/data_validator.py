import pandas as pd


class DataValidator:

    def __init__(self, path):

        self.path = path

    def validate(self):

        df = pd.read_csv(self.path)

        print("Rows:", df.shape[0])

        print("Columns:", df.shape[1])

        print(df.isnull().sum())

        print(df.duplicated().sum())

        return True
validator = DataValidator(
    "data/raw/ev_data.csv"
)

validator.validate()