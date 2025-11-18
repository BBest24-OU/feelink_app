"""
Entry service - business logic for daily log entries
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import date
from decimal import Decimal

from app.models import User, Entry, EntryValue, Metric
from app.schemas import EntryCreate, EntryUpdate, EntryValueCreate


class EntryService:
    """Service class for entry operations"""

    @staticmethod
    def create_entry(db: Session, user: User, entry_data: EntryCreate) -> Entry:
        """
        Create a new daily log entry.

        Args:
            db: Database session
            user: User who owns the entry
            entry_data: Entry creation data

        Returns:
            Created Entry object with values

        Raises:
            HTTPException: If entry for this date already exists or metric validation fails
        """
        # Create entry
        new_entry = Entry(
            user_id=user.id,
            entry_date=entry_data.entry_date,
            notes=entry_data.notes
        )

        try:
            db.add(new_entry)
            db.flush()  # Get the entry ID

            # Create entry values
            for value_data in entry_data.values:
                # Verify metric exists and belongs to user
                metric = db.query(Metric).filter(
                    Metric.id == value_data.metric_id,
                    Metric.user_id == user.id,
                    Metric.archived == False
                ).first()

                if not metric:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Metric {value_data.metric_id} not found or archived"
                    )

                # Create entry value based on metric type
                entry_value = EntryService._create_entry_value(
                    entry_id=new_entry.id,
                    metric=metric,
                    value_data=value_data
                )
                db.add(entry_value)

            db.commit()
            db.refresh(new_entry)
            return new_entry

        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Entry for date {entry_data.entry_date} already exists"
            )

    @staticmethod
    def _create_entry_value(
        entry_id: int,
        metric: Metric,
        value_data: EntryValueCreate
    ) -> EntryValue:
        """
        Create an EntryValue with appropriate type-based storage.

        Args:
            entry_id: Entry ID
            metric: Metric object
            value_data: Value data

        Returns:
            EntryValue object

        Raises:
            HTTPException: If value doesn't match metric type
        """
        entry_value = EntryValue(
            entry_id=entry_id,
            metric_id=metric.id
        )

        # Store value in appropriate column based on metric type
        if metric.value_type in ('range', 'number', 'count'):
            if not isinstance(value_data.value, (int, float, Decimal)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Metric {metric.name_key} expects numeric value"
                )

            numeric_value = Decimal(str(value_data.value))

            # Validate range constraints
            if metric.value_type == 'range':
                if metric.min_value is not None and numeric_value < metric.min_value:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Value {numeric_value} below minimum {metric.min_value}"
                    )
                if metric.max_value is not None and numeric_value > metric.max_value:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Value {numeric_value} above maximum {metric.max_value}"
                    )

            entry_value.value_numeric = numeric_value

        elif metric.value_type == 'boolean':
            if not isinstance(value_data.value, bool):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Metric {metric.name_key} expects boolean value"
                )
            entry_value.value_boolean = value_data.value

        elif metric.value_type == 'text':
            if not isinstance(value_data.value, str):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Metric {metric.name_key} expects text value"
                )
            entry_value.value_text = value_data.value

        return entry_value

    @staticmethod
    def get_user_entries(
        db: Session,
        user: User,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        limit: int = 100,
        offset: int = 0
    ) -> tuple[List[Entry], int]:
        """
        Get entries for a user with optional date filtering.

        Args:
            db: Database session
            user: User who owns the entries
            date_from: Optional start date filter
            date_to: Optional end date filter
            limit: Maximum number of entries to return
            offset: Offset for pagination

        Returns:
            Tuple of (list of Entry objects, total count)
        """
        query = db.query(Entry).filter(Entry.user_id == user.id)

        if date_from:
            query = query.filter(Entry.entry_date >= date_from)
        if date_to:
            query = query.filter(Entry.entry_date <= date_to)

        total = query.count()
        entries = query.order_by(Entry.entry_date.desc()).limit(limit).offset(offset).all()

        return entries, total

    @staticmethod
    def get_entry_by_id(db: Session, user: User, entry_id: int) -> Optional[Entry]:
        """
        Get a specific entry by ID (must belong to user).

        Args:
            db: Database session
            user: User who should own the entry
            entry_id: Entry ID

        Returns:
            Entry object if found and owned by user, None otherwise
        """
        return db.query(Entry).filter(
            Entry.id == entry_id,
            Entry.user_id == user.id
        ).first()

    @staticmethod
    def get_entry_by_date(db: Session, user: User, entry_date: date) -> Optional[Entry]:
        """
        Get entry for a specific date.

        Args:
            db: Database session
            user: User who owns the entry
            entry_date: Date of entry

        Returns:
            Entry object if found, None otherwise
        """
        return db.query(Entry).filter(
            Entry.user_id == user.id,
            Entry.entry_date == entry_date
        ).first()

    @staticmethod
    def update_entry(
        db: Session,
        entry: Entry,
        entry_data: EntryUpdate
    ) -> Entry:
        """
        Update an entry.

        Args:
            db: Database session
            entry: Entry object to update
            entry_data: Update data

        Returns:
            Updated Entry object
        """
        if entry_data.notes is not None:
            entry.notes = entry_data.notes

        if entry_data.values is not None:
            # Delete existing values
            db.query(EntryValue).filter(EntryValue.entry_id == entry.id).delete()

            # Create new values
            for value_data in entry_data.values:
                metric = db.query(Metric).filter(
                    Metric.id == value_data.metric_id,
                    Metric.user_id == entry.user_id,
                    Metric.archived == False
                ).first()

                if not metric:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Metric {value_data.metric_id} not found or archived"
                    )

                entry_value = EntryService._create_entry_value(
                    entry_id=entry.id,
                    metric=metric,
                    value_data=value_data
                )
                db.add(entry_value)

        db.commit()
        db.refresh(entry)
        return entry

    @staticmethod
    def delete_entry(db: Session, entry: Entry) -> None:
        """
        Delete an entry (hard delete).

        Args:
            db: Database session
            entry: Entry object to delete
        """
        db.delete(entry)
        db.commit()
