from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from vectorstore.chroma_client import resume_collection, jd_collection

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500, chunk_overlap=50
)

def embed_resume(resume_id: int, text: str):
    chunks = splitter.split_text(text)
    vectors = embeddings.embed_documents(chunks)
    resume_collection.add(
        ids=[f"resume_{resume_id}_chunk_{i}" for i in range(len(chunks))],
        documents=chunks, embeddings=vectors
    )

def embed_jd(jd_id: int, text: str):
    chunks = splitter.split_text(text)
    vectors = embeddings.embed_documents(chunks)
    jd_collection.add(
        ids=[f"jd_{jd_id}_chunk_{i}" for i in range(len(chunks))],
        documents=chunks, embeddings=vectors
    )