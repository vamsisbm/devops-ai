#!/bin/bash
IMAGE_URI=$1
SERVICE_NAME="my-lab-agent"
aws ecr get-login-password --region us-east-2 \
  | docker login --username AWS --password-stdin \
    YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-2.amazonaws.com
docker pull $IMAGE_URI
docker stop $SERVICE_NAME 2>/dev/null || true
docker rm   $SERVICE_NAME 2>/dev/null || true
docker run -d --name $SERVICE_NAME --restart unless-stopped -p 8080:8080 $IMAGE_URI
sleep 5 && curl -f http://localhost:8080/ping && echo "Health check passed" || echo "FAILED"
