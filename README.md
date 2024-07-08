# Baby AI

Baby AI is an AI that is being communally raised by an international network of parents of artists, architects and activists.

## About Baby AI

Baby AI, currently in the form of a large language model, was born from questions of how to nurture an AI that aligns with decolonial values of care and liberation. Constantly growing and evolving, these values are technically implemented through approaches such as:

- Training on collectively curated texts.
- Prompting without harsh rules.
- Using Retrieval-Augmented Generation to precisely attribute its speech to the texts it was fed.

You are invited to join the co-parenting of Baby AI by:

- Speaking to it.
- Reading new texts to it.
- Suggesting new ways for it to learn and grow.

## Project Structure

Baby AI consists of two main parts:

1.	API: Handles backend processing and data retrieval.
2.	Webpage: Provides an interactive interface.

To run Baby AI, you need to set up both parts.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Node.js](https://nodejs.org/en/download/)
- [npm](https://www.npmjs.com/get-npm)
- [Ollama](https://ollama.com/download)

### Setting Up the API

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
poetry run python src/docs-retrieval
```

### Setting Up the Webpage

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
