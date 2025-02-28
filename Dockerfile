FROM python:3.9-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install pipenv
RUN pip install pipenv

# Install any needed packages specified in Pipfile.lock
RUN pipenv install --ignore-pipfile

# # Install curl
# RUN apt-get update && apt-get install -y curl

# # # Download the PostgreSQL CA certificate
# RUN mkdir -p ~/.postgresql

# Make port 8000 available to the world outside this container
EXPOSE 8000

# # # Run the command to start FastAPI
# # # CMD ["pipenv", "run", "uvicorn", "flash_fast_api.flash_fast_api:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["pipenv", "run", "uvicorn", "flash_fast_api.flash_fast_api:app", "--host", "0.0.0.0", "--port", "8000"]
# 'pipenv run uvicorn flash_fast_api.flash_fast_api:app --host 0.0.0.0 --port 8000'

# # Run an infinite loop to keep the container running
# CMD ["tail", "-f", "/dev/null"]