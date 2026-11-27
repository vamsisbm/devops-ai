# DevOps AI Lab — github.com/vamsisbm/devops-ai

> Recovered from AWS Assistant for review. Workflow templates are under `workflow-templates/` and GitHub Actions will not discover them there. Replace `YOUR_AWS_ACCOUNT_ID` and other placeholders, review IAM permissions and deployment commands, and validate the AWS setup before installing the templates in `.github/workflows/`.

Personal AWS lab: AI-enabled DevOps with Amazon Bedrock, AgentCore, and GitHub Actions.

## Projects
| # | Project | AWS Services |
|---|---------|-------------|
| 1 | AI CI/CD Pipeline + LLM eval gate | Bedrock, ECR, AgentCore |
| 2 | Terraform + AI plan review | Bedrock, CloudTrail |
| 3 | RAG Knowledge Base | Bedrock KB, OpenSearch Serverless |
| 4 | CloudWatch log analyser | CloudWatch, Bedrock |
| 5 | boto3 inventory collector | boto3, Bedrock |
| 6 | On-prem hybrid deploy | SSM, CloudWatch Agent |

## Quick Start
1. Enable Bedrock model access in us-east-2
2. Run: cd terraform && terraform init && terraform apply
3. Create Bedrock Knowledge Base (NextGen OpenSearch Serverless)
4. Update KB_ID in .github/workflows/deploy-agent.yml and agent/app.py
5. Review and validate the workflow templates before enabling them.

## Cost: ~$10-30/month
Critical: Choose NextGen (not Classic) OpenSearch when creating the Knowledge Base.
