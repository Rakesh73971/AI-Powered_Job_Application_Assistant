from fastapi import FastAPI
from . import models
from app.db.database import engine
from .routers import oauth, user

models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(user.router)
app.include_router(oauth.router)