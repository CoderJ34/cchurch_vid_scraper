#!/bin/bash

# Exit the script immediately if any command fails
set -e

echo "Starting build process..."

# Install Python dependencies from requirements.txt
if [ -f requirements.txt ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found!"
    exit 1
fi

# Install Playwright browser binaries
pip uninstall websockets
pip install websockets
