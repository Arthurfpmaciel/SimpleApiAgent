from typing import List
from fastembed import TextEmbedding
from langchain_core.embeddings import Embeddings
import numpy as np
import chromadb
from pathlib import Path

# classe para gerar embeddings de descrições a partir de modelo do FastEmbed
class FastEmbedEmbeddings(Embeddings):
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2', cache_dir: str = "/models"):
        super().__init__()
        # no meu caso, para rodar local preciso remover o comentário abaixo e colocar cache_dir= None
        # if cache_dir is None:
        #     cache_dir = Path.home() / "models"
        self.model = TextEmbedding(model_name=model_name, cache_dir=str(cache_dir))

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        embeddings: List[np.ndarray] = list(self.model.embed(texts))
        return [embedding.tolist() for embedding in embeddings]

    def embed_query(self, text: str) -> List[float]:
        embedding: np.ndarray = list(self.model.embed([text]))[0]
        return embedding.tolist()
    
fastembed_model = FastEmbedEmbeddings()

# interface da classe de embeddings para o chroma db
class EmbeddingFunction(chromadb.EmbeddingFunction):
    def __init__(self):
        super().__init__()

    def __call__(self, input: chromadb.Documents) -> chromadb.Embeddings:
        embeddings = fastembed_model.embed_documents(input)
        return embeddings