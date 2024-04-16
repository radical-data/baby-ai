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
from langchain.pydantic_v1 import BaseModel, Field
from langserve import add_routes
from typing import List, Dict
from tqdm import tqdm



# load document
print("loading docs")
loader = DirectoryLoader('data/', glob="**/*.html", show_progress=True, use_multithreading=True)
raw_docs = loader.load()

# split text
print("splitting text")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False)
docs = text_splitter.split_documents(raw_docs)

# # # embed text
print("embedding text")
underlying_embeddings = OllamaEmbeddings()
store = LocalFileStore("./cache/")
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)

# put text in database
# db = FAISS.from_documents(docs[0:10000], cached_embedder)

db = None
with tqdm(total=len(docs[0:10000]), desc="Ingesting documents") as pbar:
    for d in docs:
        if db:
            db.add_documents([d])
        else:
            db = FAISS.from_documents([d], cached_embedder)
        pbar.update(1)  

# print(db.embeddings)

# similarity search by vector
# print("searching by similarity")
# query = "the role of technology"
# embedding_vector = underlying_embeddings.embed_query(query)
# related_docs = db.similarity_search_by_vector(embedding_vector)
# for doc in related_docs:
#     print(f"From '{doc.metadata['source']}': {doc.page_content}\n")

# # build the question
print("building question")
llm = Ollama()
prompt = ChatPromptTemplate.from_template("""You are an expert researcher and storyteller, taking ideas from research and communicating them to others. Write an answer to the following question based only on the provided context.

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

# response = retrieval_chain.invoke({"input": "How can economics play a role in building a more equitable future?"})

# print(f"Question: {response['input']}\n")
# print("Related documents used in the context:")
# for doc in response['context']:
#     print(f"From '{doc.metadata['source']}': {doc.page_content}\n")
# print("Answer:")
# print(response['answer'])





# Define FastAPI application
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# Set all CORS enabled origins
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

# class Document(BaseModel):
#     page_content: str
#     metadata: Dict[str, str]

# class Output(BaseModel):
#     question: str = Field(..., alias="input")
#     context: List[Document]
#     answer: str

add_routes(app, chain.with_types(input_type=Input), path="/agent")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
