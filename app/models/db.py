from sqlmodel import create_engine
from decouple import config


postgres_url = config("DATABASE_URL")

engine = create_engine(postgres_url, echo=True)
