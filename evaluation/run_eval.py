import json, boto3, sys, argparse, re

bedrock = boto3.client("bedrock-runtime", region_name="us-east-2")
bedrock_agent = boto3.client("bedrock-agent-runtime", region_name="us-east-2")
JUDGE_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"
JUDGE_PROMPT = "Score ANSWER vs EXPECTED 1-5. Output ONLY the integer.\nEXPECTED: {expected}\nANSWER: {actual}\nScore:"

def get_answer(kb_id, query):
    r = bedrock_agent.retrieve_and_generate(
        input={"text": query},
        retrieveAndGenerateConfiguration={"type": "KNOWLEDGE_BASE",
            "knowledgeBaseConfiguration": {"knowledgeBaseId": kb_id,
                "modelArn": "arn:aws:bedrock:us-east-2::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"}})
    return r["output"]["text"]

def score(expected, actual):
    r = bedrock.converse(modelId=JUDGE_MODEL,
        messages=[{"role": "user", "content": [{"text": JUDGE_PROMPT.format(expected=expected, actual=actual)}]}],
        inferenceConfig={"temperature": 0, "maxTokens": 10})
    m = re.search(r"\d", r["output"]["message"]["content"][0]["text"])
    return int(m.group()) if m else 1

def main(kb_id):
    data = json.load(open("evaluation/golden_set.json"))
    total = sum(score(i["expected_answer"], get_answer(kb_id, i["query"])) for i in data)
    avg = total / len(data)
    print(f"Average: {avg:.2f}/5")
    sys.exit(0 if avg >= 3.5 else 1)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--kb-id", required=True)
    main(p.parse_args().kb_id)
