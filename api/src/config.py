import os
import warnings


def get_model_name():
    model_name = os.getenv("OLLAMA_MODEL")
    if not model_name:
        warnings.warn(
            "The OLLAMA_MODEL environment variable is not defined. Using the default model."
        )
        model_name = "qwen2.5:0.5b"
    return model_name


def get_openai_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError(
            "The OPENAI_API_KEY environment variable is not defined. Please set it."
        )
    return openai_api_key
