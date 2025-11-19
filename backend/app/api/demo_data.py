"""
Demo Data API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.models import User
from app.services.demo_data import DemoDataService
from app.security import get_current_active_user

router = APIRouter(prefix="/demo-data", tags=["Demo Data"])


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_demo_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Generate demo data for the current user for the last 180 days.

    This will create realistic metrics and entries to showcase the app's functionality.

    Args:
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Summary of generated data

    Raises:
        400: If user already has data
    """
    try:
        result = DemoDataService.generate_demo_data(db, current_user)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_user_data(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Clear all user data (metrics and entries).

    This restores the account to its initial state, as if just created.

    Args:
        current_user: Currently authenticated user
        db: Database session

    Returns:
        204 No Content
    """
    try:
        DemoDataService.clear_user_data(db, current_user)
        return None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to clear user data"
        )
