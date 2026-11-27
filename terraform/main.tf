terraform {
  required_providers { aws = { source = "hashicorp/aws", version = "~> 5.0" } }
  backend "s3" {
    bucket         = "my-lab-tf-state-YOUR_AWS_ACCOUNT_ID"
    key            = "devops-ai-lab/terraform.tfstate"
    region         = "us-east-2"
    dynamodb_table = "my-lab-tf-locks"
    encrypt        = true
  }
}
provider "aws" { region = var.aws_region }

resource "aws_s3_bucket" "kb_docs" {
  bucket = "my-lab-kb-docs-${var.account_id}"
}
resource "aws_s3_bucket_public_access_block" "kb_docs" {
  bucket                  = aws_s3_bucket.kb_docs.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
resource "aws_ecr_repository" "agent" {
  name                 = "my-lab-agent"
  image_tag_mutability = "IMMUTABLE"
  image_scanning_configuration { scan_on_push = true }
}
resource "aws_iam_role" "agentcore" {
  name = "AgentCoreLabRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect    = "Allow"
      Principal = { Service = "bedrock-agentcore.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }]
  })
}
resource "aws_iam_role_policy" "agentcore" {
  name = "AgentCoreLabPolicy"
  role = aws_iam_role.agentcore.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow"
        Action = ["bedrock:InvokeModel","bedrock:Retrieve","bedrock:RetrieveAndGenerate"]
        Resource = "*" },
      { Effect = "Allow"
        Action = ["ecr:GetDownloadUrlForLayer","ecr:BatchGetImage","ecr:GetAuthorizationToken"]
        Resource = "*" }
    ]
  })
}
