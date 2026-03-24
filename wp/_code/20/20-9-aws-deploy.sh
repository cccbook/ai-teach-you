#!/bin/bash
set -e

echo "Deploying to AWS..."

ECR_REPOSITORY="myapp"
ECR_IMAGE="${ECR_REGISTRY}/${ECR_REPOSITORY}:${GITHUB_SHA}"

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_REGISTRY

docker build -t $ECR_IMAGE ./backend
docker push $ECR_IMAGE

aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE --force-new-deployment

aws ecs wait services-stable --cluster $ECS_CLUSTER --services $ECS_SERVICE

echo "Deployment complete!"
