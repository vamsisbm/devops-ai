import boto3, re, os
from datetime import datetime, timezone

bedrock = boto3.client("bedrock-runtime", region_name="us-east-2")
logs   = boto3.client("logs",            region_name="us-east-2")
LOG_GROUP = "/aws/lambda/my-lab-agent"

def sanitise(text):
    for pattern in [r"AKIA[0-9A-Z]{16}", r"password[=:\s]+\S+"]:
        text = re.sub(pattern, "[REDACTED]", text, flags=re.IGNORECASE)
    return text

def get_errors():
    now = int(datetime.now(timezone.utc).timestamp() * 1000)
    try:
        r = logs.filter_log_events(
            logGroupName=LOG_GROUP,
            startTime=now - 3_600_000,
            endTime=now,
            filterPattern="ERROR"
        )
        return [e["message"] for e in r.get("events", [])]
    except Exception as e:
        print(f"Log fetch error: {e}"); return []

if __name__ == "__main__":
    errors = get_errors()
    if not errors:
        print("No errors found."); exit(0)
    log_text = sanitise("\n".join(errors[:50]))
    prompt = (
        "Analyse these log errors. Return:\n"
        "root_cause, severity (HIGH/MEDIUM/LOW), remediation_steps, runbook_entry.\n\n"
        + log_text
    )
    r = bedrock.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0, "maxTokens": 800}
    )
    analysis = r["output"]["message"]["content"][0]["text"]
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    os.makedirs("incidents", exist_ok=True)
    with open(f"incidents/{date_str}.md", "w") as f:
        f.write(f"# Incident Report — {date_str}\n\n**Errors:** {len(errors)}\n\n## AI Analysis\n\n{analysis}")
    print(f"Written to incidents/{date_str}.md")
