def analyze_interface_evidence(row):

    evidence = []
    scores = {}

    # -----------------------------------------
    # Interface DOWN
    # -----------------------------------------

    if row["interface_status"] == "DOWN":

        evidence.append(
            "Interface status is DOWN"
        )

        scores["interface_failure"] = 6

    # -----------------------------------------
    # Interface flapping
    # -----------------------------------------

    if row["interface_flaps"] >= 3:

        evidence.append(
            f"Interface flapped "
            f"{int(row['interface_flaps'])} times"
        )

        scores["interface_flapping"] = 5

    # -----------------------------------------
    # Packet errors
    # -----------------------------------------

    if row["packet_errors"] >= 100:

        evidence.append(
            f"Packet errors increased to "
            f"{int(row['packet_errors'])}"
        )

        scores["interface_instability"] = (
            scores.get(
                "interface_instability",
                0
            ) + 3
        )

    # -----------------------------------------
    # Packet loss
    # -----------------------------------------

    if row["packet_loss_percent"] >= 5:

        evidence.append(
            f"Packet loss reached "
            f"{row['packet_loss_percent']:.2f}%"
        )

        scores["packet_loss"] = (
            scores.get(
                "packet_loss",
                0
            ) + 2
        )

    # -----------------------------------------
    # High latency
    # -----------------------------------------

    if row["latency_ms"] >= 50:

        evidence.append(
            f"Latency increased to "
            f"{row['latency_ms']:.2f} ms"
        )

        scores["latency"] = (
            scores.get(
                "latency",
                0
            ) + 2
        )

    # -----------------------------------------
    # Congestion
    # -----------------------------------------

    if row["bandwidth_utilization"] >= 90:

        evidence.append(
            f"Bandwidth utilization reached "
            f"{row['bandwidth_utilization']:.2f}%"
        )

        scores["congestion"] = 5

    # -----------------------------------------
    # High CPU
    # -----------------------------------------

    if row["cpu_usage"] >= 90:

        evidence.append(
            f"CPU utilization reached "
            f"{row['cpu_usage']:.2f}%"
        )

        scores["high_cpu"] = 5

    return evidence, scores


def determine_root_cause(scores):

    if not scores:

        return {
            "root_cause": "Insufficient evidence",
            "confidence": 0,
            "scores": {}
        }

    # Pick highest scoring cause
    root_cause = max(
        scores,
        key=scores.get
    )

    max_score = scores[root_cause]

    # Prototype evidence-strength score.
    confidence = min(
        max_score / 6,
        1.0
    )

    cause_names = {

        "interface_failure":
            "Interface failure",

        "interface_flapping":
            "Interface flapping",

        "interface_instability":
            "Interface/link instability",

        "packet_loss":
            "Packet loss",

        "latency":
            "High network latency",

        "congestion":
            "Network congestion",

        "high_cpu":
            "Device resource exhaustion"
    }

    return {
        "root_cause": cause_names.get(
            root_cause,
            root_cause
        ),

        "confidence": round(
            confidence,
            2
        ),

        "scores": scores
    }