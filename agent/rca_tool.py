import pandas as pd

RESULTS_FILE = "data/processed/anomaly_results.csv"


def analyze_incident(device, interface):
    df = pd.read_csv(RESULTS_FILE)

    data = df[
        (df["device"] == device) &
        (df["interface"] == interface) &
        (df["anomaly_prediction"] == 1)
    ].copy()

    if data.empty:
        return {
            "device": device,
            "interface": interface,
            "status": "No confirmed anomaly detected"
        }

    # Select the most abnormal observation
    row = data.loc[data["anomaly_score"].idxmin()]

    evidence = {
        "device": device,
        "interface": interface,
        "anomaly_score": float(row["anomaly_score"]),
        "incident_type": str(row["incident_type"]),
        "cpu_usage": float(row["cpu_usage"]),
        "memory_usage": float(row["memory_usage"]),
        "bandwidth_utilization": float(row["bandwidth_utilization"]),
        "latency_ms": float(row["latency_ms"]),
        "packet_loss_percent": float(row["packet_loss_percent"]),
        "packet_errors": int(row["packet_errors"]),
        "interface_flaps": int(row["interface_flaps"]),
        "interface_status": str(row["interface_status"])
    }

    # Evidence-based RCA rules
    if evidence["interface_status"] == "DOWN":
        root_cause = "Interface failure"

    elif evidence["interface_flaps"] >= 3:
        root_cause = "Interface flapping"

    elif evidence["packet_errors"] >= 100:
        root_cause = "Interface/link instability"

    elif evidence["bandwidth_utilization"] >= 90:
        root_cause = "Network congestion"

    elif evidence["cpu_usage"] >= 90:
        root_cause = "Device resource exhaustion"

    elif evidence["packet_loss_percent"] >= 5:
        root_cause = "Packet loss"

    elif evidence["latency_ms"] >= 50:
        root_cause = "High network latency"

    else:
        root_cause = "Insufficient evidence"

    evidence["root_cause"] = root_cause

    return evidence