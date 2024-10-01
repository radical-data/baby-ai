#!/bin/sh

# Check if model is present
if ollama list | grep -q "qwen"; then
  exit 0
else
  exit 1
fi