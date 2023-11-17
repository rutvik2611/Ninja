#!/bin/bash

# Function to check if a command is available
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check if fortune is installed
if ! command_exists fortune; then
  echo "Installing fortune..."
  brew install fortune
fi

# Check if cowsay is installed
if ! command_exists cowsay; then
  echo "Installing cowsay..."
  brew install cowsay
fi

# Find the installation directory of cowsay
cowsay_dir=$(dirname $(dirname $(which cowsay)))/share/cows

# Append fortune | cowsay command to .zshrc
echo "fortune | cowsay \$(ls \"$cowsay_dir\" | sort -R | head -n 1 | sed 's/\\.cow//')" >> ~/.zshrc

echo "Setup complete!"
