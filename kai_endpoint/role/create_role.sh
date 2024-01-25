#!/bin/bash

# Define the role name and trust policy file
ROLE_NAME="lambda-ex"
TRUST_POLICY="trust-policy.json"

# Create the trust policy file
cat > $TRUST_POLICY << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create a new IAM role with the trust policy
ROLE_ARN=$(aws iam create-role --role-name $ROLE_NAME --assume-role-policy-document file://$TRUST_POLICY --query 'Role.Arn' --output text)

# Attach the AWSLambdaBasicExecutionRole policy to the role
aws iam attach-role-policy --role-name $ROLE_NAME --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Clean up the trust policy file
rm $TRUST_POLICY

# Print the ARN of the role
echo "Created role with ARN: $ROLE_ARN"