from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from core.config import settings
from core.exceptions import DatabaseConnectionError

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    except SQLAlchemyError as exc:
        # Only catch database conn errors
        session.rollback()
        raise DatabaseConnectionError("Database connection error") from exc
    except Exception as exc:
        session.rollback()
        raise
    finally:
        session.close()
