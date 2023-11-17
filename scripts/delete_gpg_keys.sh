#!/bin/bash

count=1
keys=()

while IFS= read -r line; do
    if [[ "$line" =~ ^sec: ]]; then
        key_id=$(echo "$line" | awk -F: '{print $5}')
        user=$(echo "$line" | awk -F: '/^uid/ {print substr($0, index($0, $10))}')
        comment=$(echo "$line" | awk -F: '/^uid/ {print substr($0, index($0, $12))}')
        email=$(echo "$line" | awk -F: '/^uid/ {print substr($0, index($0, $14))}')

        echo "Key Number: $count"
        echo "Key ID: $key_id"
        echo "User Name: $user"
        echo "Comment: $comment"
        echo "Email: $email"
        echo "--------------------------------------------------"

        keys+=("$key_id")
        ((count++))
    fi
done < <(gpg --list-secret-keys --with-colons)

echo

while true; do
    read -p "Enter the number of the key to delete (or 'exit' to quit): " user_choice

    if [[ "$user_choice" == "exit" ]]; then
        break
    fi

    if [[ "$user_choice" =~ ^[0-9]+$ && "$user_choice" -ge 1 && "$user_choice" -le ${#keys[@]} ]]; then
        key_id_to_delete=${keys[$((user_choice - 1))]}
        echo
        echo "Deleting selected key..."
        fingerprint=$(gpg --list-secret-keys --with-colons "$key_id_to_delete" | awk -F: '$1 == "fpr" {print $10; exit}')
        if [[ -n "$fingerprint" ]]; then
            delete_output=$(gpg --batch --yes --delete-secret-keys "$fingerprint" 2>&1)
            if [[ $? -ne 0 ]]; then
                echo "Error deleting secret key: $delete_output"
            else
                delete_output=$(gpg --batch --yes --delete-keys "$fingerprint" 2>&1)
                if [[ $? -ne 0 ]]; then
                    echo "Error deleting public key: $delete_output"
                else
                    echo "Key deleted successfully."
                fi
            fi
        else
            echo "Error: Could not find the key's fingerprint."
        fi

        echo
        echo "Restarting GPG agent..."
        gpgconf --kill all
        echo
    else
        echo "Invalid key number. Please try again."
    fi
done
