import os
import chromadb

# Persist ChromaDB data to a local directory
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_PATH)

# Collection for resume chunks
resume_collection = client.get_or_create_collection(
    name="resumes",
    metadata={"hnsw:space": "cosine"}
)

# Collection for job description chunks
jd_collection = client.get_or_create_collection(
    name="job_descriptions",
    metadata={"hnsw:space": "cosine"}
)
