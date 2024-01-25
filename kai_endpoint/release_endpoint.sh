#!/bin/bash

# Echo every command that is executed
set -x

# Define the function name and region
FUNCTION_NAME="kai_lambda"
REGION="us-west-2"  # Updated to use us-west-2

# Define the log file
LOG_FILE="script.log"

# Redirect all output to the log file
exec > >(tee -a $LOG_FILE)
exec 2>&1

# Create a new HTTP API
API_ID=$(aws apigatewayv2 create-api --name "${FUNCTION_NAME}_api" --protocol-type HTTP --region $REGION --query 'ApiId' --output text)

# Create an integration with the Lambda function
INTEGRATION_ID=$(aws apigatewayv2 create-integration --api-id $API_ID --integration-type AWS_PROXY --integration-method POST --integration-uri arn:aws:lambda:$REGION:<account-id>:function:$FUNCTION_NAME --region $REGION --query 'IntegrationId' --output text)

# Create a new route for the GET method
aws apigatewayv2 create-route --api-id $API_ID --route-key 'GET /{user}/{rsa}' --target integrations/$INTEGRATION_ID --region $REGION

# Deploy the API
aws apigatewayv2 create-deployment --api-id $API_ID --region $REGION

echo "HTTP API created with URL: https://$API_ID.execute-api.$REGION.amazonaws.com"