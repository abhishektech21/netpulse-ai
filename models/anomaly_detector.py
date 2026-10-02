import pandas as pd
import numpy as np
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score
)
from sklearn.model_selection import train_test_split


DATA_FILE = "data/processed/network_dataset.csv"

MODEL_FILE = "models_saved/anomaly_model.pkl"
OUTPUT_FILE = "data/processed/anomaly_results.csv"


FEATURES = [
    "cpu_usage",
    "memory_usage",
    "bandwidth_utilization",
    "latency_ms",
    "packet_loss_percent",
    "jitter_ms",
    "packet_errors",
    "interface_flaps"
]


def load_dataset():

    df = pd.read_csv(DATA_FILE)

    print(f"Dataset loaded: {len(df)} rows")

    return df


def prepare_features(df):

    X = df[FEATURES].copy()

    X = X.replace(
        [np.inf, -np.inf],
        np.nan
    )

    X = X.fillna(0)

    return X


def train_model(normal_train):

    X_train = prepare_features(normal_train)

    print(f"Training samples: {len(X_train)}")

    model = IsolationForest(
        n_estimators=300,
        max_samples="auto",
        contamination="auto",
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train)

    return model


def calculate_threshold(model, normal_validation):

    X_validation = prepare_features(
        normal_validation
    )

    normal_scores = model.decision_function(
        X_validation
    )

    # We expect only a very small percentage
    # of normal traffic to be classified as anomalous.
    #
    # 0.2% false-positive allowance.

    threshold = np.percentile(
        normal_scores,
        0.2
    )

    print("\n========================================")
    print("THRESHOLD CALIBRATION")
    print("========================================")

    print(
        f"Anomaly threshold: {threshold:.6f}"
    )

    print(
        "Threshold calibrated using normal "
        "validation telemetry."
    )

    return threshold


def predict(model, df, threshold):

    X = prepare_features(df)

    scores = model.decision_function(X)

    # Lower Isolation Forest scores indicate
    # more abnormal observations.

    predictions = np.where(
        scores < threshold,
        1,
        0
    )

    return predictions, scores


def evaluate(df, predictions):

    actual = df["label"].values

    print("\n========================================")
    print("CONFUSION MATRIX")
    print("========================================")

    cm = confusion_matrix(
        actual,
        predictions
    )

    print(cm)

    print("\n========================================")
    print("CLASSIFICATION REPORT")
    print("========================================")

    print(
        classification_report(
            actual,
            predictions,
            target_names=[
                "Normal",
                "Anomaly"
            ],
            zero_division=0
        )
    )

    precision = precision_score(
        actual,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        actual,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        actual,
        predictions,
        zero_division=0
    )

    print("\n========================================")
    print("FINAL ANOMALY METRICS")
    print("========================================")

    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")

    return precision, recall, f1


def save_results(
    df,
    predictions,
    scores,
    threshold
):

    results = df.copy()

    results["anomaly_score"] = scores

    results["anomaly_prediction"] = predictions

    results["anomaly_status"] = np.where(
        predictions == 1,
        "ANOMALY",
        "NORMAL"
    )

    results["threshold"] = threshold

    results.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"\nResults saved to: {OUTPUT_FILE}"
    )

    return results


def save_model(model):

    joblib.dump(
        model,
        MODEL_FILE
    )

    print(
        f"Model saved to: {MODEL_FILE}"
    )


if __name__ == "__main__":

    print("\n========================================")
    print("NETPULSE AI - ANOMALY DETECTION")
    print("========================================")

    # ------------------------------------------------
    # 1. LOAD DATA
    # ------------------------------------------------

    df = load_dataset()

    print("\nDataset distribution:")
    print(
        df["label"].value_counts()
    )

    # ------------------------------------------------
    # 2. GET ONLY NORMAL DATA
    # ------------------------------------------------

    normal_data = df[
        df["label"] == 0
    ].copy()

    anomaly_data = df[
        df["label"] == 1
    ].copy()

    print(
        f"\nNormal data: {len(normal_data)}"
    )

    print(
        f"Anomaly data: {len(anomaly_data)}"
    )

    # ------------------------------------------------
    # 3. SPLIT NORMAL DATA
    # ------------------------------------------------

    normal_train, normal_validation = train_test_split(
        normal_data,
        test_size=0.20,
        random_state=42
    )

    print(
        f"\nNormal training data: "
        f"{len(normal_train)}"
    )

    print(
        f"Normal validation data: "
        f"{len(normal_validation)}"
    )

    # ------------------------------------------------
    # 4. TRAIN ISOLATION FOREST
    # ------------------------------------------------

    print(
        "\nTraining Isolation Forest..."
    )

    model = train_model(
        normal_train
    )

    print(
        "Training completed."
    )

    # ------------------------------------------------
    # 5. CALIBRATE THRESHOLD
    # ------------------------------------------------

    threshold = calculate_threshold(
        model,
        normal_validation
    )

    # ------------------------------------------------
    # 6. CREATE TEST DATA
    # ------------------------------------------------

    test_data = pd.concat(
        [
            normal_validation,
            anomaly_data
        ],
        ignore_index=True
    )

    test_data = test_data.sample(
        frac=1,
        random_state=42
    ).reset_index(
        drop=True
    )

    print(
        f"\nTest samples: {len(test_data)}"
    )

    # ------------------------------------------------
    # 7. PREDICT
    # ------------------------------------------------

    print(
        "\nRunning anomaly detection..."
    )

    predictions, scores = predict(
        model,
        test_data,
        threshold
    )

    # ------------------------------------------------
    # 8. EVALUATE
    # ------------------------------------------------

    evaluate(
        test_data,
        predictions
    )

    # ------------------------------------------------
    # 9. SAVE RESULTS
    # ------------------------------------------------

    save_results(
        test_data,
        predictions,
        scores,
        threshold
    )

    # ------------------------------------------------
    # 10. SAVE MODEL
    # ------------------------------------------------

    save_model(model)

    print(
        "\n========================================"
    )

    print(
        "PIPELINE COMPLETED"
    )

    print(
        "========================================"
    )