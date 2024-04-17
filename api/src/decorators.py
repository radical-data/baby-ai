from functools import wraps
from pathlib import Path
import os
import json
from langchain_core.documents import Document

def document_to_dict(doc):
    """Convert a Document object or a list of Document objects to a dictionary format."""
    if isinstance(doc, list):
        return [document_to_dict(d) for d in doc]
    return {'page_content': doc.page_content, 'metadata': doc.metadata}

def dict_to_document(doc_dict):
    """Convert a dictionary or a list of dictionaries back to Document objects."""
    if isinstance(doc_dict, list):
        return [dict_to_document(d) for d in doc_dict]
    return Document(page_content=doc_dict['page_content'], metadata=doc_dict.get('metadata', {}))

def cached_info(name, **dec_kwargs):
    def decorator(wrapped):
        @wraps(wrapped)
        def wrapper(*args, **kwargs):
            cachedir = Path(os.environ.get('CACHEDIR', '.'), ".cache")
            if not cachedir.exists():
                cachedir.mkdir(parents=True, exist_ok=True)
            cache_file = cachedir / f"{name.replace(' ', '_')}.json"
            if 'version' in dec_kwargs:
                version = str(dec_kwargs['version']).lstrip('v')
                cache_file = cache_file.with_name(f"{cache_file.stem}-{version}{cache_file.suffix}")
            if not os.environ.get('REFRESH', 'false').lower() in ['true', '1'] and cache_file.exists():
                print(f"[reading cache: {cache_file}]")
                with open(cache_file, 'r') as file:
                    cached_data = json.load(file)
                return dict_to_document(cached_data)
            result = wrapped(*args, **kwargs)
            print(f"[caching to: {cache_file}]")
            with open(cache_file, 'w') as file:
                json.dump(document_to_dict(result), file, indent=2)
            return result
        return wrapper
    return decorator
