"""
Script simples para criação das tabelas no banco PostgreSQL.

Execute, por exemplo:
    uvicorn app.main:app --reload
e, antes disso, rode:
    python -m app.init_db
"""

from app.db.session import Base, engine
from app.models import appointment, employee  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()


