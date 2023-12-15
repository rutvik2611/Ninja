# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install pipenv
RUN pip install pipenv

# Install any needed packages specified in Pipfile.lock
RUN pipenv install --ignore-pipfile

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run the command to start FastAPI
CMD ["pipenv", "run", "uvicorn", "flash_fast_api.flash_fast_api:app", "--host", "0.0.0.0", "--port", "8000"]