from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler


BACKEND_DIR = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = BACKEND_DIR / "data" / "raw" / "ev_data.csv"
PROCESSED_DIR = BACKEND_DIR / "data" / "processed"
PROCESSED_DATA_PATH = PROCESSED_DIR / "processed_data.parquet"

FEATURE_COLUMNS = [
    "VIN (1-10)",
    "City",
    "Model Year",
    "Make",
    "Electric Vehicle Type",
    "Electric Range",
    "Clean Alternative Fuel Vehicle (CAFV) Eligibility",
]


class DataPreprocessor:
    def __init__(self, dataset_path=RAW_DATA_PATH):
        self.dataset_path = Path(dataset_path)
        self.scaler = StandardScaler()
        self.ev_type_encoder = LabelEncoder()
        self.cafv_encoder = LabelEncoder()

    def load_dataset(self):
        return pd.read_csv(self.dataset_path)

    def select_columns(self, df):
        return df[FEATURE_COLUMNS].copy()

    def remove_duplicates(self, df):
        print("Duplicates:", df.duplicated().sum())
        return df.drop_duplicates()

    def remove_nulls(self, df):
        before = len(df)
        df = df.dropna()
        print("Nulls Removed:", before - len(df))
        return df

    def encode_ev_type(self, df):
        df["Electric Vehicle Type"] = self.ev_type_encoder.fit_transform(
            df["Electric Vehicle Type"]
        )
        return df

    def encode_target(self, df):
        target = "Clean Alternative Fuel Vehicle (CAFV) Eligibility"
        df[target] = self.cafv_encoder.fit_transform(df[target])
        return df

    def one_hot_make(self, df):
        return pd.get_dummies(df, columns=["Make"], dtype=int)

    def drop_unused(self, df):
        return df.drop(columns=["VIN (1-10)", "City"])

    def split_features_target(self, df):
        target = "Clean Alternative Fuel Vehicle (CAFV) Eligibility"
        return df.drop(columns=[target]), df[target]

    def scale_data(self, X):
        numeric_columns = ["Model Year", "Electric Range"]
        X = X.copy()
        X[numeric_columns] = self.scaler.fit_transform(X[numeric_columns])
        return X

    def save_processed_data(self, df):
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        df.to_parquet(PROCESSED_DATA_PATH, index=False)
        print("Processed Data Saved:", PROCESSED_DATA_PATH)

    def save_scaler(self):
        joblib.dump(self.scaler, BACKEND_DIR / "ml" / "scaler.pkl")

    def save_encoders(self):
        joblib.dump(self.ev_type_encoder, BACKEND_DIR / "ml" / "ev_type_encoder.pkl")
        joblib.dump(self.cafv_encoder, BACKEND_DIR / "ml" / "label_encoder.pkl")

    def create_split(self, X, y):
        return train_test_split(
            X,
            y,
            test_size=0.3,
            random_state=100,
            stratify=y,
        )

    def process(self):
        df = self.load_dataset()
        df = self.select_columns(df)
        df = self.remove_duplicates(df)
        df = self.remove_nulls(df)
        df = self.encode_ev_type(df)
        df = self.encode_target(df)
        df = self.one_hot_make(df)
        df = self.drop_unused(df)

        X, y = self.split_features_target(df)
        X = self.scale_data(X)
        processed_df = X.copy()
        processed_df["Clean Alternative Fuel Vehicle (CAFV) Eligibility"] = y.values
        self.save_processed_data(processed_df)
        self.save_scaler()
        self.save_encoders()
        return self.create_split(X, y)


if __name__ == "__main__":
    processor = DataPreprocessor()
    X_train, X_test, y_train, y_test = processor.process()
    print("X Train Shape:", X_train.shape)
    print("X Test Shape:", X_test.shape)
