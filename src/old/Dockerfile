# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies if required (e.g., using pip)
# RUN pip install -r requirements.txt

# Specify the command to run your Python main file
CMD ["python", "src/main.py"]

