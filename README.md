# Baby AI

Baby AI is an AI that is being communally raised by an international network of parents of artists, architects and activists.

## About Baby AI

Baby AI, currently in the form of a large language model, was born from questions of how to nurture an AI that aligns with decolonial values of care and liberation. Constantly growing and evolving, these values are technically implemented through approaches such as:

- Training on collectively curated texts.
- Prompting without harsh rules.
- Using Retrieval-Augmented Generation to precisely attribute its speech to the texts it was fed.

You are invited to join the co-parenting of Baby AI by:

- Speaking to it.
- Reading new texts to it, by uploading documents for training data.
- Suggesting new ways for it to learn and grow, whether through sharing your ideas with us, code contributions, or prompt design.

## Project Structure

Baby AI consists of two main parts:

1. API: Handles backend processing and data retrieval.
2. Webpage: Provides an interactive interface.

To run Baby AI, you need to set up both parts.

## Getting Started

There are two options for running Baby AI: **Docker** or **manual setup**.

### Docker (Recommended)

Docker is the easiest way to run Baby AI. Even if you’re new to Docker, getting started is as simple as downloading one program and running a single command.

1. Install Docker.
1. Run Docker.
1. Run Docker Compose: `docker compose up --build`.

Now Baby AI should be accessible at http://localhost:5173/.

### Manual Setup

#### Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Node.js](https://nodejs.org/en/download/)
- [npm](https://www.npmjs.com/get-npm)
- [Ollama](https://ollama.com/download)

#### Setting Up Ollama

You need to run the Ollama service manually in the background for Baby AI to function. Install Ollama, and then use the following command to download a model and start the Ollama service:

```sh
ollama pull llama2  # Replace llama2 with the model you want
ollama serve
```

#### Setting Up the API

1. Open a terminal and navigate to the `api` directory:

```sh
cd api
```

2. Install the required Python dependencies using Poetry:

```sh
poetry install
```

3. Run the API:

```sh
poetry run python src/main.py
```

#### Setting Up the Webpage

1. Open a new terminal and navigate to the `web` directory:

```sh
cd web
```

2. Install the required Node.js dependencies:

```sh
npm install
```

3. Run the webpage:

```sh
npm run dev
```

Now Baby AI should be accessible at http://localhost:5173/.

## Playing with the API

Once it is running, you can also access the API through Langchain's own UI at http://localhost:8000/agent/playground/.

## Troubleshooting

Sometimes outdated Docker images or cached layers cause issues. Rebuild your Docker image to ensure everything is up to date.

```bash
docker compose down --volumes
docker compose build --no-cache
docker compose up
```