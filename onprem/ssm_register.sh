#!/bin/bash
# Step 1: Generate activation first in AWS console or via:
# aws ssm create-activation --region us-east-2 --iam-role service-role/AmazonEC2RunCommandRoleForManagedInstances
REGION=us-east-2
sudo yum install -y amazon-ssm-agent 2>/dev/null || sudo apt-get install -y amazon-ssm-agent 2>/dev/null
sudo amazon-ssm-agent -register \
  -code "YOUR_ACTIVATION_CODE" \
  -id   "YOUR_ACTIVATION_ID" \
  -region $REGION
sudo systemctl start amazon-ssm-agent && sudo systemctl enable amazon-ssm-agent
echo "Verify: https://us-east-2.console.aws.amazon.com/systems-manager/fleet-manager"
