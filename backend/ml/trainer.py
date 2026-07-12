import json
import time
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DATA_PATH = BACKEND_DIR / "data" / "processed" / "processed_data.parquet"
MODELS_DIR = BACKEND_DIR / "ml" / "models"
METRICS_PATH = BACKEND_DIR / "ml" / "metrics.json"
TARGET_COLUMN = "Clean Alternative Fuel Vehicle (CAFV) Eligibility"


MODELS = {
    "logistic_regression": LogisticRegression(max_iter=500),
    "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
    "decision_tree": DecisionTreeClassifier(criterion="entropy", random_state=42),
    "svm": SVC(kernel="linear", C=1.0, probability=True),
    "knn": KNeighborsClassifier(n_neighbors=345),
    "adaboost": AdaBoostClassifier(
        n_estimators=100,
        learning_rate=0.1,
        random_state=42,
    ),
}

TRAINING_LIMITS = {
    "logistic_regression": 80000,
    "random_forest": 80000,
    "decision_tree": 80000,
    "svm": 15000,
    "knn": 30000,
    "adaboost": 80000,
}

CV_SAMPLE_SIZE = 30000


def load_data():
    df = pd.read_parquet(PROCESSED_DATA_PATH)
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]
    return train_test_split(X, y, test_size=0.3, random_state=100, stratify=y)


def load_full_data():
    df = pd.read_parquet(PROCESSED_DATA_PATH)
    return df.drop(columns=[TARGET_COLUMN]), df[TARGET_COLUMN]


def train_model(model, X_train, y_train):
    started = time.perf_counter()
    model.fit(X_train, y_train)
    return model, time.perf_counter() - started


def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    cm = confusion_matrix(y_test, predictions)
    report = classification_report(y_test, predictions, output_dict=True)
    return accuracy, cm, report


def perform_cross_validation(model, X, y):
    if len(X) > CV_SAMPLE_SIZE:
        sample = X.assign(_target=y).sample(CV_SAMPLE_SIZE, random_state=42)
        y = sample.pop("_target")
        X = sample

    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    return cross_val_score(model, X, y, cv=cv, scoring="accuracy")


def save_model(model, name):
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODELS_DIR / f"{name}.pkl")


def train_all_models():
    all_metrics = {}
    X_train, X_test, y_train, y_test = load_data()
    X_full, y_full = load_full_data()

    for name, model in MODELS.items():
        print(f"Training {name}", flush=True)
        limit = TRAINING_LIMITS[name]
        if len(X_train) > limit:
            train_sample = X_train.assign(_target=y_train).sample(limit, random_state=42)
            y_fit = train_sample.pop("_target")
            X_fit = train_sample
        else:
            X_fit = X_train
            y_fit = y_train

        trained_model, training_time = train_model(model, X_fit, y_fit)
        accuracy, cm, report = evaluate_model(trained_model, X_test, y_test)
        cv_scores = perform_cross_validation(model, X_full, y_full)
        save_model(trained_model, name)

        all_metrics[name] = {
            "accuracy": float(accuracy),
            "training_time": float(training_time),
            "confusion_matrix": cm.tolist(),
            "classification_report": report,
            "cross_validation_scores": cv_scores.tolist(),
            "cross_validation_mean": float(cv_scores.mean()),
        }

    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(all_metrics, f, indent=4)

    return all_metrics


if __name__ == "__main__":
    metrics = train_all_models()
    for model_name, values in metrics.items():
        print(model_name, values["accuracy"])
