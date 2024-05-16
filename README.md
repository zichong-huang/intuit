
# Lambda Docker Project

This repository contains the code and Docker configuration for an AWS Lambda function managed through Docker containers and deployed via AWS ECR. GitHub Actions is set up to upload the Python code to ECR.

## Setup

Follow the instructions in `deploy.sh` to build and deploy the Lambda function.

## Deployment

Run the `deploy.sh` script to deploy your Docker container to AWS Lambda.

## Testing

```sh
python3 my-set-service/my-lambda-project/tests/test_api.py
```

# AWS Lambda and API Gateway Deployment

This AWS CloudFormation template deploys a Lambda function from a Docker image stored in ECR, with API Gateway integration. The template creates the necessary resources, including an IAM role for the Lambda function, the Lambda function itself, and an API Gateway setup with resources and methods.

## Table of Contents

- [Parameters](#parameters)
- [Resources Created](#resources-created)
- [Outputs](#outputs)
- [Deployment Instructions](#deployment-instructions)
- [Testing the API](#testing-the-api)
- [Cleanup](#cleanup)

## Parameters

- **applicationName**: The name of the application. Default is `"my-lambda"`.

## Resources Created

- **LambdaExecutionRole**: IAM Role for the Lambda function with permissions to write logs and access ECR.
- **LambdaFunction**: Lambda function created from a Docker image stored in ECR.
- **ApiGatewayRestApi**: API Gateway REST API.
- **ApiGatewayResourceAddItem**: API Gateway resource for adding an item.
- **ApiGatewayMethodAddItem**: API Gateway method for adding an item.
- **ApiGatewayResourceRemoveItem**: API Gateway resource for removing an item.
- **ApiGatewayMethodRemoveItem**: API Gateway method for removing an item.
- **ApiGatewayResourceHasItem**: API Gateway resource for checking if an item exists.
- **ApiGatewayMethodHasItem**: API Gateway method for checking if an item exists.
- **ApiGatewayResourceReset**: API Gateway resource for resetting the set.
- **ApiGatewayMethodReset**: API Gateway method for resetting the set.
- **ApiGatewayDeployment**: API Gateway deployment to the `prod` stage.
- **LambdaInvokePermission**: Lambda function invocation permission for API Gateway.

## Outputs

- **ApiURL**: URL of the API Gateway endpoint.

## Deployment Instructions

1. **Clone the Repository**:
    ```sh
    git clone <repository_url>
    ```

2. **Deploy the CloudFormation Stack**:
    ```sh
    aws cloudformation create-stack --stack-name my-lambda-stack --template-body file://cloudformation.yaml --capabilities CAPABILITY_NAMED_IAM
    ```

3. **Wait for the stack to be created**:
    Monitor the progress in the AWS CloudFormation console or using the AWS CLI:
    ```sh
    aws cloudformation describe-stacks --stack-name my-lambda-stack
    ```

## Testing the API

Once the stack is successfully created, you can test the API using the following endpoints:

1. **Add an Item**:
    ```sh
    curl -X POST https://7okw1aj4k2.execute-api.us-east-1.amazonaws.com/prod/addItem -H "Content-Type: application/json" -d '{"operation": "AddItem", "item": 20}'
    ```

2. **Remove an Item**:
    ```sh
    curl -X DELETE "https://7okw1aj4k2.execute-api.us-east-1.amazonaws.com/prod/removeItem?item=20" -H "Content-Type: application/json"
    ```

3. **Check if an Item Exists**:
    ```sh
    curl -X GET "https://7okw1aj4k2.execute-api.us-east-1.amazonaws.com/prod/hasItem?item=20" -H "Content-Type: application/json"
    ```

4. **Reset the Set**:
    ```sh
    curl -X POST https://7okw1aj4k2.execute-api.us-east-1.amazonaws.com/prod/resetSet -H "Content-Type: application/json" -d '{"operation": "Reset"}'
    ```

## Cleanup

To delete the resources created by this CloudFormation stack, use the following command:

```sh
aws cloudformation delete-stack --stack-name my-lambda-stack
```
