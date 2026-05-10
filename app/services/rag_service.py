from langchain_google_genai import GoogleGenerativeAIEmbeddings
from vectorstore.chroma_client import resume_collection, jd_collection
from app.core.config import settings

embeddings = GoogleGenerativeAIEmbeddings(
    model=settings.google_embedding_model,
    google_api_key=settings.google_api_key
)

def retrieve_resume_context(resume_id: int, query: str, top_k: int = 5) -> str:
    query_vector = embeddings.embed_query(query)

    results = resume_collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where={"resume_id": resume_id}   # removed str()
    )

    docs = results.get("documents", [[]])[0]
    return "\n".join(docs) if docs else ""


def retrieve_jd_context(jd_id: int, query: str, top_k: int = 5) -> str:
    query_vector = embeddings.embed_query(query)

    results = jd_collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where={"jd_id": jd_id}
    )

    docs = results.get("documents", [[]])[0]
    return "\n".join(docs) if docs else ""