import pandas as pd


RESULTS_FILE = (
    "data/processed/anomaly_results.csv"
)


def get_device_metrics(device):

    df = pd.read_csv(
        RESULTS_FILE
    )

    device_data = df[
        df["device"] == device
    ]

    if device_data.empty:

        return {
            "error":
                f"No telemetry found for {device}"
        }

    latest = device_data.iloc[-1]

    return {
        "device": device,

        "cpu_usage":
            float(latest["cpu_usage"]),

        "memory_usage":
            float(latest["memory_usage"]),

        "bandwidth_utilization":
            float(
                latest[
                    "bandwidth_utilization"
                ]
            ),

        "latency_ms":
            float(latest["latency_ms"]),

        "packet_loss_percent":
            float(
                latest[
                    "packet_loss_percent"
                ]
            )
    }


def get_interface_status(
    device,
    interface
):

    df = pd.read_csv(
        RESULTS_FILE
    )

    data = df[
        (df["device"] == device) &
        (df["interface"] == interface)
    ]

    if data.empty:

        return {
            "error":
                "Interface not found"
        }

    latest = data.iloc[-1]

    return {
        "device": device,
        "interface": interface,

        "status":
            latest["interface_status"],

        "packet_errors":
            int(latest["packet_errors"]),

        "interface_flaps":
            int(latest["interface_flaps"]),

        "packet_loss_percent":
            float(
                latest[
                    "packet_loss_percent"
                ]
            ),

        "latency_ms":
            float(latest["latency_ms"])
    }


def get_anomalies():

    df = pd.read_csv(
        RESULTS_FILE
    )

    anomalies = df[
        df["anomaly_prediction"] == 1
    ]

    return anomalies[
        [
            "device",
            "interface",
            "anomaly_score",
            "incident_type"
        ]
    ].to_dict(
        orient="records"
    )


def get_incident_history(device, interface):
    df = pd.read_csv(RESULTS_FILE)

    data = df[
        (df["device"] == device) &
        (df["interface"] == interface)
    ].copy()

    if data.empty:
        return {"error": "No history found"}

    data["timestamp"] = pd.to_datetime(data["timestamp"])

    data = data.sort_values("timestamp").tail(20)

    return data[[
        "timestamp",
        "cpu_usage",
        "latency_ms",
        "packet_loss_percent",
        "packet_errors",
        "interface_flaps",
        "anomaly_score"
    ]].to_dict(orient="records")