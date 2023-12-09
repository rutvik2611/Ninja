#!/bin/bash

echo "Starting to check for non-running or never started containers..."

for file in $(pwd)/src/docker-compose-files/*.yml
do
  service=$(basename $file .yml)
  echo "Checking service: $service"
  
  if [ "$(docker ps -a -q -f 'status=created' -f 'status=paused' -f 'status=restarting' -f 'status=removing' -f 'status=exited' -f 'status=dead' -f name=$service)" ]; then
    echo "Found non-running containers for service: $service. Starting them..."
    docker-compose -f $file up -d &
  elif [ -z "$(docker ps -a -q -f name=$service)" ]; then
    echo "No containers found for service: $service. Starting it..."
    docker-compose -f $file up -d &
  else
    echo "No non-running containers found for service: $service"
  fi
done

echo "Finished checking for non-running or never started containers."