FROM python:3.8

# Install MoviePy and FFMpeg
RUN pip install moviepy
RUN apt-get update && apt-get install -y ffmpeg

# Set the working directory
WORKDIR /app

# Copy your Python script into the container
COPY cutcut.py /app/cutcut.py

# Entry point for the Docker container
CMD ["python", "cutcut.py"]

