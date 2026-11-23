"""
Chunk scraped documents and embed them into ChromaDB.

Usage:
    python ingest.py             # scrapes, chunks, and stores in ChromaDB
"""

from langchain_community.vectorstores import Chroma
from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_COLLECTION, CHROMA_DIR, EMBED_MODEL
from scrape import scrape


def build_vectorstore() -> Chroma:
    print("Scraping pages...")
    docs = scrape()
    print(f"  Scraped {len(docs)} pages")

    print("Loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)

    print("Chunking documents...")
    splitter = SemanticChunker(embeddings)
    chunks = splitter.split_documents(docs)
    print(f"  Total chunks: {len(chunks)}")

    print("Storing in ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
        collection_name=CHROMA_COLLECTION,
    )
    print(f"Stored {len(chunks)} chunks in {CHROMA_DIR}")
    return vectorstore


def load_vectorstore() -> tuple[Chroma, list]:
    """Load existing ChromaDB and return (vectorstore, chunks) for BM25."""
    embeddings = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vectorstore = Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings,
        collection_name=CHROMA_COLLECTION,
    )
    # Retrieve all stored docs for BM25
    raw = vectorstore.get(include=["documents", "metadatas"])
    from langchain_core.documents import Document
    chunks = [
        Document(page_content=text, metadata=meta)
        for text, meta in zip(raw["documents"], raw["metadatas"])
    ]
    return vectorstore, chunks


if __name__ == "__main__":
    build_vectorstore()
