import boto3, argparse, subprocess, sys

bedrock = boto3.client("bedrock-runtime", region_name="us-east-2")

def review(plan_file, pr_number):
    plan = open(plan_file).read()[:8000]
    prompt = (
        "Review this Terraform plan. Flag:\n"
        "1) Resource deletions  2) IAM changes  3) Security group changes  4) Cost impact\n"
        "Recommend: APPROVE / REQUEST CHANGES / BLOCK\n\n" + plan
    )
    r = bedrock.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0, "maxTokens": 1000}
    )
    result = r["output"]["message"]["content"][0]["text"]
    if pr_number and pr_number != "None":
        subprocess.run(
            ["gh", "pr", "comment", pr_number,
             "--body", f"## AI Terraform Plan Review\n\n{result}"],
            check=False
        )
    print(result)
    if "BLOCK" in result.upper():
        sys.exit(1)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--plan-file",  required=True)
    p.add_argument("--pr-number",  default="None")
    a = p.parse_args()
    review(a.plan_file, a.pr_number)
