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
    local existing_keys
    existing_keys=$(gpg --list-secret-keys --keyid-format LONG)

    if [[ -z "$existing_keys" ]]; then
        echo "No existing GPG keys found."
        return
    fi

    echo "Existing GPG keys:"
    echo "$existing_keys"

    echo "$existing_keys" | grep sec | while read -r line; do
        local keyid=$(echo $line | awk '{print $2}' | awk -F'/' '{print $2}')
        echo "Key ID: $keyid"
        read -p "Do you want to delete this key? (yes/no): " delete_key
        if [[ "$delete_key" == "yes" ]]; then
            echo "Deleting key: $keyid"
            gpg --batch --yes --delete-secret-key "$keyid"
            gpg --batch --yes --delete-key "$keyid"
            echo "Key deleted."
        else
            echo "Skipping key: $keyid"
        fi
    done
}

# Offer to delete existing keys
delete_existing_keys

# Prompt for key details
read -p "Enter your full name: " full_name
read -p "Enter your email: " email
read -p "Enter a comment for your key (optional): " comment

# Generate a new GPG key
echo "Generating a new GPG key with default size 4096 and no expiration..."
gpg --batch --gen-key <<EOF
    Key-Type: RSA
    Key-Length: 4096
    Subkey-Type: RSA
    Subkey-Length: 4096
    Name-Real: $full_name
    Name-Email: $email
    Name-Comment: $comment
    Expire-Date: 0
    %commit
EOF

echo "GPG key generation complete."

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
    echo "All Git GPG settings have been reset. GPG signing is no"
fi
