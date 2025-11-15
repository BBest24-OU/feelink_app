"""
Entry and EntryValue models
"""
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Numeric, Date, DateTime,
    ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base, TimestampMixin


class Entry(Base, TimestampMixin):
    """Daily log entry model"""
    __tablename__ = "entries"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Entry Data
    entry_date = Column(Date, nullable=False, index=True)
    notes = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", back_populates="entries")
    values = relationship(
        "EntryValue",
        back_populates="entry",
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'entry_date', name='unique_user_date'),
        CheckConstraint(
            "entry_date <= CURRENT_DATE",
            name="check_entry_date_not_future"
        ),
    )

    def __repr__(self):
        return f"<Entry(id={self.id}, user_id={self.user_id}, date={self.entry_date})>"


class EntryValue(Base):
    """Metric value within an entry"""
    __tablename__ = "entry_values"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Keys
    entry_id = Column(
        Integer,
        ForeignKey("entries.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    metric_id = Column(
        Integer,
        ForeignKey("metrics.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Polymorphic Value Storage
    value_numeric = Column(Numeric(10, 2), nullable=True)
    value_boolean = Column(Boolean, nullable=True)
    value_text = Column(Text, nullable=True)

    # Metadata
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    # Relationships
    entry = relationship("Entry", back_populates="values")
    metric = relationship("Metric", back_populates="entry_values")

    # Constraints
    __table_args__ = (
        UniqueConstraint('entry_id', 'metric_id', name='unique_entry_metric'),
        CheckConstraint(
            "(value_numeric IS NOT NULL) OR "
            "(value_boolean IS NOT NULL) OR "
            "(value_text IS NOT NULL)",
            name="check_value_not_null"
        ),
    )

    def __repr__(self):
        return f"<EntryValue(id={self.id}, entry_id={self.entry_id}, metric_id={self.metric_id})>"
