from fastapi import FastAPI
from . import models
from app.core.database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()