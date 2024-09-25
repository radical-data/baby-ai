#!/bin/sh

MODEL=${MODEL}
MODEL_PATH="/root/.ollama/models/$MODEL"

ollama serve &

ollama run $MODEL

wait