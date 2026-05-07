from fastapi import FastAPI
from . import models
from app.db.database import engine
from .routers import oauth, user,resume,cover_letter,job_description

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(user.router)
app.include_router(oauth.router)
app.include_router(resume.router)
app.include_router(cover_letter.router)
app.include_router(job_description.router)