#!/bin/bash

# Define the role ARN
ROLE_ARN="arn:aws:iam::884919981963:role/lambda-ex"  # Replace with your AWS account ID and role name

# Package the Lambda function code
zip function.zip main.py

# Create the Lambda function
aws lambda create-function --function-name kai_lambda --zip-file fileb://function.zip --handler main.lambda_handler --runtime python3.8 --role $ROLE_ARN

# Clean up the zip file
rm function.zip