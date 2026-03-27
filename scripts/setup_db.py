"""
scripts/setup_db.py
One-time setup script. Run this once before starting the backend.

Usage:
    python scripts/setup_db.py
"""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from backend.db.seed_data import generate_sample_data
from backend.db.database import connect_db, drop_and_create_tables, insert_data
from backend.db.vector_store import populate_faq_store
from backend.config import Config

# def setup_sqlite():
#     """Create and seed the SQLite database."""

#     Config.ensure_directories()
#     print("⏳ Generating synthetic insurance data...")
#     data = generate_sample_data()

#     print("⏳ Setting up SQLite database...")
#     conn = connect_db()
#     drop_and_create_tables(conn)
#     insert_data(conn, data)
#     conn.close()

#     db_path = os.getenv("DB_PATH", "insurance_support.db")
#     print(f"✅ SQLite database created: {db_path}")
#     for name, df in data.items():
#         print(f"   • {name}: {len(df):,} rows")


def setup_sqlite():
    """Create and seed the SQLite database only if it doesn't exist"""
    
    # Check if database already exists and has tables
    Config.ensure_directories()
    
    db_exists = os.path.exists(Config.SQLITE_PATH)
    
    if db_exists:
        # Check if tables exist
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
            if cursor.fetchone():
                print(f"✅ SQLite database already exists at {Config.SQLITE_PATH}")
                conn.close()
                return
            conn.close()
        except:
            pass
    
    print("⏳ Generating synthetic insurance data...")
    data = generate_sample_data()

    print("⏳ Setting up SQLite database...")
    conn = connect_db()
    drop_and_create_tables(conn)
    insert_data(conn, data)
    conn.close()

    print(f"✅ SQLite database created: {Config.SQLITE_PATH}")
    for name, df in data.items():
        print(f"   • {name}: {len(df):,} rows")

# def setup_vector_store():
#     """Load FAQ dataset and populate ChromaDB."""
      
#     print("\n⏳ Loading FAQ dataset from HuggingFace (deccan-ai/insuranceQA-v2)...")
#     try:
#         from datasets import load_dataset
#         import pandas as pd

#         ds = load_dataset("deccan-ai/insuranceQA-v2")
#         df = pd.concat([split.to_pandas() for split in ds.values()], ignore_index=True)
#         df["combined"] = "Question: " + df["input"] + " \n Answer:  " + df["output"]

#         # Use a 500-record sample for speed
#         df = df.sample(500, random_state=42).reset_index(drop=True)
#         print(f"   Dataset loaded: {len(df)} FAQ entries selected")

#         print("⏳ Populating ChromaDB vector store...")
#         count = populate_faq_store(df)
#         chroma_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
#         print(f"✅ ChromaDB vector store populated: {count} FAQ entries → {chroma_path}")

#     except Exception as e:
#         print(f"⚠️  Could not load FAQ dataset: {e}")
#         print("   The general_help_agent will have an empty knowledge base.")
 
def setup_vector_store():
    """Load FAQ dataset and populate ChromaDB only if not already exists in persistent volume."""
    
    from backend.db.vector_store import check_vector_store_exists, get_vector_store_stats, populate_faq_store
    
    print("\n🔍 Checking for existing vector store in persistent volume...")
    
    # Check if vector store already exists and has data
    if check_vector_store_exists():
        stats = get_vector_store_stats()
        print(f"✅ Found existing vector store with {stats['count']} entries")
        print(f"   Location: {stats['path']}")
        print(f"   Collection: {stats['name']}")
        print(f"   Reusing existing vector store (no recreation needed)")
        return stats['count']
    
    print("   No existing vector store found or it's empty")
    print("   Will create new vector store...")
    
    # Load and populate FAQ data
    print("\n⏳ Loading FAQ dataset from HuggingFace (deccan-ai/insuranceQA-v2)...")
    try:
        from datasets import load_dataset
        import pandas as pd

        ds = load_dataset("deccan-ai/insuranceQA-v2")
        df = pd.concat([split.to_pandas() for split in ds.values()], ignore_index=True)
        df["combined"] = "Question: " + df["input"] + " \n Answer:  " + df["output"]

        # Use a 500-record sample for speed
        df = df.sample(500, random_state=42).reset_index(drop=True)
        print(f"   Dataset loaded: {len(df)} FAQ entries selected")

        # Populate vector store (will check again if already populated)
        count = populate_faq_store(df)
        
        chroma_path = os.getenv("CHROMA_DB_PATH", "./chroma_db")
        print(f"✅ ChromaDB vector store ready: {count} FAQ entries → {chroma_path}")
        return count

    except Exception as e:
        print(f"⚠️  Could not load FAQ dataset: {e}")
        print("   The general_help_agent will have an empty knowledge base.")
        return 0

if __name__ == "__main__":
    setup_sqlite()
    setup_vector_store()
    print("\n🎉 Setup complete! You can now start the backend:")
    print("   uvicorn backend.main:app --reload --port 8000")
