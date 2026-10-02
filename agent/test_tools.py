from agent.tools import (
    get_device_metrics,
    get_interface_status,
    get_anomalies,
    get_incident_history
)


print("\nDEVICE METRICS")

print(
    get_device_metrics("SW2")
)


print("\nINTERFACE STATUS")

print(
    get_interface_status(
        "SW2",
        "Gi0/2"
    )
)


print("\nANOMALIES")

print(
    get_anomalies()[:5]
)


print("\nINCIDENT HISTORY")

print(
    get_incident_history(
        "SW2",
        "Gi0/2"
    )
)