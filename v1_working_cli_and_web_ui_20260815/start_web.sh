#!/bin/bash

# Start Ami API server in background
echo "🔥 Starting Angry Ami API Server..."
python src/api_server.py &
API_PID=$!

# Wait for API to start
sleep 2

# Open web browser
echo "Opening web browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
  open http://localhost:5000
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
  xdg-open http://localhost:5000
fi

# Keep running
wait $API_PID
