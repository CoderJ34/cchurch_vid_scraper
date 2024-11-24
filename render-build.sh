#!/bin/bash

# Exit on error
set -e

# Step 1: Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Step 2: Install Playwright browser binaries
echo "Installing Playwright browsers..."
python -m playwright install

echo "Dependencies and Playwright browsers installed successfully."
