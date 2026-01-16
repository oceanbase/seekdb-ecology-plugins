#!/usr/bin/env python3
"""
Custom embedding functions for seekdb.

These classes can be used as embedding_function when creating collections.
"""

class CustomEmbeddingFunction:
    """
    Custom embedding function using sentence-transformers.
    
    Usage:
        from embedding_functions import CustomEmbeddingFunction
        ef = CustomEmbeddingFunction(model_name="BAAI/bge-m3")
        collection = client.get_or_create_collection(
            name="my_collection",
            embedding_function=ef
        )
    """
    def __init__(self, model_name="BAAI/bge-m3"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        self._dimension = self.model.get_sentence_embedding_dimension()
    
    def __call__(self, texts):
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    @property
    def dimension(self):
        return self._dimension


class OllamaEmbeddingFunction:
    """
    Embedding function using Ollama local models.
    
    Prerequisites:
        - Ollama installed and running
        - Model pulled: ollama pull bge-m3
    
    Usage:
        from embedding_functions import OllamaEmbeddingFunction
        ef = OllamaEmbeddingFunction(model="bge-m3")
        collection = client.get_or_create_collection(
            name="my_collection",
            embedding_function=ef
        )
    """
    def __init__(self, model="bge-m3"):
        self.model = model
        # bge-m3 dimension is 1024
        self._dimension = 1024
    
    def __call__(self, texts):
        import ollama
        result = ollama.embed(model=self.model, input=texts)
        return result['embeddings']
    
    @property
    def dimension(self):
        return self._dimension


class RemoteEmbeddingFunction:
    """
    Embedding function using OpenAI-compatible API.
    
    Supports: OpenAI, Tongyi Qianwen, and other compatible services.
    
    Usage:
        from embedding_functions import RemoteEmbeddingFunction
        ef = RemoteEmbeddingFunction(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings",
            api_key="your-api-key",
            model="text-embedding-v3",
            dimensions=1024
        )
        collection = client.get_or_create_collection(
            name="my_collection",
            embedding_function=ef
        )
    """
    def __init__(self, base_url, api_key, model, dimensions=1024):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model
        self._dimension = dimensions
    
    def __call__(self, texts):
        import requests
        res = requests.post(
            self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "input": texts,
                "model": self.model,
                "encoding_format": "float",
                "dimensions": self._dimension,
            },
        )
        data = res.json()
        return [d["embedding"] for d in data["data"]]
    
    @property
    def dimension(self):
        return self._dimension
