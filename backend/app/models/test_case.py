import datetime
import uuid
from typing import Any, Dict, Optional
from sqlalchemy import DateTime, ForeignKey, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base_class import Base


class TestCase(Base):
    __tablename__ = "test_cases"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    problem_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("problems.id", ondelete="CASCADE"), nullable=False, index=True
    )
    raw_input: Mapped[str] = mapped_column(Text, nullable=False)
    structured_input: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
    category: Mapped[str] = mapped_column(String(30), nullable=False)  # BASIC, BOUNDARY, STRUCTURAL, NUMERIC_EXTREMES, STRESS
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    generation_method: Mapped[str] = mapped_column(String(40), default="DETERMINISTIC_STRATEGY", nullable=False)
    provenance: Mapped[str] = mapped_column(String(200), default="generator", nullable=False)
    validation_status: Mapped[str] = mapped_column(String(30), default="VALIDATED", nullable=False)
    fingerprint: Mapped[str] = mapped_column(String(64), index=True, nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # Relationships
    problem = relationship("Problem", back_populates="test_cases")
    oracle_result = relationship("OracleResult", back_populates="test_case", uselist=False, cascade="all, delete-orphan")
