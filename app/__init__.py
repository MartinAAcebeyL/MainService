from fastapi import FastAPI
from sqlmodel import SQLModel
from .models.db import engine

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    SQLModel.metadata.create_all(engine)


@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()
