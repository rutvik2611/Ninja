#!/bin/bash

echo "Starting MacBook setup..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Request user's password for sudo upfront
sudo -v
echo "Sudo access granted."

# Keep-alive: update existing `sudo` timestamp until this script has finished
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

echo "Configuring Sudo for Touch ID..."
echo "auth sufficient pam_tid.so" | sudo tee -a /etc/pam.d/sudo > /dev/null
echo "Sudo configured for Touch ID."

echo "Checking and Installing Homebrew..."
if ! command_exists brew; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$(/usr/local/bin/brew shellenv)"
    echo "Homebrew installation complete."
    # Source Homebrew changes in the current shell
    source "$HOME/.zshrc"  # Assuming you're using Zsh, replace with appropriate shell file if needed
else
    echo "Homebrew is already installed. Skipping installation."
fi

echo "Checking and Installing Oh My Zsh..."
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    echo "Installing Oh My Zsh..."
    sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    echo "Oh My Zsh installation complete."
else
    echo "Oh My Zsh is already installed. Skipping installation."
fi

echo "Checking and Installing Powerlevel10k..."
if ! command_exists p10k; then
    echo "Installing Powerlevel10k..."
    brew install powerlevel10k
    echo "source $(brew --prefix)/share/powerlevel10k/powerlevel10k.zsh-theme" >>~/.zshrc
    echo "Powerlevel10k installation complete."
else
    echo "Powerlevel10k is already installed. Skipping installation."
fi

echo "Checking and Installing Zsh plugins..."
if [ ! -d "${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions" ]; then
    git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
    echo "Zsh autosuggestions plugin installed."
else
    echo "Zsh autosuggestions plugin is already installed. Skipping installation."
fi

if [ ! -d "${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting" ]; then
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
    echo "Zsh syntax highlighting plugin installed."
else
    echo "Zsh syntax highlighting plugin is already installed. Skipping installation."
fi

# Adding fzf
if ! command_exists fzf; then
    echo "Installing fzf..."
    brew install fzf
    $(brew --prefix)/opt/fzf/install
    echo "fzf installation complete."
else
    echo "fzf is already installed. Skipping installation."
fi

# Adding bat
if ! command_exists bat; then
    echo "Installing bat..."
    brew install bat
    echo "bat installation complete."
else
    echo "bat is already installed. Skipping installation."
fi

# Update plugins list
if ! grep -qF "plugins=(git zsh-autosuggestions cp sudo web-search copypath copyfile copybuffer dirhistory history jsontools macos auto-notify you-should-use fzf bat)" ~/.zshrc; then
    echo "Updating Zsh plugins list..."
    echo "plugins=(git zsh-autosuggestions cp sudo web-search copypath copyfile copybuffer dirhistory history jsontools macos auto-notify you-should-use fzf bat)" >>~/.zshrc
    echo "AUTO_NOTIFY_IGNORE+=(\"docker\")" >>~/.zshrc
    echo "Zsh plugins list updated."
else
    echo "Zsh plugins list is already updated. Skipping update."
fi

echo "Checking and Installing Visual Studio Code..."
if ! command_exists code; then
    echo "Installing Visual Studio Code..."
    brew install --cask visual-studio-code
    echo "alias code=\"/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code\"" >>~/.zshrc
    echo "Visual Studio Code installation and alias setup complete."
else
    echo "Visual Studio Code is already installed. Skipping installation."
fi

echo "Checking and Installing Discord..."
if ! command_exists discord; then
    echo "Installing Discord..."
    brew install --cask discord
    echo "Discord installation complete."
else
    echo "Discord is already installed. Skipping installation."
fi

echo "Checking and Installing Docker Desktop..."
if ! command_exists docker; then
    echo "Installing Docker Desktop..."
    brew install --cask docker
    echo "Docker Desktop installation complete."
else
    echo "Docker Desktop is already installed. Skipping installation."
fi

echo "MacBook setup completed successfully! Please restart your terminal."
