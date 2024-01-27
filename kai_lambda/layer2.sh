#!/bin/bash

# Create a temporary directory in the current directory
TEMP_DIR=$(mktemp -d -p ./)
mkdir -p $TEMP_DIR/python


# Install required packages
# pip install --platform manylinux2014_x86_64 --target=$TEMP_DIR/python --implementation cp --python 3.9 --only-binary=:all: --upgrade psycopg2-binary
pip install -t $TEMP_DIR/python sqlalchemy
pip install -t $TEMP_DIR/python sqlalchemy-cockroachdb
#pip install --platform manylinux2014_x86_64 --target=$TEMP_DIR/python --implementation cp --python-version 3.9 --only-binary=:all: --upgrade psycopg2-binary


# Create the ZIP archive
cd $TEMP_DIR
zip -r python2.zip python

echo "ZIP archive created at $TEMP_DIR/python2.zip"

## Clean up the temporary directory
#rm -rf $TEMP_DIR
