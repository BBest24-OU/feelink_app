"""
Metrics API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.models import User
from app.schemas import MetricCreate, MetricUpdate, MetricResponse, MetricListResponse
from app.services import MetricService
from app.security import get_current_active_user

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("", response_model=MetricListResponse)
async def list_metrics(
    include_archived: bool = Query(False, description="Include archived metrics"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all metrics for the current user.

    Args:
        include_archived: Whether to include archived metrics
        current_user: Currently authenticated user
        db: Database session

    Returns:
        List of user's metrics
    """
    metrics = MetricService.get_user_metrics(db, current_user, include_archived)
    return MetricListResponse(
        metrics=[MetricResponse.from_orm(m) for m in metrics],
        total=len(metrics)
    )


@router.post("", response_model=MetricResponse, status_code=status.HTTP_201_CREATED)
async def create_metric(
    metric_data: MetricCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new metric.

    Args:
        metric_data: Metric creation data
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Created metric

    Raises:
        400: If metric with same name_key already exists
    """
    metric = MetricService.create_metric(db, current_user, metric_data)
    return MetricResponse.from_orm(metric)


@router.get("/{metric_id}", response_model=MetricResponse)
async def get_metric(
    metric_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific metric by ID.

    Args:
        metric_id: Metric ID
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Metric data

    Raises:
        404: If metric not found
    """
    metric = MetricService.get_metric_by_id(db, current_user, metric_id)
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Metric not found"
        )
    return MetricResponse.from_orm(metric)


@router.patch("/{metric_id}", response_model=MetricResponse)
async def update_metric(
    metric_id: int,
    metric_data: MetricUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update a metric.

    Args:
        metric_id: Metric ID
        metric_data: Fields to update
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Updated metric

    Raises:
        404: If metric not found
    """
    metric = MetricService.get_metric_by_id(db, current_user, metric_id)
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Metric not found"
        )

    updated_metric = MetricService.update_metric(db, metric, metric_data)
    return MetricResponse.from_orm(updated_metric)


@router.delete("/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_metric(
    metric_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Archive a metric (soft delete).

    Args:
        metric_id: Metric ID
        current_user: Currently authenticated user
        db: Database session

    Returns:
        204 No Content

    Raises:
        404: If metric not found
    """
    metric = MetricService.get_metric_by_id(db, current_user, metric_id)
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Metric not found"
        )

    MetricService.archive_metric(db, metric)
    return None


@router.post("/{metric_id}/unarchive", response_model=MetricResponse)
async def unarchive_metric(
    metric_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Unarchive a metric.

    Args:
        metric_id: Metric ID
        current_user: Currently authenticated user
        db: Database session

    Returns:
        Unarchived metric

    Raises:
        404: If metric not found
    """
    metric = MetricService.get_metric_by_id(db, current_user, metric_id)
    if not metric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Metric not found"
        )

    unarchived_metric = MetricService.unarchive_metric(db, metric)
    return MetricResponse.from_orm(unarchived_metric)
