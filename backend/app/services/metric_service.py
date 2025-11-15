"""
Metric service - business logic for metric management
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import List, Optional

from app.models import User, Metric
from app.schemas import MetricCreate, MetricUpdate


class MetricService:
    """Service class for metric operations"""

    @staticmethod
    def create_metric(db: Session, user: User, metric_data: MetricCreate) -> Metric:
        """
        Create a new metric for a user.

        Args:
            db: Database session
            user: User who owns the metric
            metric_data: Metric creation data

        Returns:
            Created Metric object

        Raises:
            HTTPException: If metric with same name_key already exists for user
        """
        # Get the highest display_order for this user
        max_order = db.query(Metric).filter(
            Metric.user_id == user.id
        ).count()

        new_metric = Metric(
            user_id=user.id,
            name_key=metric_data.name_key,
            category=metric_data.category,
            value_type=metric_data.value_type,
            min_value=metric_data.min_value,
            max_value=metric_data.max_value,
            description=metric_data.description,
            color=metric_data.color,
            icon=metric_data.icon,
            display_order=max_order
        )

        try:
            db.add(new_metric)
            db.commit()
            db.refresh(new_metric)
            return new_metric
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Metric with name_key '{metric_data.name_key}' already exists"
            )

    @staticmethod
    def get_user_metrics(
        db: Session,
        user: User,
        include_archived: bool = False
    ) -> List[Metric]:
        """
        Get all metrics for a user.

        Args:
            db: Database session
            user: User who owns the metrics
            include_archived: Whether to include archived metrics

        Returns:
            List of Metric objects
        """
        query = db.query(Metric).filter(Metric.user_id == user.id)

        if not include_archived:
            query = query.filter(Metric.archived == False)

        return query.order_by(Metric.display_order, Metric.created_at).all()

    @staticmethod
    def get_metric_by_id(
        db: Session,
        user: User,
        metric_id: int
    ) -> Optional[Metric]:
        """
        Get a specific metric by ID (must belong to user).

        Args:
            db: Database session
            user: User who should own the metric
            metric_id: Metric ID

        Returns:
            Metric object if found and owned by user, None otherwise
        """
        return db.query(Metric).filter(
            Metric.id == metric_id,
            Metric.user_id == user.id
        ).first()

    @staticmethod
    def update_metric(
        db: Session,
        metric: Metric,
        metric_data: MetricUpdate
    ) -> Metric:
        """
        Update a metric.

        Args:
            db: Database session
            metric: Metric object to update
            metric_data: Update data

        Returns:
            Updated Metric object
        """
        update_data = metric_data.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(metric, field, value)

        db.commit()
        db.refresh(metric)
        return metric

    @staticmethod
    def archive_metric(db: Session, metric: Metric) -> Metric:
        """
        Archive a metric (soft delete).

        Args:
            db: Database session
            metric: Metric object to archive

        Returns:
            Updated Metric object
        """
        metric.archived = True
        db.commit()
        db.refresh(metric)
        return metric

    @staticmethod
    def unarchive_metric(db: Session, metric: Metric) -> Metric:
        """
        Unarchive a metric.

        Args:
            db: Database session
            metric: Metric object to unarchive

        Returns:
            Updated Metric object
        """
        metric.archived = False
        db.commit()
        db.refresh(metric)
        return metric

    @staticmethod
    def delete_metric(db: Session, metric: Metric) -> None:
        """
        Permanently delete a metric (hard delete).
        Warning: This will also delete all entry values associated with this metric.

        Args:
            db: Database session
            metric: Metric object to delete
        """
        db.delete(metric)
        db.commit()
