#!/bin/bash

# Load AWS credentials from .env file
source .env

# Export the variables so they are available to subprocesses
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION
export AWS_DEFAULT_OUTPUT_FORMAT

# Print the variables to verify they were loaded correctly
echo "AWS Access Key ID: $AWS_ACCESS_KEY_ID"
echo "AWS Secret Access Key: $AWS_SECRET_ACCESS_KEY"
echo "Default region name: $AWS_DEFAULT_REGION"
echo "Default output format: $AWS_DEFAULT_OUTPUT_FORMAT"