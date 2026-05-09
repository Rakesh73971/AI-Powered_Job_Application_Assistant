from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from vectorstore.chroma_client import resume_collection, jd_collection
from app.core.config import settings

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=settings.google_api_key
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

def embed_resume(resume_id: int, text: str):
    chunks = splitter.split_text(text)
    if not chunks:
        return
    vectors = embeddings.embed_documents(chunks)
    resume_collection.add(
        ids=[f"resume_{resume_id}_chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=vectors,
        metadatas=[{"resume_id": resume_id} for _ in chunks]
    )

def embed_jd(jd_id: int, text: str):
    chunks = splitter.split_text(text)
    if not chunks:
        return
    vectors = embeddings.embed_documents(chunks)
    jd_collection.add(
        ids=[f"jd_{jd_id}_chunk_{i}" for i in range(len(chunks))],
        documents=chunks,
        embeddings=vectors,
        metadatas=[{"jd_id": jd_id} for _ in chunks]
    )
