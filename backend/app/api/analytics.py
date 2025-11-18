"""
Analytics API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.database import get_db
from app.security.dependencies import get_current_user
from app.models.user import User
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import (
    CorrelationRequest,
    CorrelationResponse,
    CorrelationResultSchema,
    StatisticsResponse,
    MetricStatistics
)

router = APIRouter()


@router.post("/correlations", response_model=CorrelationResponse)
def calculate_correlations(
    request: CorrelationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calculate correlations between metrics

    This endpoint analyzes correlations between user's metrics using
    Pearson, Spearman, or Kendall correlation coefficients.

    Features:
    - Lag correlation analysis (delayed effects up to max_lag days)
    - Statistical significance testing
    - Filtering by metric IDs and date range
    - Minimum 7 data points required

    Example:
        POST /api/v1/analytics/correlations
        {
            "algorithm": "pearson",
            "max_lag": 7,
            "only_significant": true
        }
    """
    service = AnalyticsService(db)

    try:
        results = service.get_correlations(
            user_id=current_user.id,
            metric_ids=request.metric_ids,
            date_from=request.date_from,
            date_to=request.date_to,
            algorithm=request.algorithm,
            max_lag=request.max_lag,
            min_significance=request.min_significance,
            only_significant=request.only_significant
        )

        # Convert CorrelationResult objects to response schema
        correlation_schemas = [
            CorrelationResultSchema(
                metric_1_id=r.metric_1_id,
                metric_1_name=r.metric_1_name,
                metric_2_id=r.metric_2_id,
                metric_2_name=r.metric_2_name,
                coefficient=r.coefficient,
                p_value=r.p_value,
                lag=r.lag,
                strength=r.strength,
                significant=r.significant,
                direction=r.direction,
                sample_size=r.sample_size,
                algorithm=r.algorithm
            )
            for r in results
        ]

        return CorrelationResponse(
            correlations=correlation_schemas,
            algorithm_used=request.algorithm,
            date_range={
                'from': str(request.date_from) if request.date_from else None,
                'to': str(request.date_to) if request.date_to else None
            },
            total_correlations=len(correlation_schemas)
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Correlation analysis failed: {str(e)}")


@router.get("/statistics", response_model=StatisticsResponse)
def get_statistics(
    metric_ids: str = None,
    date_from: str = None,
    date_to: str = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get basic statistics for metrics

    Returns mean, median, standard deviation, min, and max for each metric.

    Query Parameters:
    - metric_ids: Comma-separated list of metric IDs (optional)
    - date_from: Start date in YYYY-MM-DD format (optional)
    - date_to: End date in YYYY-MM-DD format (optional)

    Example:
        GET /api/v1/analytics/statistics?metric_ids=1,2,3&date_from=2024-01-01
    """
    service = AnalyticsService(db)

    # Parse metric_ids if provided
    parsed_metric_ids = None
    if metric_ids:
        try:
            parsed_metric_ids = [int(id.strip()) for id in metric_ids.split(',')]
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid metric_ids format")

    # Parse dates if provided
    from datetime import datetime
    parsed_date_from = None
    parsed_date_to = None

    if date_from:
        try:
            parsed_date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_from format (use YYYY-MM-DD)")

    if date_to:
        try:
            parsed_date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date_to format (use YYYY-MM-DD)")

    try:
        stats = service.get_statistics(
            user_id=current_user.id,
            metric_ids=parsed_metric_ids,
            date_from=parsed_date_from,
            date_to=parsed_date_to
        )

        return StatisticsResponse(
            statistics=[MetricStatistics(**s) for s in stats],
            date_range={
                'from': date_from,
                'to': date_to
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Statistics calculation failed: {str(e)}")
