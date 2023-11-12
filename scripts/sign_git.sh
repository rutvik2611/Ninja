#!/bin/bash

# Function to check if a command exists
command_exists() {
    type "$1" &> /dev/null
}

echo "Checking for GPG installation..."

# Check if GPG is installed
if command_exists gpg; then
    echo "GPG is already installed."
else
    echo "Installing GPG..."
    # Use appropriate package manager based on the OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update && sudo apt-get install -y gnupg
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # Assuming Homebrew is installed on macOS
        brew install gnupg
    else
        echo "Unsupported operating system."
        exit 1
    fi
    echo "GPG installation complete."
fi

# Function to delete existing GPG keys
delete_existing_keys() {
    echo "Existing GPG keys:"
    gpg --list-secret-keys --keyid-format LONG

    read -p "Do you want to delete all existing GPG keys? (yes/no): " delete_keys
    if [[ "$delete_keys" == "yes" ]]; then
        gpg --list-secret-keys --keyid-format LONG | grep sec | awk '{print $2}' | awk -F'/' '{print $2}' | while read -r keyid; do
            echo "Deleting key: $keyid"
            gpg --batch --yes --delete-secret-key "$keyid"
            gpg --batch --yes --delete-key "$keyid"
        done
        echo "All existing GPG keys have been deleted."
    else
        echo "Skipping deletion of existing GPG keys."
    fi
}

# Offer to delete existing keys
delete_existing_keys

# Generate a new GPG key
echo "Generating a new GPG key with default size 4096 and no expiration..."
gpg --full-generate-key --default-key 4096 --default-new-key-algo rsa4096 --gen-key --pinentry-mode loopback

# Extract the GPG key ID
echo "Extracting the GPG key ID..."
key_id=$(gpg --list-secret-keys --keyid-format LONG | grep sec | awk '{print $2}' | awk -F'/' '{print $2}')
echo "GPG key ID: $key_id"

# Ask user if they want to configure Git for commit signing
read -p "Do you want to configure Git to use GPG key for commit signing? (yes/no): " configure_git
if [[ "$configure_git" == "yes" ]]; then
    # Configure Git to use the GPG key for signing commits
    echo "Configuring Git to use GPG key for commit signing..."
    git config --global user.signingkey "$key_id"
    echo "git config --global user.signingkey $key_id"

    git config --global commit.gpgsign true
    echo "git config --global commit.gpgsign true"

    # Test to validate GPG key works for signing
    echo "Testing GPG key for signing..."
    echo "test message" | gpg --clearsign > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        echo "GPG key test successful. Signing works as expected."
    else
        echo "GPG key test failed. Please check your GPG setup."
    fi

    echo "Git has been configured to use the GPG key with ID $key_id for signing commits."
else
    echo "Skipping Git configuration for commit signing."
fi

# Provide an option to undo settings
read -p "Do you want to undo all settings and disable GPG signing for Git? (yes/no): " undo_settings
if [[ "$undo_settings" == "yes" ]]; then
    git config --global --unset user.signingkey
    git config --global commit.gpgsign false
    echo "All Git GPG settings have been reset. GPG signing is no longer required.."
fi
