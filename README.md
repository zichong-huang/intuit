# Lambda Docker Project

This repository contains the code and Docker configuration for an AWS Lambda function managed through Docker containers and deployed via AWS ECR.
Github Actions is setup to able to upload the python to ECR.

## Setup

Follow the instructions in `deploy.sh` to build and deploy the Lambda function.

## Deployment

Run the `deploy.sh` script to deploy your Docker container to AWS Lambda.

## Testing 
python3 my-set-service/my-lambda-project/tests/test_api.py

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
- **ApiGatewayDeployment**: API Gateway deployment to the `prod` stage.
- **LambdaInvokePermission**: Lambda function invocation permission for API Gateway.

## Outputs

- **ApiURL**: URL of the API Gateway endpoint.

## Deployment Instructions

1. **Clone the Repository**:
    ```sh
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Deploy the CloudFormation Stack**:
    ```sh
    aws cloudformation create-stack --stack-name my-lambda-stack --template-body file://path/to/cloudformation.yaml --capabilities CAPABILITY_NAMED_IAM
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
    curl -X POST https://<ApiURL>/prod/addItem -H "Content-Type: application/json" -d '{"operation": "AddItem", "item": "item_value"}'
    ```

2. **Remove an Item**:
    ```sh
    curl -X DELETE https://<ApiURL>/prod/removeItem -H "Content-Type: application/json" -d '{"operation": "RemoveItem", "item": "item_value"}'
    ```

3. **Check if an Item Exists**:
    ```sh
    curl -X GET "https://<ApiURL>/prod/hasItem?operation=HasItem&item=item_value"
    ```

Replace `<ApiURL>` with the value of `ApiURL` output from the CloudFormation stack.

## Cleanup

To delete the resources created by this CloudFormation stack, use the following command:

```sh
aws cloudformation delete-stack --stack-name my-lambda-stack
