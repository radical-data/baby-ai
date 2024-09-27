# Base image for Ollama
FROM ollama/ollama

# Set working directory
WORKDIR /app

# Copy the start script into the container
COPY start-ollama.sh /app/start-ollama.sh

# Make the script executable
RUN chmod +x /app/start-ollama.sh

# Run the script in a shell environment
ENTRYPOINT ["/bin/sh", "/app/start-ollama.sh"]