from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from llm import setup_langchain
from config import get_model_name


model_name = get_model_name()

chain = setup_langchain(model_name)

app = FastAPI(
    title="LangChain with Ollama",
    version="1.0",
    description="A LangChain service using Ollama",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

add_routes(app, chain, path="/agent")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
