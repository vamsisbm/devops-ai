# AI Tool Usage Policy

## Approved Tools
| Tool | Use For | Human Review Required |
|------|---------|----------------------|
| Amazon Bedrock (Claude) | Eval gate, log analysis, plan review | Yes — before acting on output |
| GitHub Copilot | Code completion | Yes — review all suggestions |
| Claude Code | Multi-file refactoring | Yes — review before commit |
| Amazon Q Developer | IaC suggestions | Yes — review before apply |

## Rules
1. AI recommends, humans decide — no AI output goes to production without review
2. No secrets in prompts — never include AWS keys, passwords, or PII
3. Eval gate threshold (3.5/5) must not be lowered without team discussion
4. Terraform destroy always requires human approval
5. Changes to evaluation/golden_set.json require a PR

## Cost Controls
- Claude 3 Haiku for scoring/diagnosis, Sonnet for user-facing responses only
- Delete OpenSearch collection when not using the lab
- $30/month AWS Budget alert is mandatory
