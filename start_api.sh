#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$SCRIPT_DIR/venv/bin/activate"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"
export $(cat "$SCRIPT_DIR/.env" | grep -v '#' | xargs)

cd "$SCRIPT_DIR"

echo "🔥 STARTING ANGRY AMI API SERVER 🔥"
echo ""
python src/api_server.py
