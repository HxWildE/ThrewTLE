import datetime
import uuid
from typing import Any, List, Optional
from sqlalchemy import DateTime, Enum, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base
from sqlalchemy.sql import func


class Problem(Base):
    __tablename__ = "problems"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    source: Mapped[str] = mapped_column(String(50), default="leetcode", nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, index=True, nullable=False)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(20), nullable=False)  # EASY, MEDIUM, HARD
    content: Mapped[str] = mapped_column(Text, default="", nullable=False)
    constraints: Mapped[List[str]] = mapped_column(JSON, default=list, nullable=False)
    input_schema: Mapped[List[dict]] = mapped_column(JSON, default=list, nullable=False)
    support_status: Mapped[str] = mapped_column(String(30), default="SUPPORTED", nullable=False)  # SUPPORTED, PARTIAL, UNSUPPORTED_FORMAT

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    # Relationships
    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
    generation_runs = relationship("GenerationRun", back_populates="problem")
