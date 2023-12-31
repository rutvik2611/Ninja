#!/bin/bash

# Bring all Docker Compose files down in parallel
for file in $(pwd)/src/docker-compose-files/*.yml
do
  docker-compose -f $file down --remove-orphans &
done

# Wait for all background jobs to finish
wait

# Bring all Docker Compose files up in parallel
for file in $(pwd)/src/docker-compose-files/*.yml
do
  docker-compose -f $file up -d &
done

# Wait for all background jobs to finish
wait