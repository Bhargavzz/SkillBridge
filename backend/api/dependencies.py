from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import settings
from core.exceptions import DatabaseConnectionError

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    except Exception as exc:
        session.rollback()
        raise DatabaseConnectionError("Database session error") from exc
    finally:
        session.close()


def get_llm_client():
    from langchain_groq import ChatGroq
    return ChatGroq(
        model="llama3-70b-8192",
        api_key=settings.groq_api_key,
        temperature=0,
    )
