import os
import re
from pathlib import Path
from typing import List
from agent.infrastructure.knowledge.semanticSearch.ChromaCollection import ChromaCollection
from dotenv import load_dotenv
load_dotenv(".env")

def mdx_to_md(text: str) -> str:
    # Remove imports e exports
    text = re.sub(r"^import .*?$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^export .*?$", "", text, flags=re.MULTILINE)
    # Remove JSX simples (<Component /> ou <Component>...</Component>)
    text = re.sub(r"<[^>]+/>", "", text)
    text = re.sub(r"<[^>]+>.*?</[^>]+>", "", text, flags=re.DOTALL)
    # Limpa múltiplas linhas vazias
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start = end - overlap
    return chunks

def ingest_mdx_folder(folder_path: str, chroma: ChromaCollection):
    folder = Path(folder_path)
    for file_path in folder.rglob("*.mdx"):
        with open(file_path, "r", encoding="utf-8") as f:
            raw_text = f.read()
        md_text = mdx_to_md(raw_text)
        chunks = chunk_text(md_text)
        documents = []
        metadatas = []
        ids = []
        for i, chunk in enumerate(chunks):
            documents.append(chunk)
            metadatas.append({
                "source": str(file_path),
                "file_name": file_path.name,
                "chunk_index": i,
                "total_chunks": len(chunks),
                "doc_type": "documentation",
                "format": "md"
            })
            ids.append(f"{file_path.stem}_{i}")

        if documents:
            chroma.collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )

chroma = ChromaCollection("./agent/infrastructure/knowledge/vectorStore","langgraph_docs")

# a base de conhecimento usada para o teste foi a documentação do langgraph, disponível em https://github.com/langchain-ai/docs/tree/main/src/oss/langgraph
ingest_mdx_folder(os.getenv("KNOWLEDGE_BASE_ORIGINAL_PATH"),chroma)

