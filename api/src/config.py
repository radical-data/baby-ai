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
