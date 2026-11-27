import boto3, asyncio, json, os
from datetime import datetime, timezone

bedrock = boto3.client("bedrock-runtime", region_name="us-east-2")
REGIONS = ["us-east-2", "us-east-1"]

async def collect(service, op, key, region):
    try:
        client = boto3.Session().client(service, region_name=region)
        r = getattr(client, op)()
        return {"service": service, "region": region, "count": len(r.get(key, []))}
    except Exception as e:
        return {"service": service, "region": region, "error": str(e)}

async def main():
    tasks = [collect(s, o, k, r) for r in REGIONS
             for s, o, k in [
                 ("ec2",    "describe_instances",    "Reservations"),
                 ("lambda", "list_functions",         "Functions"),
                 ("rds",    "describe_db_instances",  "DBInstances")
             ]
    ] + [
        collect("s3",  "list_buckets", "Buckets", "us-east-2"),
        collect("iam", "list_users",   "Users",   "us-east-2")
    ]
    results = await asyncio.gather(*tasks)
    summary = json.dumps(results, indent=2)
    prompt = f"Review this AWS inventory. Flag: errors, high counts, cost savings, security gaps.\n\n{summary}"
    r = bedrock.converse(modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0, "maxTokens": 800})
    findings = r["output"]["message"]["content"][0]["text"]
    os.makedirs("inventory", exist_ok=True)
    date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    with open("inventory/findings.md", "w") as f:
        f.write(f"# Findings — {date_str}\n\n{findings}")
    print("Done. See inventory/findings.md")

asyncio.run(main())
