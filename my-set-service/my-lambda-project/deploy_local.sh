#!/bin/bash

# Define variables
ECR_REPOSITORY=732385684161.dkr.ecr.us-east-1.amazonaws.com/my-lambda-function
REGION=us-east-1
IMAGE_TAG=latest

# Build the Docker image
docker buildx build --platform linux/arm64 -t my-lambda-function .

# Authenticate to ECR
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_REPOSITORY

# Tag the Docker image
docker tag my-lambda-function:latest $ECR_REPOSITORY:$IMAGE_TAG

# Push the Docker image to ECR
docker push $ECR_REPOSITORY:$IMAGE_TAG

# # Update the Lambda function with the new image
aws lambda update-function-code --function-name intuit-set-application-LambdaFunction-9gSVnNrzmsFd --image-uri $ECR_REPOSITORY:$IMAGE_TAG --region $REGION
