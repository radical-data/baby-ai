from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def setup_langchain(model_name: str):
    llm = OllamaLLM(model=model_name)

    prompt_template = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are Baby AI. You can only talk by saying 'goo goo gaa gaa'.",
            ),
            ("user", "{text}"),
        ]
    )

    parser = StrOutputParser()

    chain = prompt_template | llm | parser

    return chain
