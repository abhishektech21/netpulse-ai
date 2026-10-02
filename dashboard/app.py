import sys
from pathlib import Path

# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# --------------------------------------------------
# IMPORTS
# --------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from network.topology import create_network
from agent.rca_tool import analyze_incident
from agent.chat_agent import answer_question


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NetPulse AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

RESULTS_FILE = PROJECT_ROOT / "data" / "processed" / "anomaly_results.csv"

df = pd.read_csv(RESULTS_FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])

df = df.sort_values("timestamp")


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def get_latest_interface_state(dataframe):

    latest = (
        dataframe
        .sort_values("timestamp")
        .groupby(["device", "interface"], as_index=False)
        .tail(1)
    )

    return latest


def get_severity(root_cause):

    if root_cause == "Interface failure":
        return "CRITICAL"

    if root_cause in [
        "Interface flapping",
        "Interface/link instability",
        "Network congestion",
        "Device resource exhaustion"
    ]:
        return "HIGH"

    if root_cause in [
        "Packet loss",
        "High network latency"
    ]:
        return "MEDIUM"

    return "NORMAL"


def get_node_description(node):

    if node.startswith("R"):
        return "Router"

    if node.startswith("SW"):
        return "Switch"

    if node.startswith("H"):
        return "Host"

    return "Network Node"


# --------------------------------------------------
# NETWORK SUMMARY
# --------------------------------------------------

total_devices = df["device"].nunique()

total_anomalies = int(
    df["anomaly_prediction"].sum()
)

latest_states = get_latest_interface_state(df)

active_interfaces = int(
    (latest_states["interface_status"] == "UP").sum()
)

active_incidents = int(
    df[df["anomaly_prediction"] == 1]
    [["device", "interface"]]
    .drop_duplicates()
    .shape[0]
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🌐 NetPulse AI")

st.markdown(
    "### AI-Powered Predictive Network Assurance & Root-Cause Analysis"
)

st.caption(
    "ML-driven anomaly detection • Topology-aware RCA • "
    "Evidence-grounded GenAI troubleshooting"
)

st.divider()


# --------------------------------------------------
# TOP KPI CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Network Devices",
        total_devices
    )

with col2:
    st.metric(
        "Active Incidents",
        active_incidents
    )

with col3:
    st.metric(
        "Active Interfaces",
        active_interfaces
    )

with col4:
    st.metric(
        "Telemetry Records",
        f"{len(df):,}"
    )


st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("🎛️ Incident Selection")

st.sidebar.caption(
    "Select a device and interface to investigate."
)

selected_device = st.sidebar.selectbox(
    "Device",
    sorted(df["device"].unique())
)

device_interfaces = sorted(
    df[
        df["device"] == selected_device
    ]["interface"].unique()
)

selected_interface = st.sidebar.selectbox(
    "Interface",
    device_interfaces
)

st.sidebar.divider()

st.sidebar.markdown("### Demo Scenario")

st.sidebar.info(
    "Recommended demo:\n\n"
    "Device: **SW2**\n\n"
    "Interface: **Gi0/2**\n\n"
    "Incident: **Interface Flapping**"
)


# --------------------------------------------------
# RCA
# --------------------------------------------------

rca = analyze_incident(
    selected_device,
    selected_interface
)

root_cause = rca.get(
    "root_cause",
    "Insufficient evidence"
)

severity = get_severity(root_cause)

has_incident = (
    root_cause != "Insufficient evidence"
    and "status" not in rca
)


# --------------------------------------------------
# INCIDENT ANALYSIS HEADER
# --------------------------------------------------

st.header("🔎 Incident Analysis")

st.caption(
    f"Selected interface: "
    f"**{selected_device} / {selected_interface}**"
)


# --------------------------------------------------
# INCIDENT STATUS
# --------------------------------------------------

if has_incident:

    if severity == "CRITICAL":
        st.error(
            f"🚨 {severity} INCIDENT DETECTED"
        )

    elif severity == "HIGH":
        st.warning(
            f"⚠️ {severity} SEVERITY INCIDENT DETECTED"
        )

    else:
        st.info(
            f"ℹ️ {severity} SEVERITY INCIDENT"
        )

else:

    st.success(
        "🟢 No confirmed incident for the selected interface"
    )


# --------------------------------------------------
# INCIDENT KPI CARDS
# --------------------------------------------------

if has_incident:

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Root Cause",
            root_cause
        )

    with col2:
        st.metric(
            "Packet Loss",
            f"{rca.get('packet_loss_percent', 0):.2f}%"
        )

    with col3:
        st.metric(
            "Packet Errors",
            f"{rca.get('packet_errors', 0):,}"
        )

    with col4:
        st.metric(
            "Interface Flaps",
            rca.get("interface_flaps", 0)
        )


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Latency",
            f"{rca.get('latency_ms', 0):.2f} ms"
        )

    with col2:
        st.metric(
            "Bandwidth",
            f"{rca.get('bandwidth_utilization', 0):.2f}%"
        )

    with col3:
        st.metric(
            "CPU",
            f"{rca.get('cpu_usage', 0):.2f}%"
        )

    with col4:
        st.metric(
            "Anomaly Score",
            f"{rca.get('anomaly_score', 0):.4f}"
        )


    # --------------------------------------------------
    # EVIDENCE
    # --------------------------------------------------

    st.markdown("### 📋 RCA Evidence")

    evidence_col1, evidence_col2 = st.columns(2)

    with evidence_col1:

        st.write(
            f"**Incident Type:** "
            f"`{rca.get('incident_type', 'unknown')}`"
        )

        st.write(
            f"**Interface Status:** "
            f"`{rca.get('interface_status', 'unknown')}`"
        )

        st.write(
            f"**CPU Usage:** "
            f"{rca.get('cpu_usage', 0):.2f}%"
        )

        st.write(
            f"**Memory Usage:** "
            f"{rca.get('memory_usage', 0):.2f}%"
        )

    with evidence_col2:

        st.write(
            f"**Bandwidth Utilization:** "
            f"{rca.get('bandwidth_utilization', 0):.2f}%"
        )

        st.write(
            f"**Latency:** "
            f"{rca.get('latency_ms', 0):.2f} ms"
        )

        st.write(
            f"**Packet Loss:** "
            f"{rca.get('packet_loss_percent', 0):.2f}%"
        )

        st.write(
            f"**Interface Flaps:** "
            f"{rca.get('interface_flaps', 0)}"
        )


    st.caption(
        "RCA is based on deterministic evidence rules applied "
        "to telemetry identified as anomalous by the ML layer."
    )


else:

    st.info(
        "No confirmed anomaly is currently associated with "
        f"{selected_device} / {selected_interface}."
    )


st.divider()


# --------------------------------------------------
# NETWORK TOPOLOGY
# --------------------------------------------------

st.header("🗺️ Network Topology")

st.caption(
    "Selected device is highlighted for incident investigation."
)

graph = create_network()


positions = {
    "R1": (0, 1),
    "SW1": (-1.2, 0),
    "SW2": (1.2, 0),
    "H1": (-1.8, -1),
    "H2": (-0.6, -1),
    "H3": (0.6, -1),
    "H4": (1.8, -1)
}


# --------------------------------------------------
# EDGES
# --------------------------------------------------

edge_x = []
edge_y = []

for source, target in graph.edges():

    x0, y0 = positions[source]
    x1, y1 = positions[target]

    edge_x.extend([
        x0,
        x1,
        None
    ])

    edge_y.extend([
        y0,
        y1,
        None
    ])


edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    mode="lines",
    line=dict(
        width=2
    ),
    hoverinfo="none"
)


# --------------------------------------------------
# NODES
# --------------------------------------------------

node_x = []
node_y = []
node_text = []
node_hover = []
node_sizes = []
node_symbols = []


for node in graph.nodes():

    x, y = positions[node]

    node_x.append(x)
    node_y.append(y)

    node_text.append(node)

    node_hover.append(
        f"{node}<br>"
        f"Type: {get_node_description(node)}"
    )

    if node == selected_device:

        node_sizes.append(45)
        node_symbols.append("diamond")

    elif node.startswith("R"):

        node_sizes.append(38)
        node_symbols.append("square")

    elif node.startswith("SW"):

        node_sizes.append(38)
        node_symbols.append("circle")

    else:

        node_sizes.append(30)
        node_symbols.append("circle")


node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers+text",
    text=node_text,
    textposition="bottom center",
    hovertext=node_hover,
    hoverinfo="text",
    marker=dict(
        size=node_sizes,
        symbol=node_symbols,
        line=dict(
            width=2
        )
    )
)


# --------------------------------------------------
# TOPOLOGY FIGURE
# --------------------------------------------------

fig = go.Figure(
    data=[
        edge_trace,
        node_trace
    ]
)


fig.update_layout(
    height=500,
    showlegend=False,
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=20
    ),
    xaxis=dict(
        visible=False,
        range=[-2.3, 2.3]
    ),
    yaxis=dict(
        visible=False,
        range=[-1.5, 1.5]
    ),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)"
)


st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False
    }
)


st.divider()


# --------------------------------------------------
# TELEMETRY
# --------------------------------------------------

st.header("📊 Interface Telemetry")

interface_data = df[
    (df["device"] == selected_device) &
    (df["interface"] == selected_interface)
].copy()

interface_data = interface_data.sort_values(
    "timestamp"
).tail(100)


# --------------------------------------------------
# TELEMETRY SUMMARY
# --------------------------------------------------

if not interface_data.empty:

    latest = interface_data.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Current CPU",
            f"{latest['cpu_usage']:.2f}%"
        )

    with col2:

        st.metric(
            "Current Latency",
            f"{latest['latency_ms']:.2f} ms"
        )

    with col3:

        st.metric(
            "Current Packet Loss",
            f"{latest['packet_loss_percent']:.2f}%"
        )

    with col4:

        st.metric(
            "Interface Status",
            latest["interface_status"]
        )


# --------------------------------------------------
# TELEMETRY CHARTS
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.markdown("### Latency")

    latency_fig = go.Figure()

    latency_fig.add_trace(
        go.Scatter(
            x=interface_data["timestamp"],
            y=interface_data["latency_ms"],
            mode="lines",
            name="Latency"
        )
    )

    latency_fig.update_layout(
        height=300,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title=None,
        yaxis_title="ms"
    )

    st.plotly_chart(
        latency_fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


with col2:

    st.markdown("### Packet Loss")

    loss_fig = go.Figure()

    loss_fig.add_trace(
        go.Scatter(
            x=interface_data["timestamp"],
            y=interface_data["packet_loss_percent"],
            mode="lines",
            name="Packet Loss"
        )
    )

    loss_fig.update_layout(
        height=300,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title=None,
        yaxis_title="%"
    )

    st.plotly_chart(
        loss_fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


col1, col2 = st.columns(2)


with col1:

    st.markdown("### Packet Errors")

    errors_fig = go.Figure()

    errors_fig.add_trace(
        go.Scatter(
            x=interface_data["timestamp"],
            y=interface_data["packet_errors"],
            mode="lines",
            name="Packet Errors"
        )
    )

    errors_fig.update_layout(
        height=300,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title=None,
        yaxis_title="Errors"
    )

    st.plotly_chart(
        errors_fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


with col2:

    st.markdown("### Interface Flaps")

    flap_fig = go.Figure()

    flap_fig.add_trace(
        go.Scatter(
            x=interface_data["timestamp"],
            y=interface_data["interface_flaps"],
            mode="lines",
            name="Interface Flaps"
        )
    )

    flap_fig.update_layout(
        height=300,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        ),
        xaxis_title=None,
        yaxis_title="Flaps"
    )

    st.plotly_chart(
        flap_fig,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


st.divider()


# --------------------------------------------------
# RAW TELEMETRY
# --------------------------------------------------

with st.expander("📄 View Raw Telemetry"):

    st.dataframe(
        interface_data,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# --------------------------------------------------
# AI TROUBLESHOOTING ASSISTANT
# --------------------------------------------------

st.header("🤖 NetPulse AI Troubleshooting Assistant")

st.caption(
    "Ask questions about the selected incident. "
    "The response is grounded in telemetry and RCA evidence."
)


user_question = st.text_input(
    "Ask NetPulse AI",
    placeholder=(
        "Example: Why is this interface experiencing "
        "packet loss?"
    )
)


if st.button(
    "🔍 Analyze Incident",
    type="primary"
):

    if not user_question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        with st.spinner(
            "NetPulse AI is analyzing the network evidence..."
        ):

            try:

                answer = answer_question(
                    user_question,
                    selected_device,
                    selected_interface
                )

                st.markdown("### 🧠 AI Analysis")

                st.markdown(answer)

            except Exception as e:

                st.error(
                    f"AI analysis failed: {e}"
                )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "NetPulse AI — Student-built research prototype for "
    "predictive network assurance, topology-aware RCA, "
    "and evidence-grounded AI troubleshooting."
)