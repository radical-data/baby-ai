#!/bin/sh

# Start the Ollama server in the background
ollama serve &

# Wait a few seconds for the server to start (optional but ensures readiness)
sleep 5

# Pull the model after the server has started
ollama pull $OLLAMA_MODEL

wait