import os
import sys

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from decimal import Decimal

# Input video directory path inside the Docker container
input_directory = '/app/input'

# List all files in the input directory
input_files = os.listdir(input_directory)

# Filter for MP4 files
mp4_files = [file for file in input_files if file.endswith(".mp4")]

if len(mp4_files) == 1:
    # If there is only one MP4 file, rename it to 'original_file.mp4'
    input_video = os.path.join(input_directory, 'original_file.mp4')
    os.rename(os.path.join(input_directory, mp4_files[0]), input_video)
    print(f"Renamed input file to {input_video}")
else:
    print("Error: There should be one and only one MP4 file in the input directory.")
    sys.exit(1)

# Parse the durations as a comma-separated string to convert to a list of floats
durations_str = os.getenv("DURATIONS")
durations = [float(dur) for dur in durations_str.split(",")]

# Output video file names
output_videos = []

# Calculate the end times based on the given durations
end_times = [sum(durations[:i]) for i in range(1, len(durations) + 1)]

# Set the output directory
output_directory = "/app/output_directory"  # You can change this path

# Cut the video based on the end times
for i, end_time in enumerate(end_times):
    start_time = end_times[i - 1] if i > 0 else 0
    output_video = os.path.join(output_directory, f"output_{i + 1}.mp4")

    # Check if the output file already exists and remove it
    if os.path.exists(output_video):
        os.remove(output_video)

    output_videos.append(output_video)
    ffmpeg_extract_subclip(input_video, start_time, end_time, targetname=output_video)

# Print the list of output video file names and their respective lengths
for i, output_video in enumerate(output_videos):
    start_time = end_times[i - 1] if i > 0 else 0
    length = durations[i]
    print(f"Cut video {i + 1}: Start Time: {start_time} seconds, End Time: {start_time + length} seconds, Length: {length} seconds")
