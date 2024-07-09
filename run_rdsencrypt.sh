#!/bin/bash

# Function to check if a Python package is installed
function is_installed {
    $PYTHON_CMD -c "import $1" &> /dev/null
    return $?
}

# Function to find the python command
function find_python {
    if command -v python &> /dev/null; then
        PYTHON_CMD=python
    elif command -v python3 &> /dev/null; then
        PYTHON_CMD=python3
    else
        echo "Python is not installed. Please install Python and try again."
        exit 1
    fi
}

# Find the python command
find_python

# Clone the repository
git clone https://github.com/mriccobene-git/RDS-Encryption-Hardening.git

# Change to the repository directory
cd RDS-Encryption-Hardening

# Check if boto3 is installed, and install it if not
if is_installed boto3; then
    echo "boto3 is already installed."
else
    echo "boto3 is not installed. Installing boto3..."
    $PYTHON_CMD -m pip install boto3
fi

# Run the Python script
$PYTHON_CMD rdsencrypt.py
