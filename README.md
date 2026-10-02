<h1 align="center">NetPulse AI</h1>

<p align="center">
  <strong>AI-Powered Predictive Network Assurance, Root-Cause Analysis & Intelligent Troubleshooting</strong>
</p>

<p align="center">
  Detect → Diagnose → Explain → Troubleshoot
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/ML-Isolation%20Forest-orange" alt="Machine Learning">
  <img src="https://img.shields.io/badge/RCA-Topology%20Aware-purple" alt="RCA">
  <img src="https://img.shields.io/badge/GenAI-Gemini-blue" alt="Gemini">
  <img src="https://img.shields.io/badge/Dashboard-Streamlit-red?logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/Network-NetworkX-teal" alt="NetworkX">
  <img src="https://img.shields.io/badge/Status-Research%20Prototype-success" alt="Status">
</p>

------------------------------------------------------------------------

## 🚨 The Problem

Modern networks continuously generate operational telemetry such as:

-   CPU utilization
-   Memory utilization
-   Bandwidth utilization
-   Latency
-   Packet loss
-   Packet errors
-   Interface flaps
-   Interface status

The difficult part is not simply collecting these metrics.

The difficult part is answering:

> **"Something is wrong. What happened, where did it happen, what is the
> likely root cause, and what should a network engineer check next?"**

Traditional threshold-based monitoring can identify abnormal values, but
it does not naturally connect:

**telemetry → anomaly → network topology → root cause → troubleshooting
guidance**

### NetPulse AI addresses this problem with a layered approach.

------------------------------------------------------------------------

# 🎯 What Is NetPulse AI?

**NetPulse AI** is a student-built network assurance research prototype
that combines:

**synthetic network telemetry + machine-learning anomaly detection +
topology-aware RCA + evidence-grounded GenAI + interactive
visualization**

The system simulates a small network, injects controlled incidents,
detects abnormal telemetry using **Isolation Forest**, performs
**topology-aware root-cause analysis**, and uses **Gemini** to explain
the incident and provide troubleshooting recommendations.

The entire workflow is presented through a **Streamlit network
operations dashboard**.

------------------------------------------------------------------------

# 🧠 How It Works

``` text
                    ┌──────────────────────────┐
                    │     Network Topology     │
                    │   R1 ─ SW1 / SW2 ─ H1-H4 │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │    Telemetry Generator   │
                    │ CPU • Memory • Latency    │
                    │ Loss • Errors • Flaps     │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Incident Simulation     │
                    │                          │
                    │ • Congestion             │
                    │ • High CPU               │
                    │ • Interface Flapping     │
                    │ • Interface Failure      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │  Isolation Forest (ML)   │
                    │   Anomaly Detection      │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Topology-Aware RCA Engine│
                    │       NetworkX           │
                    │                          │
                    │ Evidence + Rules + Paths │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │     Evidence Layer       │
                    │ Structured incident data │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │       Gemini GenAI       │
                    │ Explanation + Guidance   │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │     Streamlit Dashboard  │
                    │                          │
                    │ Topology • Telemetry     │
                    │ RCA • AI Troubleshooting│
                    └──────────────────────────┘
```

------------------------------------------------------------------------

# 🔬 Core Architecture

The project deliberately separates **detection**, **diagnosis**, and
**explanation**.

``` mermaid
flowchart LR
    A[Network Simulator] --> B[Telemetry Generator]
    B --> C[Incident Injection]
    C --> D[Telemetry Dataset]
    D --> E[Isolation Forest]
    E --> F[Anomaly Detection]
    F --> G[NetworkX Topology + RCA Rules]
    G --> H[Structured Evidence]
    H --> I[Gemini GenAI]
    I --> J[Streamlit Dashboard]
    J --> K[Interactive Troubleshooting]
```

### Why this separation matters

The LLM is **not responsible for independently guessing the root
cause**.

Instead:

``` text
ML
 ↓
Detect anomaly

RCA
 ↓
Determine evidence-based root cause

GenAI
 ↓
Explain evidence + recommend troubleshooting
```

This reduces the risk of an LLM inventing telemetry or contradicting the
diagnostic layer.

------------------------------------------------------------------------

# 🖥️ Network Topology

The prototype models a small network:

``` text
                         ┌───────┐
                         │  R1   │
                         │Router │
                         └───┬───┘
                         ┌───┴───┐
                         │       │
                      ┌──▼──┐ ┌──▼──┐
                      │ SW1 │ │ SW2 │
                      └─┬─┬─┘ └─┬─┬─┘
                        │ │     │ │
                       H1 H2   H3 H4
```

### Devices

  Device   Type
  -------- --------
  R1       Router
  SW1      Switch
  SW2      Switch
  H1--H4   Hosts

The topology is represented using **NetworkX**, allowing the RCA layer
to reason about neighbors and connected paths.

------------------------------------------------------------------------

# 🚨 Controlled Network Incidents

The telemetry generator supports controlled incident injection.

  -----------------------------------------------------------------------
  Incident                            Example telemetry behavior
  ----------------------------------- -----------------------------------
  🔥 Network Congestion               Bandwidth approaches 90--100%,
                                      latency and packet loss increase

  🧠 High CPU                         CPU and memory increase
                                      significantly

  🔄 Interface Flapping               Interface flaps, packet errors,
                                      packet loss and latency increase

  🔴 Interface Failure                Interface goes DOWN with severe
                                      packet loss and errors
  -----------------------------------------------------------------------

This controlled design makes it possible to evaluate the complete
pipeline against known ground truth.

------------------------------------------------------------------------

# 🤖 Machine Learning --- Anomaly Detection

## Isolation Forest

NetPulse AI uses **Isolation Forest** to identify unusual network
telemetry.

### Features

``` text
CPU Usage
Memory Usage
Bandwidth Utilization
Latency
Packet Loss
Jitter
Packet Errors
Interface Flaps
```

### Why Isolation Forest?

Network anomalies are generally rare compared with normal telemetry.

The prototype therefore trains the anomaly detector primarily on normal
behavior and identifies observations that deviate significantly from
that baseline.

A custom anomaly threshold is calibrated using held-out normal telemetry
instead of blindly relying on the default decision threshold.

------------------------------------------------------------------------

# 📊 ML Evaluation

The controlled dataset contains:

``` text
Total telemetry records: 40,000
Normal records:          39,930
Anomalous records:           70
```

Anomaly prevalence:

``` text
70 / 40,000 = 0.175%
```

Because anomalies are extremely rare, **accuracy alone is not an
appropriate primary metric**.

### Results

  Metric                  Result
  ----------------- ------------
  Precision           **77.14%**
  Recall              **77.14%**
  F1 Score            **77.14%**
  True Positives          **54**
  False Positives         **16**
  False Negatives         **16**

### Confusion Matrix

``` text
                         Predicted
                    Normal     Anomaly
                 ┌──────────┬──────────┐
Actual Normal    │   7970   │    16    │
                 ├──────────┼──────────┤
Actual Anomaly   │     16   │    54    │
                 └──────────┴──────────┘
```

The evaluation emphasizes **precision, recall and F1** rather than raw
accuracy because the dataset is highly imbalanced.

------------------------------------------------------------------------

# 🧩 Topology-Aware Root-Cause Analysis

After anomaly detection, NetPulse AI uses:

**NetworkX + deterministic evidence rules**

to identify likely root causes.

### Example evidence rules

``` text
Interface DOWN
        ↓
Interface Failure

Interface Flaps >= 3
        ↓
Interface Flapping

Packet Errors >= 100
        ↓
Interface / Link Instability

Bandwidth >= 90%
        ↓
Network Congestion

CPU >= 90%
        ↓
Device Resource Exhaustion

Packet Loss >= 5%
        ↓
Packet Loss

Latency >= 50 ms
        ↓
High Network Latency
```

The topology layer provides additional context such as:

``` text
Affected Device
      ↓
Connected Interfaces
      ↓
Neighboring Devices
      ↓
Potentially Affected Paths
```

------------------------------------------------------------------------

# 📈 RCA Evaluation

The controlled incident set contains four known incident categories.

  Incident Type                                      RCA Result
  ---------------------------- --------------------------------
  Network Congestion             **100%** conditional diagnosis
  Device Resource Exhaustion     **100%** conditional diagnosis
  Interface Flapping             **100%** conditional diagnosis
  Interface Failure              **100%** conditional diagnosis

Overall anomaly detection produced **54 correctly detected true incident
observations**.

Among those correctly detected incidents, the deterministic RCA rules
correctly mapped the controlled incident categories.

> The RCA percentage is reported conditionally on correctly detected
> true incidents; false positives from the ML detector are not treated
> as RCA failures.

------------------------------------------------------------------------

# 🧠 Evidence-Grounded GenAI

Once the RCA layer produces structured evidence, Gemini is used as the
explanation and troubleshooting layer.

### Example evidence

``` json
{
  "device": "SW2",
  "interface": "Gi0/2",
  "root_cause": "Interface flapping",
  "packet_loss_percent": 16.31,
  "packet_errors": 240,
  "interface_flaps": 9,
  "latency_ms": 47.90,
  "bandwidth_utilization": 57.25,
  "cpu_usage": 31.36
}
```

Gemini receives this evidence and can answer questions such as:

``` text
"Why is SW2 Gi0/2 experiencing packet loss?"

"Is this a congestion problem?"

"What evidence supports the root cause?"

"What should a network engineer check first?"

"What Junos commands could be used to investigate this?"
```

### Important architectural principle

> **The LLM explains the evidence; it does not independently determine
> the root cause.**

This makes the GenAI component more controlled and auditable.

------------------------------------------------------------------------

# 🧪 Example Incident

## SW2 / Gi0/2 --- Interface Flapping

### Detected evidence

``` text
Interface Flaps       9
Packet Errors       240
Packet Loss       16.31%
Latency            47.90 ms
Bandwidth          57.25%
CPU                31.36%
```

### Diagnostic reasoning

``` text
CPU is normal
      ↓
Severe CPU exhaustion unlikely

Bandwidth is below saturation
      ↓
Severe congestion not indicated

Repeated interface flaps
+ packet errors
+ packet loss
+ increased latency
      ↓
Interface / link instability
      ↓
Interface Flapping
```

### Example AI troubleshooting guidance

``` text
1. Inspect the physical cable and connectors.
2. Check the SFP/transceiver if applicable.
3. Review interface error counters.
4. Check speed/duplex/negotiation settings.
5. Review system and interface logs.
```

The prototype can also provide **recommended Junos troubleshooting
commands**, but it does not directly execute commands against a physical
Junos device.

------------------------------------------------------------------------

# 🖥️ Streamlit Dashboard

The dashboard provides a single interface for:

### Network Overview

``` text
┌─────────────────────────────────────────────────────┐
│ 🌐 NetPulse AI                                      │
│ Predictive Network Assurance                       │
├─────────────────────────────────────────────────────┤
│ Devices │ Incidents │ Interfaces │ Telemetry       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ 🔎 Incident Analysis                                │
│                                                     │
│ SW2 / Gi0/2                                         │
│                                                     │
│ Root Cause: Interface Flapping                      │
│                                                     │
│ Loss │ Errors │ Flaps │ Latency                     │
│                                                     │
├─────────────────────────────────────────────────────┤
│ 🗺️ Network Topology                                 │
│                                                     │
│                 R1                                  │
│                /  \                                 │
│              SW1  SW2                               │
│             / \   / \                               │
│            H1 H2 H3 H4                              │
│                                                     │
├─────────────────────────────────────────────────────┤
│ 📊 Telemetry                                       │
│                                                     │
│ Latency       Packet Loss                           │
│ Packet Errors Interface Flaps                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Interactive AI

The GenAI assistant is available as an **on-demand troubleshooting
popover**, keeping the main dashboard focused on network monitoring
while allowing engineers to ask questions when required.

------------------------------------------------------------------------

# 🛠️ Technology Stack

  Layer               Technology
  ------------------- ----------------------------
  Programming         Python
  Data Processing     Pandas, NumPy
  ML                  Scikit-learn
  Anomaly Detection   Isolation Forest
  Graph / Topology    NetworkX
  GenAI               Google Gemini
  Dashboard           Streamlit
  Visualization       Plotly
  Configuration       python-dotenv
  Environment         Python virtual environment

------------------------------------------------------------------------

# 📁 Project Structure

``` text
netpulse-ai/
│
├── agent/
│   ├── __init__.py
│   ├── tools.py
│   ├── rca_tool.py
│   ├── gemini_agent.py
│   └── chat_agent.py
│
├── dashboard/
│   ├── __init__.py
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── network_dataset.csv
│       └── anomaly_results.csv
│
├── evaluation/
│   ├── __init__.py
│   └── rca_evaluation.py
│
├── models/
│   └── anomaly_detector.py
│
├── models_saved/
│   └── anomaly_model.pkl
│
├── network/
│   ├── __init__.py
│   ├── topology.py
│   └── scenarios.py
│
├── rca/
│   ├── __init__.py
│   ├── rules.py
│   ├── topology_engine.py
│   └── root_cause.py
│
├── telemetry/
│   ├── __init__.py
│   ├── generator.py
│   ├── visualize.py
│   └── dataset_builder.py
│
├── docs/
│
├── requirements.txt
├── .gitignore
└── README.md
```

------------------------------------------------------------------------

# ⚙️ Installation

## 1. Clone the repository

``` bash
git clone https://github.com/<your-username>/netpulse-ai.git
cd netpulse-ai
```

## 2. Create a virtual environment

### Windows

``` powershell
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

``` bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

``` bash
pip install -r requirements.txt
```

## 4. Configure Gemini

Create a `.env` file in the project root:

``` env
GEMINI_API_KEY=your_api_key_here
```

**Never commit `.env` or your API key to GitHub.**

------------------------------------------------------------------------

# ▶️ Running the Project

Run the Streamlit dashboard from the project root:

``` bash
streamlit run dashboard/app.py
```

The dashboard will open locally.

------------------------------------------------------------------------

# 🔄 Running Individual Components

### Generate telemetry

``` bash
python -m telemetry.generator
```

### Build controlled dataset

``` bash
python -m telemetry.dataset_builder
```

### Train and evaluate anomaly detector

``` bash
python -m models.anomaly_detector
```

### Run RCA

``` bash
python -m rca.root_cause
```

### Evaluate RCA

``` bash
python -m evaluation.rca_evaluation
```

### Test GenAI report

``` bash
python -m agent.gemini_agent
```

### Run interactive AI troubleshooting

``` bash
python -m agent.chat_agent
```

------------------------------------------------------------------------

# 🔐 Security

The following files should **never** be pushed to GitHub:

``` text
.env
API keys
credentials
private configuration
```

Recommended `.gitignore` entries:

``` gitignore
venv/
.env
__pycache__/
*.pyc
.ipynb_checkpoints/
```

------------------------------------------------------------------------

# ⚠️ Current Limitations

NetPulse AI is a **research / educational prototype**, not a production
network monitoring platform.

### Current limitations

-   Telemetry is synthetically generated.
-   The network topology is simulated in software.
-   No physical Junos device is required.
-   The prototype does not directly execute Junos commands.
-   RCA rules are deterministic rather than probabilistic.
-   The anomaly detector can produce false positives.
-   Gemini availability depends on the external API.
-   The current topology is intentionally small.
-   No automated configuration changes are performed.

These limitations are intentional to keep the prototype reproducible and
lightweight.

------------------------------------------------------------------------

# 🚀 Future Improvements

The architecture can be extended toward a more realistic network
assurance platform.

### Phase 1 --- Real Network Telemetry

``` text
Synthetic Telemetry
        ↓
Real Device Telemetry
        ↓
gNMI / OpenConfig
```

### Phase 2 --- More Advanced Detection

-   XGBoost incident classification
-   Time-series forecasting
-   Multivariate anomaly detection
-   Change-point detection
-   Explainable ML

### Phase 3 --- Advanced RCA

-   Probabilistic root-cause scoring
-   Dependency graphs
-   Service-level impact analysis
-   Multi-hop failure propagation
-   Historical incident correlation

### Phase 4 --- Network Automation

``` text
Detect
  ↓
Diagnose
  ↓
Recommend
  ↓
Human Approval
  ↓
Controlled Remediation
```

### Phase 5 --- Production Architecture

Potential components:

``` text
Network Devices
      ↓
Streaming Telemetry
      ↓
Message Broker
      ↓
Telemetry Processing
      ↓
ML Detection
      ↓
RCA Engine
      ↓
AI Assistant
      ↓
NOC Dashboard
```

------------------------------------------------------------------------

# 🎓 Why This Project Matters

NetPulse AI demonstrates the integration of multiple engineering areas
rather than treating AI as an isolated chatbot.

``` text
        Networking
            │
            ▼
       Telemetry
            │
            ▼
       Machine Learning
            │
            ▼
      Graph Algorithms
            │
            ▼
      Root-Cause Analysis
            │
            ▼
        Generative AI
            │
            ▼
       Visualization
```

The project demonstrates practical skills in:

-   Computer Networks
-   Network monitoring
-   Anomaly detection
-   Machine learning
-   Graph algorithms
-   Root-cause analysis
-   Generative AI
-   Prompt engineering
-   Data engineering
-   Interactive dashboards
-   Python software architecture

------------------------------------------------------------------------

# 💬 Interview Explanation

### 30-second version

> **NetPulse AI is a network assurance prototype that detects anomalous
> network telemetry, identifies likely root causes using network
> topology and deterministic evidence rules, and uses a grounded Gemini
> model to explain incidents and recommend troubleshooting steps. The
> system simulates network telemetry, injects controlled incidents,
> detects anomalies using Isolation Forest, performs topology-aware RCA
> using NetworkX, and presents everything through a Streamlit
> dashboard.**

### Key design decision

> **"I intentionally separated anomaly detection, root-cause analysis,
> and GenAI explanation. The ML and RCA layers determine what happened
> from telemetry, while the LLM is grounded on that evidence and is
> mainly responsible for explanation and interactive troubleshooting."**

------------------------------------------------------------------------

# ⭐ Key Results

``` text
┌─────────────────────────────────────────────┐
│              NETPULSE AI RESULTS            │
├─────────────────────────────────────────────┤
│                                             │
│  Telemetry Records                 40,000   │
│  Controlled Anomalies                   70 │
│                                             │
│  Precision                         77.14%   │
│  Recall                            77.14%   │
│  F1 Score                          77.14%   │
│                                             │
│  Controlled RCA Categories              4  │
│  Conditional RCA Accuracy            100%  │
│                                             │
│  AI Troubleshooting                ✓       │
│  Interactive Dashboard              ✓       │
│                                             │
└─────────────────────────────────────────────┘
```

------------------------------------------------------------------------

# 🧭 Project Philosophy

NetPulse AI follows a simple principle:

> **Detect with ML. Diagnose with evidence. Explain with GenAI.**

The goal is not to replace network engineers.

The goal is to reduce the time between:

**"Something is wrong."**

and

**"Here is the evidence, likely cause, and what should be investigated
next."**

------------------------------------------------------------------------

# 📜 License

This project is intended for educational, research, and portfolio
purposes.

------------------------------------------------------------------------

