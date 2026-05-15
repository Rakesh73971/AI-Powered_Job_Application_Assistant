import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from app.db.database import engine
from .routers import oauth, user, resume, cover_letter, job_description, analysis, stream


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    models.Base.metadata.create_all(bind=engine)
    os.makedirs("uploads/resumes", exist_ok=True)
    os.makedirs("chroma_db", exist_ok=True)
    print("[OK] AI-Powered Job Application Assistant started successfully.")
    yield

    print("[STOP] Application shutting down.")


app = FastAPI(
    title="AI-Powered Job Application Assistant",
    description=(
        "A backend system that helps job seekers tailor resumes, "
        "generate cover letters, and match JDs using RAG + LangChain + Google Gemini."
    ),
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(oauth.router)
app.include_router(resume.router)
app.include_router(cover_letter.router)
app.include_router(job_description.router)
app.include_router(analysis.router)
app.include_router(stream.router)


@app.get("/", tags=["Health"])
def root():
    return {
        "status": "running",
        "message": "AI-Powered Job Application Assistant API",
        "docs": "/docs"
    }
