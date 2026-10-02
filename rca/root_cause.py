import pandas as pd

from rca.rules import (
    analyze_interface_evidence,
    determine_root_cause
)

from rca.topology_engine import (
    get_neighbors,
    get_connected_interfaces,
    find_affected_paths
)

from network.topology import create_network


RESULTS_FILE = (
    "data/processed/anomaly_results.csv"
)


def analyze_incident(row, graph):

    # -----------------------------------------
    # 1. Metric evidence
    # -----------------------------------------

    evidence, scores = analyze_interface_evidence(row)

    diagnosis = determine_root_cause(scores)

    # -----------------------------------------
    # 2. Topology information
    # -----------------------------------------

    device = row["device"]

    neighbors = get_neighbors(
        graph,
        device
    )

    interfaces = get_connected_interfaces(
        graph,
        device
    )

    paths = find_affected_paths(
        graph,
        device
    )

    # -----------------------------------------
    # 3. Add topology evidence
    # -----------------------------------------

    if neighbors:

        evidence.append(
            f"Device is connected to: "
            f"{', '.join(neighbors)}"
        )

    return {

        "device": device,

        "interface": row["interface"],

        "root_cause":
            diagnosis["root_cause"],

        "confidence":
            diagnosis["confidence"],

        "evidence": evidence,

        "neighbors": neighbors,

        "connected_interfaces": interfaces,

        "affected_paths": paths,

        "anomaly_score":
            row["anomaly_score"],

        "incident_type":
            row["incident_type"]
    }


def run_rca():

    # -----------------------------------------
    # Load network graph
    # -----------------------------------------

    graph = create_network()

    # -----------------------------------------
    # Load anomaly results
    # -----------------------------------------

    df = pd.read_csv(
        RESULTS_FILE
    )

    # Only ML-detected anomalies
    anomalies = df[
        df["anomaly_prediction"] == 1
    ].copy()

    print(
        f"ML detected anomalies: "
        f"{len(anomalies)}"
    )

    # -----------------------------------------
    # Group by device/interface
    # -----------------------------------------

    grouped = anomalies.groupby(
        ["device", "interface"]
    )

    print(
        "\n========================================"
    )

    print(
        "TOPOLOGY-AWARE ROOT CAUSE ANALYSIS"
    )

    print(
        "========================================"
    )

    for (device, interface), group in grouped:

        # Use the most abnormal observation
        # for this device/interface.

        row = group.loc[
            group["anomaly_score"].idxmin()
        ]

        result = analyze_incident(
            row,
            graph
        )

        print(
            "\n----------------------------------------"
        )

        print(
            f"Device: {result['device']}"
        )

        print(
            f"Interface: {result['interface']}"
        )

        print(
            f"Anomalous observations: "
            f"{len(group)}"
        )

        print(
            f"Root Cause: "
            f"{result['root_cause']}"
        )

        print(
            f"Confidence: "
            f"{result['confidence']}"
        )

        print("\nTopology:")

        print(
            f"Neighbors: "
            f"{', '.join(result['neighbors'])}"
        )

        print("\nEvidence:")

        for item in result["evidence"]:

            print(
                f"  • {item}"
            )


if __name__ == "__main__":

    run_rca()