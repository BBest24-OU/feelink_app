"""
Metric model
"""
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Numeric,
    ForeignKey, CheckConstraint, UniqueConstraint
)
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class Metric(Base, TimestampMixin):
    """Custom user metric model"""
    __tablename__ = "metrics"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    # Metric Definition
    name_key = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, index=True)

    # Value Type & Constraints
    value_type = Column(String(20), nullable=False)
    min_value = Column(Numeric(10, 2), nullable=True)
    max_value = Column(Numeric(10, 2), nullable=True)

    # Display
    description = Column(Text, nullable=True)
    color = Column(String(7), nullable=True)  # Hex color
    icon = Column(String(50), nullable=True)
    display_order = Column(Integer, default=0, server_default='0')

    # Status
    archived = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="metrics")
    entry_values = relationship(
        "EntryValue",
        back_populates="metric",
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint('user_id', 'name_key', name='unique_user_metric_name'),
        CheckConstraint(
            "category IN ('physical', 'psychological', 'triggers', "
            "'medications', 'selfcare', 'wellness', 'notes')",
            name="check_category"
        ),
        CheckConstraint(
            "value_type IN ('range', 'number', 'boolean', 'count', 'text')",
            name="check_value_type"
        ),
        CheckConstraint(
            "(value_type != 'range') OR "
            "(min_value IS NOT NULL AND max_value IS NOT NULL AND min_value < max_value)",
            name="check_valid_range"
        ),
    )

    def __repr__(self):
        return f"<Metric(id={self.id}, name_key={self.name_key}, category={self.category})>"
