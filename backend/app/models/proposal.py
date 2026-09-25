import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Proposal(Base):
    __tablename__ = "proposals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    proposal_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    sum_assured: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    annual_premium: Mapped[float] = mapped_column(
        Numeric(15, 2),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="draft",
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now().astimezone(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now().astimezone(),
        onupdate=lambda: datetime.now().astimezone(),
        nullable=False,
    )

    customer = relationship(
        "Customer",
        back_populates="proposals",
    )

    documents = relationship(
        "Document",
        back_populates="proposal",
        cascade="all, delete-orphan",
    )