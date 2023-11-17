#!/bin/bash

# Function to validate email
validate_email() {
    if [[ $1 =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$ ]]; then
        return 0
    else
        return 1
    fi
}

# Path to the SSH directory
SSH_DIR="$HOME/.ssh"

# Check for existing SSH keys
echo "Checking for existing SSH keys..."
existing_keys=()
if [ -d "$SSH_DIR" ]; then
    for keyfile in "$SSH_DIR"/*.pub; do
        if [ -f "$keyfile" ]; then
            existing_keys+=("$keyfile")
        fi
    done

    if [ ${#existing_keys[@]} -gt 0 ]; then
        echo "Existing SSH keys found:"
        for i in "${!existing_keys[@]}"; do
            echo "[$i] ${existing_keys[$i]}"
        done

        read -p "Do you want to use one of these keys? (yes/no): " use_existing_key
        if [ "$use_existing_key" == "yes" ]; then
            read -p "Enter the number of the key you want to use: " key_number
            if [ -n "${existing_keys[$key_number]}" ]; then
                echo "You chose to use ${existing_keys[$key_number]}"
                key_path="${existing_keys[$key_number]}"
                private_key_path="${key_path%.*}"
                ssh-add --apple-use-keychain "$private_key_path"
                echo "SSH key added to the SSH agent and macOS Keychain."
            else
                echo "Invalid selection. Exiting script."
                exit 1
            fi
        fi
    fi
fi

# Generate a new SSH key if not using an existing one
if [ -z "$key_path" ]; then
    read -p "Do you want to generate a new SSH key? (yes/no): " generate_key
    if [ "$generate_key" == "yes" ]; then
        while true; do
            read -p "Enter the email address associated with your GitHub account: " email
            if validate_email "$email"; then
                break
            else
                echo "Invalid email format. Please try again."
            fi
        done
        read -p "Enter a name for your SSH key (e.g., 'github_rsa'): " key_name
        ssh-keygen -t rsa -b 4096 -C "$email" -f "$SSH_DIR/$key_name"
        echo "SSH key generated."
        key_path="$SSH_DIR/${key_name}.pub"
        private_key_path="$SSH_DIR/$key_name"
        ssh-add --apple-use-keychain "$private_key_path"
        echo "SSH key added to the SSH agent and macOS Keychain."
    else
        echo "No SSH key selected or generated. Exiting script."
        exit 1
    fi
fi

# Copy the SSH key to clipboard
if [ -f "$key_path" ]; then
    echo "Copying the SSH public key to the clipboard..."
    pbcopy < "$key_path"
    echo "SSH public key has been copied to the clipboard."
else
    echo "No SSH key available to copy to clipboard."
fi

# Instructions for adding SSH key to GitHub
echo "Please manually add the SSH key to your GitHub account:"
echo "1. Go to https://github.com/settings/keys"
echo "2. Click on 'New SSH key' or 'Add SSH key'"
echo "3. In the 'Title' field, add a descriptive label for the new key"
echo "4. Paste your key into the 'Key' field"
echo "5. Click 'Add SSH key'"
echo "If prompted, confirm your GitHub password"

# Confirmation and Validation step
read -p "Have you added the SSH key to your GitHub account? (yes/no): " added_key
if [ "$added_key" == "yes" ]; then
    echo "Attempting to verify the SSH key with GitHub..."
    ssh_output=$(ssh -T git@github.com 2>&1)
    if [[ $ssh_output == *"successfully authenticated"* ]]; then
        echo "SSH key successfully authenticated with GitHub."
        echo "Your SSH key should now be set up with GitHub."
    else
        echo "Failed to authenticate with GitHub using the SSH key."
        echo "Please check if the SSH key has been correctly added to your GitHub account."
    fi
else
    echo "Please add the SSH key to GitHub to complete the setup."
fi

# Ask user if they want to set default behavior for GitHub URLs to use SSH
read -p "Do you want to set default behavior for Git to use SSH for GitHub URLs? (yes/no): " configure_ssh
if [[ "$configure_ssh" == "yes" ]]; then
    git config --global url."git@github.com:".insteadOf "https://github.com/"
    echo "Git configured to use SSH for GitHub URLs."
else
    echo "Skipping default behavior configuration for GitHub URLs."
fi
