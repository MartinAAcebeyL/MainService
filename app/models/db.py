from sqlmodel import create_engine, Session
from decouple import config


postgres_url = config("DATABASE_URL")
engine = create_engine(postgres_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
    