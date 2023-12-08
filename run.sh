#!/bin/bash

for file in $(pwd)/src/docker-compose-files/*.yml
do
  docker-compose -f $file down --remove-orphans
  docker-compose -f $file up -d
done