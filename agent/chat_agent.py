import os
import time

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


def answer_question(question, device, interface):

    # Collect evidence from NetPulse AI
    metrics = get_device_metrics(device)

    interface_data = get_interface_status(
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
You are NetPulse AI, a network troubleshooting assistant.

Answer the user's networking question using ONLY the
provided telemetry and RCA evidence.

Do not invent telemetry values.

The RCA engine has already determined the root cause.
Do not replace or contradict the RCA result.

You may explain the evidence and provide recommended
troubleshooting steps.

USER QUESTION:
{question}

DEVICE:
{device}

INTERFACE:
{interface}

CURRENT DEVICE METRICS:
{metrics}

INTERFACE DATA:
{interface_data}

RCA EVIDENCE:
{rca}

RECENT HISTORY:
{history}

Answer clearly and concisely.

If recommending Junos troubleshooting commands,
clearly label them as "Recommended Junos commands"
because this prototype does not directly execute commands
on a physical Junos device.
"""

    # Retry temporary Gemini 503 errors
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            return response.text

        except Exception as e:

            error_text = str(e)

            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < 2:

                    wait_time = 2 ** attempt

                    print(
                        f"\nGemini temporarily unavailable. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:

                    return (
                        "Gemini is temporarily unavailable.\n\n"
                        "The underlying NetPulse AI analysis "
                        "is still available.\n\n"
                        f"RCA Root Cause: "
                        f"{rca.get('root_cause', 'Unknown')}\n"
                        f"Anomaly Score: "
                        f"{rca.get('anomaly_score', 'Unknown')}\n"
                        f"Packet Loss: "
                        f"{rca.get('packet_loss_percent', 'Unknown')}%\n"
                        f"Packet Errors: "
                        f"{rca.get('packet_errors', 'Unknown')}\n"
                        f"Interface Flaps: "
                        f"{rca.get('interface_flaps', 'Unknown')}"
                    )

            else:
                raise


def main():

    print("=" * 70)
    print("NETPULSE AI — INTERACTIVE NETWORK TROUBLESHOOTING")
    print("=" * 70)

    device = input("\nDevice [SW2]: ").strip() or "SW2"

    interface = input(
        "Interface [Gi0/2]: "
    ).strip() or "Gi0/2"

    print("\nType 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":

            print("\nNetPulse AI session ended.")
            break

        try:

            answer = answer_question(
                question,
                device,
                interface
            )

            print("\nNetPulse AI:")
            print(answer)
            print()

        except Exception as e:

            print("\nError:")
            print(e)


if __name__ == "__main__":
    main()