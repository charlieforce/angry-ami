#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "$SCRIPT_DIR/venv/bin/activate"

# Set Python path
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Load environment
export $(cat "$SCRIPT_DIR/.env" | grep -v '#' | xargs)

# Launch Ami - suppress initialization logs
cd "$SCRIPT_DIR"
python src/agent.py 2>/dev/null

# Deactivate on exit
trap "deactivate" EXIT
