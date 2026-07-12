import joblib
import pandas as pd
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]


class EVPredictor:

    def __init__(self):

        self.models_path = BACKEND_DIR / "ml" / "models"

        self.scaler = joblib.load(
            BACKEND_DIR / "ml" / "scaler.pkl"
        )

        self.ev_type_encoder = joblib.load(
            BACKEND_DIR / "ml" / "ev_type_encoder.pkl"
        )

        self.cafv_encoder = joblib.load(
            BACKEND_DIR / "ml" / "label_encoder.pkl"
        )

        with open(
            BACKEND_DIR / "ml" / "metrics.json",
            "r",
            encoding="utf-8"
        ) as f:
            self.metrics = json.load(f)

        self.best_model_name = self.get_best_model()

        self.model = joblib.load(
            self.models_path /
            f"{self.best_model_name}.pkl"
        )

    def get_best_model(self):

        best_model = None
        best_accuracy = 0

        for model_name, values in self.metrics.items():

            if values["accuracy"] > best_accuracy:

                best_accuracy = values["accuracy"]

                best_model = model_name

        return best_model

    def preprocess_input(
        self,
        model_year,
        make,
        ev_type,
        electric_range
    ):

        df = pd.DataFrame(
            {
                "Model Year": [model_year],
                "Electric Vehicle Type": [ev_type],
                "Electric Range": [electric_range]
            }
        )

        df["Electric Vehicle Type"] = (
            self.ev_type_encoder.transform(
                df["Electric Vehicle Type"]
            )
        )

        training_columns = self.model.feature_names_in_

        for col in training_columns:

            if col.startswith("Make_"):

                if col not in df.columns:

                    df[col] = 0

        make_column = f"Make_{make}"

        if make_column in training_columns:

            df[make_column] = 1

        numeric_columns = [
            "Model Year",
            "Electric Range"
        ]

        df[numeric_columns] = (
            self.scaler.transform(
                df[numeric_columns]
            )
        )

        df = df.reindex(
            columns=training_columns,
            fill_value=0
        )

        return df

    def predict(
        self,
        model_year,
        make,
        ev_type,
        electric_range
    ):

        processed_input = (
            self.preprocess_input(
                model_year,
                make,
                ev_type,
                electric_range
            )
        )

        prediction = self.model.predict(
            processed_input
        )[0]

        probabilities = (
            self.model.predict_proba(
                processed_input
            )[0]
        )

        confidence = (
            max(probabilities) * 100
        )

        predicted_class = (
            self.cafv_encoder.inverse_transform(
                [prediction]
            )[0]
        )

        return {

            "best_model":
            self.best_model_name,

            "prediction":
            predicted_class,

            "confidence":
            round(confidence, 2),

            "probabilities": {

                cls: round(prob * 100, 2)

                for cls, prob in zip(
                    self.cafv_encoder.classes_,
                    probabilities
                )
            },

            "explanation":
            self.generate_explanation(
                predicted_class,
                confidence,
                model_year,
                electric_range,
                ev_type
            )
        }

    def generate_explanation(
        self,
        prediction,
        confidence,
        model_year,
        electric_range,
        ev_type
    ):

        return (
            f"The vehicle is predicted as "
            f"'{prediction}' with "
            f"{confidence:.2f}% confidence. "
            f"The prediction was based on "
            f"Model Year={model_year}, "
            f"Electric Range={electric_range}, "
            f"Vehicle Type={ev_type}."
        )


if __name__ == "__main__":

    predictor = EVPredictor()

    result = predictor.predict(

        model_year=2023,

        make="TESLA",

        ev_type="Battery Electric Vehicle (BEV)",

        electric_range=320

    )

    print(
        json.dumps(
            result,
            indent=4
        )
    )
