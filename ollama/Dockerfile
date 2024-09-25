FROM ollama/ollama

RUN apt-get update && apt-get install -y curl

COPY download_model.sh /usr/local/bin/download_model.sh

RUN chmod +x /usr/local/bin/download_model.sh