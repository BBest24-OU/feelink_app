"""
User model
"""
from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User account model"""
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Authentication
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Preferences
    language = Column(
        String(2),
        default='en',
        nullable=False,
        server_default='en'
    )
    timezone = Column(
        String(50),
        default='UTC',
        nullable=False,
        server_default='UTC'
    )

    # Soft delete
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    metrics = relationship(
        "Metric",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    entries = relationship(
        "Entry",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "language IN ('en', 'pl')",
            name="check_language"
        ),
        CheckConstraint(
            "email = LOWER(email)",
            name="check_email_lowercase"
        ),
    )

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"
