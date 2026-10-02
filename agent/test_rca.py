from agent.rca_tool import analyze_incident

result = analyze_incident("SW2", "Gi0/2")

print("\n=== RCA RESULT ===")

for key, value in result.items():
    print(f"{key}: {value}")