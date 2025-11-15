"""
FastAPI dependencies for authentication
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional

from app.utils.database import get_db
from app.models import User
from app.security.jwt import verify_token

# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.

    Args:
        credentials: Bearer token from Authorization header
        db: Database session

    Returns:
        Current authenticated User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify the token
    payload = verify_token(credentials.credentials, token_type="access")
    if payload is None:
        raise credentials_exception

    # Get user ID from payload
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    # Fetch user from database
    user = db.query(User).filter(User.id == user_id, User.deleted_at.is_(None)).first()
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to get the current active (non-deleted) user.

    Args:
        current_user: Current user from get_current_user dependency

    Returns:
        Current active User object

    Raises:
        HTTPException: If user is deactivated
    """
    if current_user.deleted_at is not None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
    return current_user
