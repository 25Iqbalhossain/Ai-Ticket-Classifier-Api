from __future__ import annotations

import os
import joblib
from dataclasses import dataclass
from typing import Optional

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


@dataclass
class MLArtifacts:
    pipeline: Pipeline
    labels: list[str]



DEFAULT_LABELS = ["Complaint", "Billing", "Technical", "Other","Account"]

DATA_PATH = r"C:\Users\hi\OneDrive\Desktop\ai_ticket_api\app\data\enhanced_customer_support_data.csv"


def load_training_data_from_csv(csv_path: str) -> tuple[list[str], list[str]]:
    df = pd.read_csv(csv_path)

    df = df.dropna(subset=["Ticket_Subject", "Ticket_Description", "Issue_Category"])
    X = (df["Ticket_Subject"].astype(str) + " " + df["Ticket_Description"].astype(str)).tolist()

   
    mapping = {
        "Technical": "Technical",
        "Billing": "Billing",
        "Fraud": "Complaint",
        "Account": "Account",
        "General Inquiry": "other",
    }

    y = df["Issue_Category"].astype(str).map(mapping)

    y = y.fillna("other").tolist()

    return X, y


def train_and_save(model_path: str, data_path: str = DATA_PATH) -> MLArtifacts:
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"CSV file not found: {data_path}")

    X, y = load_training_data_from_csv(data_path)

    pipeline = Pipeline(
        steps=[
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
            ("clf", LogisticRegression(max_iter=2000)),
        ]
    )
    pipeline.fit(X, y)

    learned_labels = list(pipeline.named_steps["clf"].classes_)
    artifacts = {"pipeline": pipeline, "labels": learned_labels}

    model_dir = os.path.dirname(model_path)
    if model_dir:
        os.makedirs(model_dir, exist_ok=True)

    joblib.dump(artifacts, model_path)
    return MLArtifacts(pipeline=pipeline, labels=learned_labels)


class TicketClassifier:
    def __init__(self, model_path: str, data_path: str = DATA_PATH):
        self.model_path = model_path
        self.data_path = data_path
        self.artifacts: Optional[MLArtifacts] = None

    def load(self) -> None:
        if os.path.exists(self.model_path):
            data = joblib.load(self.model_path)
            self.artifacts = MLArtifacts(
                pipeline=data["pipeline"],
                labels=data.get("labels", DEFAULT_LABELS),
            )
        else:
            self.artifacts = train_and_save(self.model_path, self.data_path)

    def predict_category(self, text: str) -> str:
        if self.artifacts is None:
            self.load()
        return str(self.artifacts.pipeline.predict([text])[0])
