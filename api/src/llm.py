from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from langchain_core.vectorstores import InMemoryVectorStore

# from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough
from config import get_openai_api_key


def setup_langchain(model_name: str):
    print("load docs")
    loader = DirectoryLoader("./data/texts", show_progress=True)
    docs = loader.load()

    print("splitting")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    print("create embeddings")
    openai_api_key = get_openai_api_key()
    embedding_function = OpenAIEmbeddings(api_key=openai_api_key)

    vector_store = InMemoryVectorStore.from_texts(
        texts=[doc.page_content for doc in split_docs], embedding=embedding_function
    )

    print("create retriever")
    retriever = vector_store.as_retriever(
        search_type="similarity", search_kwargs={"k": 6}
    )

    print("define prompt")
    system_prompt = (
        "You are Baby AI. You are talking to users to learn about the world."
        "Use the following pieces of retrieved context to generate your response."
        "\n\n"
        "{context}"
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [("system", system_prompt), ("user", "{input}")]
    )

    # Create Ollama LLM instance
    llm = OllamaLLM(model=model_name)

    # Function to format the retrieved documents
    def format_docs(docs):
        return "\n\n".join([doc.page_content for doc in docs])

    # Setup RAG chain with retriever and LLM
    rag_chain = (
        {"context": retriever | format_docs, "input": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )

    return rag_chain
