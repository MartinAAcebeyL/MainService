from app import app
from sqlmodel import SQLModel
from app.models.db import engine


@app.on_event("startup")
async def on_startup():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(e)


@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()
