import os
from fastapi import FastAPI
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langserve import add_routes

# Define the Ollama LLM
model_name = os.getenv("OLLAMA_MODEL")
if not model_name:
    raise EnvironmentError("The OLLAMA_MODEL environment variable is not defined. Please set it to the desired model.")
llm = OllamaLLM(model=model_name)

# Create prompt template
# system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages([
    # ('system', system_template),
    ('user', '{text}')
])

# Create parser
parser = StrOutputParser()

# Create chain
chain = prompt_template | llm | parser

# Define FastAPI app
app = FastAPI(
    title="LangChain with Ollama",
    version="1.0",
    description="A LangChain service using Ollama"
)

# Add chain route
add_routes(app, chain, path="/agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)