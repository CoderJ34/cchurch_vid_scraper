#!/bin/bash

# Exit on error
set -e

# Step 1: Install Python dependencies from requirements.txt
apt-get update
apt-get install -y \
  wget \
  gnupg \
  curl \
  libnss3 \
  libatk-bridge2.0-0 \
  libatk1.0-0 \
  libcups2 \
  libxss1 \
  libgdk-pixbuf2.0-0 \
  libnspr4 \
  libxcomposite1 \
  libxrandr2 \
  libgbm1 \
  libasound2 \
  libpangocairo-1.0-0 \
  libpango-1.0-0 \
  libx11-xcb1 \
  libgl1-mesa-glx \
  libegl1-mesa \
  libxrandr2 \
  libgbm1 \
  libgdk-pixbuf2.0-0 \
  libsecret-1-0 \
  libvulkan1 \
  libavif-dev \
  libgles2-mesa
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Step 2: Install Playwright browser binaries
echo "Installing Playwright browsers..."
python -m playwright install

echo "Dependencies and Playwright browsers installed successfully."
