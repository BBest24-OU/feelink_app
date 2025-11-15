"""
User API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.models import User
from app.schemas import UserResponse, UserUpdate
from app.services import UserService
from app.security import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user's profile.

    Args:
        current_user: Currently authenticated user

    Returns:
        User profile data
    """
    return UserResponse.from_orm(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update current user's profile.

    Args:
        user_data: Fields to update (language, timezone)
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Updated user profile data
    """
    updated_user = UserService.update_user(db, current_user, user_data)
    return UserResponse.from_orm(updated_user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_current_user_account(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete (deactivate) current user's account.

    Args:
        current_user: Currently authenticated user
        db: Database session

    Returns:
        204 No Content
    """
    UserService.delete_user(db, current_user)
    return None
