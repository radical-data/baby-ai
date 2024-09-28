from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langserve import add_routes
from llm import setup_langchain
from config import get_model_name
from db import add_message, get_all_messages, create_tables
from pydantic import BaseModel


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

@app.on_event("startup")
async def startup_event():
    await create_tables()

class MessageRequest(BaseModel):
    message_text: str

@app.post("/log_message/")
async def log_message(message: MessageRequest):
    await add_message(message.message_text)
    return {"message": "Message logged successfully."}


@app.get("/all_messages/")
async def all_messages():
    all_messages = await get_all_messages()
    return {"messages": all_messages}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
