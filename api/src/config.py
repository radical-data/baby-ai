import os


def get_model_name():
    model_name = os.getenv("OLLAMA_MODEL")
    if not model_name:
        raise EnvironmentError(
            "The OLLAMA_MODEL environment variable is not defined. Please set it to the desired model."
        )
    return model_name
