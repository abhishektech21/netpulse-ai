import pandas as pd
import numpy as np
from datetime import datetime, timedelta


np.random.seed(42)


DEVICES = {
    "R1": ["Gi0/1", "Gi0/2"],
    "SW1": ["Gi0/1", "Gi0/10", "Gi0/11"],
    "SW2": ["Gi0/2", "Gi0/10", "Gi0/11"],
}


def generate_normal_telemetry(minutes=1000):

    rows = []

    start_time = datetime.now()

    for i in range(minutes):

        timestamp = start_time + timedelta(minutes=i)

        for device, interfaces in DEVICES.items():

            for interface in interfaces:

                # Normal network behaviour
                cpu = np.random.normal(40, 5)
                memory = np.random.normal(50, 5)
                bandwidth = np.random.normal(45, 8)
                latency = np.random.normal(12, 2)
                packet_loss = max(0, np.random.normal(0.2, 0.1))
                jitter = max(0, np.random.normal(2, 0.5))
                packet_errors = max(0, int(np.random.normal(3, 2)))
                interface_flaps = 0

                rows.append({
                    "timestamp": timestamp,
                    "device": device,
                    "interface": interface,
                    "cpu_usage": round(cpu, 2),
                    "memory_usage": round(memory, 2),
                    "bandwidth_utilization": round(bandwidth, 2),
                    "latency_ms": round(latency, 2),
                    "packet_loss_percent": round(packet_loss, 2),
                    "jitter_ms": round(jitter, 2),
                    "packet_errors": packet_errors,
                    "interface_flaps": interface_flaps,
                    "interface_status": "UP"
                })

    return pd.DataFrame(rows)


if __name__ == "__main__":

    df = generate_normal_telemetry()

    output_path = "data/raw/normal_telemetry.csv"

    df.to_csv(output_path, index=False)

    print("Telemetry generated successfully!")
    print(f"Rows generated: {len(df)}")
    print(f"Saved to: {output_path}")

    print("\nFirst 5 rows:")
    print(df.head())