#!/bin/sh

# Start the Ollama server in the background
ollama serve &

sleep 5

# Pull the model
ollama pull $OLLAMA_MODEL

# Pull embedding model
# ollama pull "nomic-embed-text:v1.5"

wait