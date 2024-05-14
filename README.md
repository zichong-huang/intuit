# Lambda Docker Project

This repository contains the code and Docker configuration for an AWS Lambda function managed through Docker containers and deployed via AWS ECR.

## Setup

Follow the instructions in `deploy.sh` to build and deploy the Lambda function.

## Deployment

Run the `deploy.sh` script to deploy your Docker container to AWS Lambda.

## Testing 
python -m unittest tests/test_lambda_function.py
