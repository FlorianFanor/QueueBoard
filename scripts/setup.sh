#!/bin/bash

# Navigate to the project root
cd "$(dirname "$0")/.."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies..."
source venv/bin/activate
pip install -r scripts/requirements.txt

echo "Setup complete! To run scripts, use:"
echo "source venv/bin/activate && python scripts/create_issues_from_yaml.py <yaml_file>"
