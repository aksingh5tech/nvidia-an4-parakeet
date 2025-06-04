#!/bin/bash

# -----------------------------
# Download and Extract AN4 Data
# -----------------------------
echo "📥 Downloading AN4 dataset..."
wget https://dldata-public.s3.us-east-2.amazonaws.com/an4_sphere.tar.gz

echo "📦 Extracting an4_sphere.tar.gz..."
tar -xvf an4_sphere.tar.gz

echo "📁 Moving 'an4' folder to current working directory..."
mv an4 "$(pwd)"

# -----------------------------
# Set DATA_DIR Environment Variable
# -----------------------------
echo "📌 Setting DATA_DIR environment variable..."
export DATA_DIR="$(pwd)"
echo "export DATA_DIR=$(pwd)" >> ~/.bashrc  # Makes it persistent for bash users

echo "✅ AN4 dataset setup complete."
