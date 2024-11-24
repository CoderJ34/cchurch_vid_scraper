#!/bin/bash

# Exit on error
# Step 1: Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y wget gnupg curl

# Add Google Chrome repository and install it
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
apt-get update
apt-get install -y google-chrome-stable

# Install Chromium browser (alternative)
apt-get install -y chromium

# Step 2: Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Step 3: Install Playwright and necessary browsers
echo "Installing Playwright and required browsers..."
python -m playwright install

echo "System and Python dependencies installed successfully."
