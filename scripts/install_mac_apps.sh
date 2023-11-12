#!/bin/bash

# ... [previous script content]


echo "Checking if mas (Mac App Store CLI) is installed..."
if brew list mas &>/dev/null; then
    echo "mas is already installed."
else
    echo "Installing mas..."
    brew install mas
    echo "mas installation complete."
fi

# Ensure you're signed in to the App Store for mas to work
# mas signin [your Apple ID email]

echo "Checking and installing/updating applications..."

# Define associative array of apps and their corresponding App Store IDs
declare -A apps
apps=(
    ["Slack for Desktop"]=803453959   # Slack's App ID
    ["DaVinci Resolve"]=571213070 # DaVinci Resolve
    # Add more apps here as needed
    # [AppName]=AppID
)


# Function to check and install/update an app
check_and_install_or_update() {
    for app_name in "${!apps[@]}"; do
        local app_id=${apps[$app_name]}

        if mas list | grep $app_id &> /dev/null; then
            echo "$app_name is already installed. Checking for updates..."
            mas upgrade $app_id
        else
            echo "Installing $app_name..."
            mas install $app_id
        fi
    done
}

# Check and install/update apps
check_and_install_or_update

echo "Application setup complete."

# ... [rest of the script]
