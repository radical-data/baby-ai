from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langserve import add_routes
from tqdm import tqdm
from decorators import cached_info

llm = Ollama(model="qwen2.5:0.5b", base_url="http://0.0.0.0:11434", verbose=True)

@cached_info("load_documents", version="1.0")
def load_documents(directory):
    loader = DirectoryLoader(
        directory,
        show_progress=True,
        use_multithreading=True,
    )
    raw_docs = loader.load()
    return raw_docs


def split_documents(raw_docs):
    print("Splitting documents")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=20, length_function=len, is_separator_regex=False
    )
    return text_splitter.split_documents(raw_docs)


print("loading docs")
raw_docs = load_documents("data/texts")

print("splitting text")
docs = split_documents(raw_docs)

print("embedding text")
underlying_embeddings = OllamaEmbeddings()
store = LocalFileStore("./cache/")
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)

print("putting texts in database")
db = None
with tqdm(total=len(docs), desc="Ingesting documents") as pbar:
    for d in docs:
        if db:
            db.add_documents([d])
        else:
            db = FAISS.from_documents([d], cached_embedder)
        pbar.update(1)

print("building question")
prompt = ChatPromptTemplate.from_template("""You are an African auntie and griot full of knowledge and wisdom, who can help us move beyond capitalist logics.
Write an answer to the following question based only on the provided context. The context is your and your people's memory and oral knowledge.

- You speak through parables.
- Your answer must be exactly three sentences long.
- It should directly address the question. In particular, the first sentence should relate to the question.
- Embed the ideas, phrases and words from the context into your answer seamlessly.
- Do not explicitly mention the provided context or that it was provided to you. Specifically, avoid phrases like "according to the provided context".
- Do not mention the process of questioning or structuring answers. Specifically, refrain from phrases like "In response to the question".

Context provided:

<context>
{context}
</context>

Question: {input}""")

document_chain = create_stuff_documents_chain(llm, prompt)

retriever = db.as_retriever(search_type="mmr")
retrieval_chain = create_retrieval_chain(retriever, document_chain)

output_parser = StrOutputParser()

chain = retrieval_chain

print("defining API")
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


class Input(BaseModel):
    input: str


add_routes(app, chain.with_types(input_type=Input), path="/agent")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
