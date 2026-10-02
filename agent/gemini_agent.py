import os
from dotenv import load_dotenv
from google import genai

from agent.tools import (
    get_device_metrics,
    get_interface_status,
    get_incident_history
)

from agent.rca_tool import analyze_incident


load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_with_ai(device, interface):

    # Collect evidence from our system
    metrics = get_device_metrics(device)

    interface_status = get_interface_status(
        device,
        interface
    )

    rca = analyze_incident(
        device,
        interface
    )

    history = get_incident_history(
        device,
        interface
    )

    prompt = f"""
You are an AI network troubleshooting assistant.

You are analyzing a network incident detected by a
student-built network assurance system.

IMPORTANT:
Do not invent telemetry values.
Do not change the root cause determined by the RCA engine.
Use only the evidence provided below.

Your job is to:
1. Explain what happened.
2. Explain the evidence supporting the root cause.
3. Identify the likely severity.
4. Recommend practical troubleshooting steps.
5. Mention affected device/interface.
6. Clearly distinguish observed evidence from recommendations.

NETWORK DEVICE METRICS:
{metrics}

INTERFACE STATUS:
{interface_status}

RCA RESULT:
{rca}

RECENT INCIDENT HISTORY:
{history}

Return the response in this format:

INCIDENT ANALYSIS

Device:
Interface:

Severity:

Root Cause:

Evidence:
- ...
- ...
- ...

Explanation:
...

Recommended Troubleshooting:
1. ...
2. ...
3. ...
4. ...

Important:
The root cause must remain exactly consistent with the RCA result.
Do not claim certainty beyond the available evidence.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text


if __name__ == "__main__":

    result = analyze_with_ai(
        "SW2",
        "Gi0/2"
    )

    print("\n")
    print("=" * 70)
    print("NETPULSE AI — GENAI TROUBLESHOOTING REPORT")
    print("=" * 70)
    print(result)