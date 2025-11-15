"""
User service - business logic for user management
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional

from app.models import User
from app.schemas import UserRegister, UserUpdate
from app.security import hash_password, verify_password


class UserService:
    """Service class for user operations"""

    @staticmethod
    def create_user(db: Session, user_data: UserRegister) -> User:
        """
        Create a new user account.

        Args:
            db: Database session
            user_data: User registration data

        Returns:
            Created User object

        Raises:
            HTTPException: If email already exists
        """
        # Hash the password
        hashed_password = hash_password(user_data.password)

        # Create user instance
        new_user = User(
            email=user_data.email.lower(),
            password_hash=hashed_password,
            language=user_data.language,
            timezone=user_data.timezone
        )

        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user by email and password.

        Args:
            db: Database session
            email: User email
            password: Plaintext password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = db.query(User).filter(
            User.email == email.lower(),
            User.deleted_at.is_(None)
        ).first()

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(
            User.id == user_id,
            User.deleted_at.is_(None)
        ).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            db: Database session
            email: User email

        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(
            User.email == email.lower(),
            User.deleted_at.is_(None)
        ).first()

    @staticmethod
    def update_user(db: Session, user: User, user_data: UserUpdate) -> User:
        """
        Update user profile.

        Args:
            db: Database session
            user: User object to update
            user_data: Update data

        Returns:
            Updated User object
        """
        update_data = user_data.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user: User) -> None:
        """
        Soft delete user account.

        Args:
            db: Database session
            user: User object to delete
        """
        from datetime import datetime
        user.deleted_at = datetime.utcnow()
        db.commit()
