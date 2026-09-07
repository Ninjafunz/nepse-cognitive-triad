"""RAG Literature Knowledge Base with pgvector embeddings."""

import uuid
from datetime import datetime
from sqlalchemy import String, Text, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base


class LiteratureKnowledge(Base):
    __tablename__ = "literature_knowledge"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    author: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    work_title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    route_affinity: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # Alpha, Beta, Gamma
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    chunk_text: Mapped[str] = mapped_column(Text, nullable=False)
    embedding = mapped_column(Vector(1536), nullable=True)  # pgvector embedding
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
