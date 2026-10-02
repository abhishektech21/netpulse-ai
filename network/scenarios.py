import pandas as pd
import numpy as np


def apply_interface_flap(df, device="SW2", interface="Gi0/2"):

    mask = (
        (df["device"] == device) &
        (df["interface"] == interface)
    )

    indices = df[mask].index

    if len(indices) > 20:

        selected = indices[-20:]

        df.loc[selected, "interface_flaps"] = np.random.randint(
            5, 10, len(selected)
        )

        df.loc[selected, "packet_errors"] += np.random.randint(
            100, 500, len(selected)
        )

        df.loc[selected, "packet_loss_percent"] += np.random.uniform(
            5, 20, len(selected)
        )

        df.loc[selected, "latency_ms"] += np.random.uniform(
            30, 80, len(selected)
        )

    return df


def apply_congestion(df, device="SW2", interface="Gi0/2"):

    mask = (
        (df["device"] == device) &
        (df["interface"] == interface)
    )

    indices = df[mask].index

    if len(indices) > 20:

        selected = indices[-20:]

        df.loc[selected, "bandwidth_utilization"] = np.random.uniform(
            90, 100, len(selected)
        )

        df.loc[selected, "latency_ms"] += np.random.uniform(
            40, 100, len(selected)
        )

        df.loc[selected, "packet_loss_percent"] += np.random.uniform(
            2, 8, len(selected)
        )

    return df


def apply_high_cpu(df, device="R1"):

    mask = df["device"] == device

    indices = df[mask].index

    if len(indices) > 20:

        selected = indices[-20:]

        df.loc[selected, "cpu_usage"] = np.random.uniform(
            90, 100, len(selected)
        )

        df.loc[selected, "memory_usage"] = np.random.uniform(
            80, 95, len(selected)
        )

    return df


def apply_interface_failure(df, device="SW1", interface="Gi0/10"):

    mask = (
        (df["device"] == device) &
        (df["interface"] == interface)
    )

    indices = df[mask].index

    if len(indices) > 10:

        selected = indices[-10:]

        df.loc[selected, "interface_status"] = "DOWN"

        df.loc[selected, "packet_loss_percent"] = np.random.uniform(
            80, 100, len(selected)
        )

        df.loc[selected, "latency_ms"] = np.random.uniform(
            100, 300, len(selected)
        )

        df.loc[selected, "packet_errors"] += np.random.randint(
            500, 1500, len(selected)
        )

    return df

if __name__ == "__main__":

    from telemetry.generator import generate_normal_telemetry

    df = generate_normal_telemetry()

    # Apply different network incidents
    df = apply_interface_flap(df)
    df = apply_congestion(df)
    df = apply_high_cpu(df)
    df = apply_interface_failure(df)

    output_path = "data/raw/incident_telemetry.csv"

    df.to_csv(output_path, index=False)

    print("Incident telemetry generated!")
    print(f"Rows: {len(df)}")
    print(f"Saved to: {output_path}")