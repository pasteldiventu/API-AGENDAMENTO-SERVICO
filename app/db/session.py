from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """Base declarativa para os modelos SQLAlchemy."""


engine = create_engine(settings.DATABASE_URL, echo=False, future=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Dependência do FastAPI para fornecer uma sessão de banco de dados.
    Fecha a sessão ao final da requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



