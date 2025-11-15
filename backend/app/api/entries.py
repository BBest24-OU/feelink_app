"""
Entries API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import Optional

from app.utils.database import get_db
from app.models import User
from app.schemas import EntryCreate, EntryUpdate, EntryResponse, EntryListResponse
from app.services import EntryService
from app.security import get_current_active_user

router = APIRouter(prefix="/entries", tags=["Entries"])


@router.get("", response_model=EntryListResponse)
async def list_entries(
    date_from: Optional[date] = Query(None, description="Start date filter (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date filter (YYYY-MM-DD)"),
    limit: int = Query(100, ge=1, le=500, description="Maximum number of entries"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all entries for the current user with optional filters.

    Args:
        date_from: Optional start date filter
        date_to: Optional end date filter
        limit: Maximum number of entries to return (default: 100, max: 500)
        offset: Offset for pagination (default: 0)
        current_user: Currently authenticated user
        db: Database session

    Returns:
        List of user's entries
    """
    entries, total = EntryService.get_user_entries(
        db, current_user, date_from, date_to, limit, offset
    )

    return EntryListResponse(
        entries=[EntryResponse.from_orm(e) for e in entries],
        total=total,
        has_more=total > (offset + limit)
    )


@router.post("", response_model=EntryResponse, status_code=status.HTTP_201_CREATED)
async def create_entry(
    entry_data: EntryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new daily log entry.

    Args:
        entry_data: Entry creation data (date, notes, values)
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Created entry

    Raises:
        400: If entry for this date already exists or validation fails
    """
    entry = EntryService.create_entry(db, current_user, entry_data)
    return EntryResponse.from_orm(entry)


@router.get("/{entry_id}", response_model=EntryResponse)
async def get_entry(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific entry by ID.

    Args:
        entry_id: Entry ID
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Entry data

    Raises:
        404: If entry not found
    """
    entry = EntryService.get_entry_by_id(db, current_user, entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )
    return EntryResponse.from_orm(entry)


@router.get("/date/{entry_date}", response_model=EntryResponse)
async def get_entry_by_date(
    entry_date: date,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get entry for a specific date.

    Args:
        entry_date: Date of entry (YYYY-MM-DD)
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Entry data

    Raises:
        404: If entry not found for this date
    """
    entry = EntryService.get_entry_by_date(db, current_user, entry_date)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Entry not found for date {entry_date}"
        )
    return EntryResponse.from_orm(entry)


@router.patch("/{entry_id}", response_model=EntryResponse)
async def update_entry(
    entry_id: int,
    entry_data: EntryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update an entry.

    Args:
        entry_id: Entry ID
        entry_data: Fields to update (notes, values)
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Updated entry

    Raises:
        404: If entry not found
    """
    entry = EntryService.get_entry_by_id(db, current_user, entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )

    updated_entry = EntryService.update_entry(db, entry, entry_data)
    return EntryResponse.from_orm(updated_entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entry(
    entry_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete an entry.

    Args:
        entry_id: Entry ID
        current_user: Currently authenticated user
        db: Database session

    Returns:
        204 No Content

    Raises:
        404: If entry not found
    """
    entry = EntryService.get_entry_by_id(db, current_user, entry_id)
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entry not found"
        )

    EntryService.delete_entry(db, entry)
    return None
