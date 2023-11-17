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

# Generate a GPG key if not existing
gpg_key_exists=$(gpg --list-secret-keys | grep -c '^')
if [ "$gpg_key_exists" -eq 0 ]; then
    echo "Generating a GPG key for signing..."
    gpg --full-generate-key
    echo "GPG key generated."
fi

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
    fi
fi

# Generate a new SSH key using GPG for signing
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

        # Generate SSH key with GPG for signing
        read -p "Enter a name for your SSH key (e.g., 'github_rsa'): " key_name
        gpg_key_id=$(gpg --list-secret-keys --keyid-format LONG | grep sec | awk '{print $2}' | awk -F '/' '{print $2}')
        ssh-keygen -t rsa -b 4096 -C "$email" -f "$SSH_DIR/$key_name" -I "$gpg_key_id"
        echo "SSH key generated and signed with GPG."
        key_path="$SSH_DIR/${key_name}.pub"
        private_key_path="$SSH_DIR/$key_name"
        ssh-add --apple-use-keychain "$private_key_path"
        echo "SSH key added to the SSH agent and macOS Keychain."

    else
        echo "No SSH key selected or generated. Exiting script."
        exit 1
    fi
fi

# Set up Git to use GPG key for signing commits
echo "Configuring Git to use GPG key for signing commits...."
gpg_key_id=$(gpg --list-secret-keys --keyid-format LONG | grep sec | awk '{print $2}' | awk -F '/' '{print $2}')
git config --global user.signingkey "$gpg_key_id"
git config --global commit.gpgsign true
echo "Git configured to use GPG key for signing commits."

# Copy the SSH key to clipboard
if [ -f "$key_path" ]; then
    echo "Copying the SSH public key to the clipboard..."
    cat "$key_path" | pbcopy
    echo "SSH public key has been copied to the clipboard."

    # Instructions to add SSH key to GitHub
    echo "Please manually add the SSH key to your GitHub account:"
    echo "1. Go to https://github.com/settings/keys"
    echo "2. Click on 'New SSH key' or 'Add SSH key'"
    echo "3. In the 'Title' field, add a descriptive label for the new key"
    echo "4. Paste your key into the 'Key' field"
    echo "5. Click 'Add SSH key'"
    echo "If prompted, confirm your GitHub password"
else
    echo "No SSH key available to copy to clipboard."
fi

# Prompt user to configure Git with GPG key
echo "Please ensure your Git email matches the GPG key's email:"
git_email=$(git config --get user.email)
if [ "$git_email" != "$email" ]; then
    read -p "Your Git email ($git_email) does not match the GPG key's email ($email). Do you want to update your Git email to match? (yes/no): " update_email
    if [ "$update_email" == "yes" ]; then
        git config --global user.email "$email"
        echo "Git email updated to match the GPG key's email."
    else
        echo "Please manually update your Git email to match the GPG key's email ($email)."
    fi
fi
