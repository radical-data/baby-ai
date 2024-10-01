#!/bin/sh

# Check if both models are present
if ollama list | grep -q "qwen" && ollama list | grep -q "nomic"; then
  exit 0
else
  exit 1
fi