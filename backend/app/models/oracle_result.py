import uuid
from typing import Optional
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base


class OracleResult(Base):
    __tablename__ = "oracle_results"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    test_case_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("test_cases.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )
    expected_output: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    comparison_mode: Mapped[str] = mapped_column(String(30), default="EXACT_MATCH", nullable=False)
    oracle_source: Mapped[str] = mapped_column(String(100), default="unverified", nullable=False)
    verification_status: Mapped[str] = mapped_column(String(30), default="UNVERIFIED", nullable=False)

    # Relationship
    test_case = relationship("TestCase", back_populates="oracle_result")
