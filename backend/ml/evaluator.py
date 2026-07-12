import json
import pandas as pd
from pathlib import Path

_METRICS_PATH = Path(__file__).resolve().parent / "metrics.json"
try:
    with open(_METRICS_PATH, "r") as f:
        metrics = json.load(f)
except (json.JSONDecodeError, FileNotFoundError):
    metrics = {}


def compare_models():
    rows = []
    for model_name, data in metrics.items():
        rows.append({
            "Model": model_name,
            "Accuracy": data.get("accuracy"),
            "CV Mean": data.get("cross_validation_mean"),
        })

    df = pd.DataFrame(rows)
    if "Accuracy" in df.columns:
        return df.sort_values("Accuracy", ascending=False)
    return df


def get_confusion_matrix(model_name):
    return metrics[model_name]["confusion_matrix"]


def get_cross_validation(model_name):
    return metrics[model_name]["cross_validation_scores"]


def get_best_model():
    df = compare_models()
    return df.iloc[0]


if __name__ == "__main__":
    print(compare_models())
    print(get_best_model())