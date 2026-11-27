import boto3, argparse, subprocess

bedrock = boto3.client("bedrock-runtime", region_name="us-east-2")

def diagnose(job_context, pr_number):
    prompt = (
        f"CI/CD pipeline failed. Context:\n{job_context}\n\n"
        "Provide: 1) Root cause  2) Suggested fix  3) Confidence. Markdown format."
    )
    r = bedrock.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"temperature": 0, "maxTokens": 500}
    )
    diagnosis = r["output"]["message"]["content"][0]["text"]
    if pr_number and pr_number != "None":
        subprocess.run(
            ["gh", "pr", "comment", pr_number,
             "--body", f"## AI Pipeline Diagnosis\n\n{diagnosis}"],
            check=False
        )
    print(diagnosis)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--job-context", required=True)
    p.add_argument("--pr-number",   default="None")
    a = p.parse_args()
    diagnose(a.job_context, a.pr_number)
