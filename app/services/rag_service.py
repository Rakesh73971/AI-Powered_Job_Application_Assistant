from langchain_openai import OpenAIEmbeddings
from vectorstore.chroma_client import resume_collection, jd_collection

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def retrieve_resume_context(resume_id: int, query: str, top_k=5):
    query_vector = embeddings.embed_query(query)
    results = resume_collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where={"resume_id": resume_id}
    )
    return "\n".join(results["documents"][0])

def retrieve_jd_context(jd_id: int, query: str, top_k=5):
    query_vector = embeddings.embed_query(query)
    results = jd_collection.query(
        query_embeddings=[query_vector],
        n_results=top_k,
        where={"jd_id": jd_id}
    )
    return "\n".join(results["documents"][0])