import pandas as pd

from rca.rules import (
    analyze_interface_evidence,
    determine_root_cause
)


RESULTS_FILE = (
    "data/processed/anomaly_results.csv"
)


CAUSE_MAPPING = {

    "congestion":
        "Network congestion",

    "high_cpu":
        "Device resource exhaustion",

    "interface_flap":
        "Interface flapping",

    "interface_failure":
        "Interface failure"
}


def evaluate_rca():

    df = pd.read_csv(
        RESULTS_FILE
    )

    # Only evaluate ML-detected anomalies
    anomalies = df[
        df["anomaly_prediction"] == 1
    ].copy()

    results = []

    for _, row in anomalies.iterrows():

        evidence, scores = (
            analyze_interface_evidence(row)
        )

        diagnosis = determine_root_cause(
            scores
        )

        actual_type = row[
            "incident_type"
        ]

        expected = CAUSE_MAPPING.get(
            actual_type
        )

        predicted = diagnosis[
            "root_cause"
        ]

        correct = (
            expected == predicted
        )

        results.append({

            "device":
                row["device"],

            "interface":
                row["interface"],

            "actual":
                expected,

            "predicted":
                predicted,

            "correct":
                correct
        })

    results_df = pd.DataFrame(
        results
    )

    print(
        "\n========================================"
    )

    print(
        "RCA EVALUATION"
    )

    print(
        "========================================"
    )

    print(
        f"\nEvaluated incidents: "
        f"{len(results_df)}"
    )

    correct_count = (
        results_df["correct"].sum()
    )

    total = len(results_df)

    accuracy = (
        correct_count / total
        if total > 0
        else 0
    )

    print(
        f"Correct diagnoses: "
        f"{correct_count}"
    )

    print(
        f"RCA Accuracy: "
        f"{accuracy:.4f}"
    )

    print(
        f"RCA Accuracy (%): "
        f"{accuracy * 100:.2f}%"
    )

    print(
        "\n========================================"
    )

    print(
        "RESULT BY INCIDENT TYPE"
    )

    print(
        "========================================"
    )

    for incident_type in (
        results_df["actual"].unique()
    ):

        subset = results_df[
            results_df["actual"]
            == incident_type
        ]

        type_accuracy = (
            subset["correct"].mean()
        )

        print(
            f"{incident_type}: "
            f"{type_accuracy * 100:.2f}%"
        )

    print(
        "\n========================================"
    )

    print(
        "DETAILED RESULTS"
    )

    print(
        "========================================"
    )

    print(
        results_df.to_string(
            index=False
        )
    )


if __name__ == "__main__":

    evaluate_rca()