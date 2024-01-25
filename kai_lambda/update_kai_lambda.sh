#!/bin/bash

# Define the role ARN
ROLE_ARN="arn:aws:iam::884919981963:role/lambda-ex"  # Replace with your AWS account ID and role name

# Package the Lambda function code
zip function.zip main.py

# Update the Lambda function code
aws lambda update-function-code --function-name kai_lambda --zip-file fileb://function.zip

# Clean up the zip file
rm function.zip