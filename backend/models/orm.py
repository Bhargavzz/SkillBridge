import uuid
from datetime import datetime, timezone
from typing import List, Optional

from pgvector.sqlalchemy import Vector
from sqlalchemy import Boolean, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# ==========================================
# APP DOMAIN: Users & Sessions
# ==========================================


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    github_username: Mapped[Optional[str]] = mapped_column(String)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    sessions: Mapped[List["Session"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    __tablename__ = "sessions"

    # This ID acts as the LangGraph 'thread_id'
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    target_role: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="processing")  # processing, completed, failed
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates="sessions")
    roadmap: Mapped[Optional["Roadmap"]] = relationship(back_populates="session", uselist=False, cascade="all, delete-orphan")


class Roadmap(Base):
    __tablename__ = "roadmaps"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id", ondelete="CASCADE"), unique=True)
    roadmap_data: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    session: Mapped["Session"] = relationship(back_populates="roadmap")


# ==========================================
# RAG DOMAIN: Global Market Intelligence
# ==========================================


class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_title: Mapped[str] = mapped_column(String, nullable=False)
    company: Mapped[str] = mapped_column(String)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String)  # e.g., LinkedIn, Wellfound
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    embedding: Mapped[Optional["JobEmbedding"]] = relationship(back_populates="job", uselist=False, cascade="all, delete-orphan")


class JobEmbedding(Base):
    __tablename__ = "job_embeddings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("job_postings.id", ondelete="CASCADE"),unique=True)
    embedding: Mapped[Vector] = mapped_column(Vector(1024))

    job: Mapped["JobPosting"] = relationship(back_populates="embedding")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String, nullable=False)
    provider: Mapped[str] = mapped_column(String)  # e.g., Coursera, Udemy
    url: Mapped[str] = mapped_column(String, nullable=False)
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    embedding: Mapped[Optional["CourseEmbedding"]] = relationship(back_populates="course", uselist=False, cascade="all, delete-orphan")


class CourseEmbedding(Base):
    __tablename__ = "course_embeddings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    course_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"),unique=True)
    embedding: Mapped[Vector] = mapped_column(Vector(1024))

    course: Mapped["Course"] = relationship(back_populates="embedding")


# HNSW indexes must be defined after table classes are declared so SQLAlchemy
# can resolve the column references correctly at module import time.
Index(
    "hnsw_job_embedding_idx",
    JobEmbedding.embedding,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding": "vector_cosine_ops"},
)
Index(
    "hnsw_course_embedding_idx",
    CourseEmbedding.embedding,
    postgresql_using="hnsw",
    postgresql_with={"m": 16, "ef_construction": 64},
    postgresql_ops={"embedding": "vector_cosine_ops"},
)
