# Base image for Ollama
FROM ollama/ollama

# Set working directory
WORKDIR /app

# Copy the start script into the container
COPY start-ollama.sh /app/start-ollama.sh
COPY healthcheck.sh /app/healthcheck.sh

# Make the script executable
RUN chmod +x /app/start-ollama.sh
RUN chmod +x healthcheck.sh

HEALTHCHECK --interval=1m --timeout=10s --start-period=10s --retries=3 CMD /app/healthcheck.sh

# Run the script in a shell environment
ENTRYPOINT ["/bin/sh", "/app/start-ollama.sh"]