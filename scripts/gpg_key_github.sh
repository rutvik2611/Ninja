#!/bin/bash

echo "Before starting, let's check if GPG keychain is installed..."
if ! command -v gpg &> /dev/null; then
  echo "GPG keychain not found. Checking if Homebrew is installed..."
  if ! command -v brew &> /dev/null; then
    echo "Homebrew not found. Please install Homebrew to proceed with GPG installation."
    exit 1
  else
    echo "Homebrew found. Installing GPG..."
    brew install gpg
  fi
fi

echo "Checking for existing GPG keys..."
keys=$(gpg --list-secret-keys --keyid-format=long)

if [[ -n "$keys" ]]; then
  echo "Existing keys found:"
  echo "$keys"
  echo "Would you like to use any existing key? (Type the key number or 'no' to generate a new key)"
  read key_choice

  if [ "$key_choice" != "no" ]; then
    key_id=$(echo "$keys" | sed -n "${key_choice}p" | grep -E -o '[A-F0-9]{40}')
    echo "Using selected key: $key_id"
  else
    echo "Generating a new GPG key..."
    gpg --full-generate-key
    key_id=$(gpg --list-secret-keys --keyid-format=long | grep -E -o '[A-F0-9]{40}')
  fi
else
  echo "No existing keys found. Generating a new GPG key..."
  gpg --full-generate-key
  key_id=$(gpg --list-secret-keys --keyid-format=long | grep -E -o '[A-F0-9]{40}')
fi

echo "Exporting GPG key..."
gpg --armor --export $key_id | pbcopy  # Copy key to clipboard (Mac)

echo "The GPG key has been copied to the clipboard."

echo "Steps to copy the key for SSH & GPG:"
echo "1. Open GitHub"
echo "2. Go to Settings > SSH and GPG keys"
echo "3. Click on 'New GPG key' or 'Add SSH key'"
echo "4. Paste the copied GPG key into the provided field"
echo "5. Save the key"

echo "Have you uploaded the GPG key to GitHub? (Type 'yes' if done)"
read uploaded

if [ "$uploaded" != "yes" ]; then
  echo "Please upload the GPG key to GitHub."
  exit 1
fi

validate_key() {
  echo "Testing GPG key..."
  echo "This is a test message." | gpg --encrypt --armor --recipient $key_id > /dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "The GPG key works!"
    return 0
  else
    return 1
  fi
}

tries=0
max_tries=3
while ! validate_key; do
  tries=$((tries+1))
  if [ $tries -eq $max_tries ]; then
    echo "Failed to validate the GPG key after $max_tries attempts."
    exit 1
  fi
  echo "Validation failed. Retrying..."
done

# Function to set GPG key for Git
set_git_gpg_key() {
  git config --global user.signingkey "$key_id"
  git config --global commit.gpgsign true
  echo "GPG key has been set for Git."
}

# Check if the key was generated or selected
if [ -n "$key_id" ]; then
  set_git_gpg_key
  if validate_git_gpg_key; then
    echo "Git GPG key configuration validated successfully."
  else
    echo "Git GPG key configuration validation failed."
    exit 1
  fi
else
  echo "No GPG key found. Unable to set Git configuration."
  exit 1
fi
