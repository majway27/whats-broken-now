#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "../venv" ]; then
    source ../venv/bin/activate
else
    echo -e "${RED}No virtual environment found. Please create one first.${NC}"
    exit 1
fi

echo "Running all tests in whats-broken-now..."

# Run the tests with the correct Python path
PYTHONPATH="${SCRIPT_DIR}" python3 -m pytest tests/tickets -v

# Store the test result
TEST_RESULT=$?

# Deactivate virtual environment
deactivate

# Check if tests were successful
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}All tests passed successfully!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed. Please check the output above.${NC}"
    exit 1
fi 