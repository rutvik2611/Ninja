#!/bin/bash

# Create a temporary directory
TEMP_DIR=$(mktemp -d)
mkdir -p $TEMP_DIR/python

# Create a virtual environment
python3 -m venv $TEMP_DIR/venv
source $TEMP_DIR/venv/bin/activate

# Install required packages
pip install -t $TEMP_DIR/python sqlalchemy sqlalchemy-cockroachdb psycopg2-binary

# Deactivate the virtual environment
deactivate

# Create the ZIP archive
zip -r python.zip -j $TEMP_DIR/python/*

# Clean up the temporary directory
rm -rf $TEMP_DIR
