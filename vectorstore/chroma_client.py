import chromadb
import os

# Persist ChromaDB data to a local directory
CHROMA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

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
