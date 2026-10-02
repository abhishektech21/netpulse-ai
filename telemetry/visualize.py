import pandas as pd
import matplotlib.pyplot as plt


NORMAL_FILE = "data/raw/normal_telemetry.csv"
INCIDENT_FILE = "data/raw/incident_telemetry.csv"


def load_data():

    normal = pd.read_csv(NORMAL_FILE)
    incident = pd.read_csv(INCIDENT_FILE)

    return normal, incident


def show_statistics(normal, incident):

    print("\n========== NORMAL TELEMETRY ==========")
    print(normal.describe())

    print("\n========== INCIDENT TELEMETRY ==========")
    print(incident.describe())


def plot_comparison(normal, incident, metric):

    # Take normal samples from the beginning
    normal_sample = normal.head(200)

    # Take incident samples from the END,
    # where our failures were injected
    incident_sample = incident.tail(200)

    plt.figure(figsize=(12, 5))

    plt.plot(
        normal_sample[metric].values,
        label="Normal"
    )

    plt.plot(
        incident_sample[metric].values,
        label="Incident"
    )

    plt.title(f"{metric} - Normal vs Incident")
    plt.xlabel("Telemetry Sample")
    plt.ylabel(metric)
    plt.legend()
    plt.grid(True)

    plt.show()


if __name__ == "__main__":

    normal, incident = load_data()

    show_statistics(normal, incident)

    metrics = [
        "latency_ms",
        "packet_loss_percent",
        "packet_errors",
        "cpu_usage",
        "bandwidth_utilization",
        "interface_flaps"
    ]

    for metric in metrics:
        plot_comparison(
            normal,
            incident,
            metric
        )