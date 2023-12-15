#!/bin/bash

# Get the current WiFi network
network=$(networksetup -getairportnetwork en0 | cut -d ":" -f 2 | xargs)

# Print the network name
echo "Current network: $network"

# Check if the network is "jpmc visitor wifi"
if [ "$network" = "JPMCVisitor" ]; then
    python3 main.py
fi