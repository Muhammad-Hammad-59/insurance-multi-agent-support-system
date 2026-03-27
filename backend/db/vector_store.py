# """
# backend/db/vector_store.py
# Manages the ChromaDB vector store for FAQ retrieval (RAG).
# """

# import os
# import chromadb
# from typing import List, Dict
# from backend.config import Config
# CHROMA_DB_PATH = Config.CHROMA_PATH
# COLLECTION_NAME = Config.COLLECTION_NAME

# _client = None
# _collection = None


# def get_chroma_client() -> chromadb.PersistentClient:
#     global _client
#     if _client is None:
#         _client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
#     return _client


# def get_faq_collection():
#     global _collection
#     if _collection is None:
#         client = get_chroma_client()
#         _collection = client.get_or_create_collection(name=COLLECTION_NAME)
#     return _collection


# def populate_faq_store(df, batch_size: int = 100) -> int:
#     """
#     Populate the ChromaDB collection from a DataFrame with 'input', 'output', 'combined' columns.
#     Returns the number of records inserted.
#     """
#     from tqdm import tqdm

#     client = get_chroma_client()
#     # Clear old collection if exists
#     try:
#         client.delete_collection(COLLECTION_NAME)
#     except Exception:
#         pass
#     collection = client.get_or_create_collection(name=COLLECTION_NAME)

#     count = 0
#     for i in tqdm(range(0, len(df), batch_size), desc="Populating FAQ store"):
#         batch = df.iloc[i : i + batch_size]
#         collection.add(
#             documents=batch["combined"].tolist(),
#             metadatas=[
#                 {"question": q, "answer": a}
#                 for q, a in zip(batch["input"], batch["output"])
#             ],
#             ids=batch.index.astype(str).tolist(),
#         )
#         count += len(batch)

#     global _collection
#     _collection = collection
#     return count


# def search_faqs(query: str, n_results: int = 3) -> List[Dict]:
#     """Search the FAQ vector store and return top results."""
#     collection = get_faq_collection()
#     results = collection.query(
#         query_texts=[query],
#         n_results=n_results,
#         include=["metadatas", "documents", "distances"],
#     )
#     faqs = []
#     if results and results.get("metadatas") and results["metadatas"][0]:
#         for i, meta in enumerate(results["metadatas"][0]):
#             faqs.append({
#                 "question": meta.get("question", ""),
#                 "answer": meta.get("answer", ""),
#                 "score": results["distances"][0][i],
#             })
#     return faqs






"""
backend/db/vector_store.py
Manages the ChromaDB vector store for FAQ retrieval (RAG).
"""

import os
import chromadb
from typing import List, Dict
from backend.config import Config

CHROMA_DB_PATH = Config.CHROMA_PATH
COLLECTION_NAME = Config.COLLECTION_NAME

_client = None
_collection = None


def get_chroma_client() -> chromadb.PersistentClient:
    """Get or create ChromaDB client singleton."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    return _client


def get_faq_collection():
    """Get or create FAQ collection singleton."""
    global _collection
    if _collection is None:
        client = get_chroma_client()
        _collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return _collection


def populate_faq_store(df, batch_size: int = 100) -> int:
    """
    Populate the ChromaDB collection from a DataFrame with 'input', 'output', 'combined' columns.
    Only populates if collection is empty (idempotent operation).
    Returns the number of records inserted.
    """
    from tqdm import tqdm

    collection = get_faq_collection()
    
    # Check if already populated to avoid duplicates
    existing_count = collection.count()
    if existing_count > 0:
        print(f"✅ Vector store already has {existing_count} entries, skipping population")
        print(f"   (Persistent data from volume - no recreation needed)")
        return existing_count
    
    print(f"📝 Populating vector store with {len(df)} entries...")
    
    # Populate in batches
    count = 0
    for i in tqdm(range(0, len(df), batch_size), desc="Populating FAQ store"):
        batch = df.iloc[i : i + batch_size]
        collection.add(
            documents=batch["combined"].tolist(),
            metadatas=[
                {"question": q, "answer": a}
                for q, a in zip(batch["input"], batch["output"])
            ],
            ids=batch.index.astype(str).tolist(),
        )
        count += len(batch)
    
    print(f"✅ Successfully populated vector store with {count} entries")
    return count


def search_faqs(query: str, n_results: int = 3) -> List[Dict]:
    """Search the FAQ vector store and return top results."""
    collection = get_faq_collection()
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["metadatas", "documents", "distances"],
    )
    faqs = []
    if results and results.get("metadatas") and results["metadatas"][0]:
        for i, meta in enumerate(results["metadatas"][0]):
            faqs.append({
                "question": meta.get("question", ""),
                "answer": meta.get("answer", ""),
                "score": results["distances"][0][i],
            })
    return faqs


def check_vector_store_exists() -> bool:
    """Check if vector store exists and has data."""
    try:
        collection = get_faq_collection()
        return collection.count() > 0
    except Exception:
        return False


def get_vector_store_stats() -> dict:
    """Get statistics about the vector store."""
    try:
        collection = get_faq_collection()
        return {
            "exists": True,
            "count": collection.count(),
            "name": COLLECTION_NAME,
            "path": CHROMA_DB_PATH
        }
    except Exception as e:
        return {
            "exists": False,
            "error": str(e),
            "path": CHROMA_DB_PATH
        }