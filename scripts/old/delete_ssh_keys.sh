#!/bin/bash

# Function to list SSH keys with numbers
list_keys() {
    echo "Available SSH Keys:"
    keys=($(ls -al ~/.ssh | grep -E '\.pub$' | awk '{print $9}'))
    for i in "${!keys[@]}"; do
        echo "$((i+1))) ${keys[i]}"
    done
}

# Function to remove SSH key from SSH config and macOS Keychain
remove_key() {
    key_number=$1
    keys=($(ls -al ~/.ssh | grep -E '\.pub$' | awk '{print $9}'))
    key_to_delete=${keys[$((key_number-1))]}
    ssh-keygen -R $key_to_delete 2>/dev/null
    ssh-add -d ~/.ssh/${key_to_delete%.pub}
    # For macOS Keychain (if applicable)
    if [ "$(uname)" == "Darwin" ]; then
        security delete-generic-password -l "SSH: $key_to_delete"
    fi
    rm -f ~/.ssh/$key_to_delete ~/.ssh/${key_to_delete%.pub}
}

# Main script

# List available SSH keys
list_keys

# Ask user for key number to delete
read -p "Enter the number of the SSH key you want to delete: " key_number

# Confirm deletion
read -p "Are you sure you want to delete key $key_number? (y/n): " confirm_delete

if [ "$confirm_delete" == "y" ]; then
    remove_key $key_number
    echo "SSH key number $key_number has been deleted."
else
    echo "Deletion cancelled."
fi
