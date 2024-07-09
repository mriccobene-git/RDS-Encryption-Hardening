#!/bin/bash

# Function to check if a Python package is installed
function is_installed {
    python -c "import $1" &> /dev/null
    return $?
}

# Clone the repository
git clone https://github.com/mriccobene-git/RDS-Encryption-Hardening.git

# Change to the repository directory
cd RDS-Encryption-Hardening

# Check if boto3 is installed, and install it if not
if is_installed boto3; then
    echo "boto3 is already installed."
else
    echo "boto3 is not installed. Installing boto3..."
    pip install boto3
fi

# Run the Python script
python rdsencrypt.py
