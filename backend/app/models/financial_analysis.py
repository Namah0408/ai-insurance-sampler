import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class FinancialAnalysis(Base):

    __tablename__ = "financial_analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    proposal_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "proposals.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    risk_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    annual_income: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    annual_premium: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    sum_assured: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    premium_to_income_ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    sum_assured_to_income_ratio: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    account_age_days: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    findings: Mapped[list[Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    flags: Mapped[list[Any]] = mapped_column(
        JSONB,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now().astimezone(),
        nullable=False,
    )

    proposal = relationship(
        "Proposal",
        back_populates="financial_analyses",
    )