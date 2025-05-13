#!/bin/bash

# This is a sample script that might be used to run parts of the project.

echo "Starting analysis script..."

# Navigate to the project root (assuming the script is in a subdirectory)
# SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
# cd "$SCRIPT_DIR/.."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
  echo "Activating virtual environment..."
  source venv/bin/activate
elif [ -d ".venv" ]; then
  echo "Activating virtual environment..."
  source .venv/bin/activate
fi

# Run the main Python application
echo "Running main application (src/main.py)..."
python src/main.py

# Example: Run tests using pytest
# echo "Running tests..."
# pytest

# Example: Linting with a hypothetical linter
# echo "Linting code..."
# pylint src/

echo "Analysis script finished." 