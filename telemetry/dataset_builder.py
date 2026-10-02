import pandas as pd
import numpy as np

from telemetry.generator import generate_normal_telemetry
from network.scenarios import (
    apply_interface_flap,
    apply_congestion,
    apply_high_cpu,
    apply_interface_failure
)


def create_normal_dataset():

    df = generate_normal_telemetry(minutes=1000)

    df["label"] = 0
    df["incident_type"] = "normal"

    return df


def create_interface_flap_dataset():

    df = generate_normal_telemetry(minutes=1000)

    df = apply_interface_flap(
        df,
        device="SW2",
        interface="Gi0/2"
    )

    # Mark the modified rows
    mask = (
        (df["device"] == "SW2") &
        (df["interface"] == "Gi0/2")
    )

    # Only the last 20 rows were modified
    indices = df[mask].index

    incident_indices = indices[-20:]

    df["label"] = 0
    df["incident_type"] = "normal"

    df.loc[incident_indices, "label"] = 1
    df.loc[incident_indices, "incident_type"] = "interface_flap"

    return df


def create_congestion_dataset():

    df = generate_normal_telemetry(minutes=1000)

    df = apply_congestion(
        df,
        device="SW2",
        interface="Gi0/2"
    )

    mask = (
        (df["device"] == "SW2") &
        (df["interface"] == "Gi0/2")
    )

    indices = df[mask].index
    incident_indices = indices[-20:]

    df["label"] = 0
    df["incident_type"] = "normal"

    df.loc[incident_indices, "label"] = 1
    df.loc[incident_indices, "incident_type"] = "congestion"

    return df


def create_high_cpu_dataset():

    df = generate_normal_telemetry(minutes=1000)

    df = apply_high_cpu(
        df,
        device="R1"
    )

    mask = df["device"] == "R1"

    indices = df[mask].index
    incident_indices = indices[-20:]

    df["label"] = 0
    df["incident_type"] = "normal"

    df.loc[incident_indices, "label"] = 1
    df.loc[incident_indices, "incident_type"] = "high_cpu"

    return df


def create_interface_failure_dataset():

    df = generate_normal_telemetry(minutes=1000)

    df = apply_interface_failure(
        df,
        device="SW1",
        interface="Gi0/10"
    )

    mask = (
        (df["device"] == "SW1") &
        (df["interface"] == "Gi0/10")
    )

    indices = df[mask].index
    incident_indices = indices[-10:]

    df["label"] = 0
    df["incident_type"] = "normal"

    df.loc[incident_indices, "label"] = 1
    df.loc[incident_indices, "incident_type"] = "interface_failure"

    return df


def build_dataset():

    print("Creating normal dataset...")
    normal = create_normal_dataset()

    print("Creating interface flap dataset...")
    flap = create_interface_flap_dataset()

    print("Creating congestion dataset...")
    congestion = create_congestion_dataset()

    print("Creating high CPU dataset...")
    cpu = create_high_cpu_dataset()

    print("Creating interface failure dataset...")
    failure = create_interface_failure_dataset()

    # Combine datasets
    dataset = pd.concat(
        [
            normal,
            flap,
            congestion,
            cpu,
            failure
        ],
        ignore_index=True
    )

    # Shuffle
    dataset = dataset.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    output_path = "data/processed/network_dataset.csv"

    dataset.to_csv(
        output_path,
        index=False
    )

    print("\nDataset created!")
    print(f"Rows: {len(dataset)}")
    print(f"Saved to: {output_path}")

    print("\nIncident distribution:")
    print(dataset["incident_type"].value_counts())

    print("\nLabel distribution:")
    print(dataset["label"].value_counts())


if __name__ == "__main__":
    build_dataset()