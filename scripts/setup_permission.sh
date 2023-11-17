#!/bin/bash

# Set the default permissions for new folders (directories)
chmod g+s,u+s .  # Sets the setgid and setuid bits on the current directory
find . -maxdepth 1 -type d -exec chmod 755 {} +  # Directories will have permissions rwxr-xr-x (755)

# Set the default permissions for new files
umask 002  # This sets default permissions for files (e.g., 775 for files)
find . -maxdepth 1 -type f -exec chmod 775 {} +  # Files will have permissions rw-rw-r-- (775)
