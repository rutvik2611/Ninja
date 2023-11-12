#!/bin/bash

echo "Starting MacBook setup..."

# Request user's password for sudo upfront
sudo -v
echo "Sudo access granted."

# Keep-alive: update existing `sudo` timestamp until this script has finished
while true; do sudo -n true; sleep 60; kill -0 "$$" || exit; done 2>/dev/null &

echo "Configuring Sudo for Touch ID..."
echo "auth sufficient pam_tid.so" | sudo tee -a /etc/pam.d/sudo > /dev/null
echo "Sudo configured for Touch ID."

echo "Installing Homebrew..."
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
eval "$(/usr/local/bin/brew shellenv)"
echo "Homebrew installation complete."

echo "Installing Oh My Zsh..."
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
echo "Oh My Zsh installation complete."

echo "Installing Powerlevel10k..."
brew install powerlevel10k
echo "source $(brew --prefix)/share/powerlevel10k/powerlevel10k.zsh-theme" >>~/.zshrc
echo "Powerlevel10k installation complete."

echo "Installing Zsh plugins..."
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git
echo "source ${(q-)PWD}/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh" >> ${ZDOTDIR:-$HOME}/.zshrc
echo "plugins=(git zsh-autosuggestions cp sudo web-search copypath copyfile copybuffer dirhistory history jsontools macos auto-notify you-should-use)" >>~/.zshrc
echo "AUTO_NOTIFY_IGNORE+=(\"docker\")" >>~/.zshrc
echo "Zsh plugins installation complete."

echo "Installing Visual Studio Code..."
brew install --cask visual-studio-code
echo "alias code=\"/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code\"" >>~/.zshrc
echo "Visual Studio Code installation and alias setup complete."

echo "Installing Discord..."
brew install --cask discord
echo "Discord installation complete."

echo "Installing Docker Desktop..."
brew install --cask docker
echo "Docker Desktop installation complete."

echo "MacBook setup completed successfully! Please restart your terminal."
