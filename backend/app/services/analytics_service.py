"""
Analytics service for correlation analysis and statistics
"""

from typing import List, Optional, Dict
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.metric import Metric
from app.models.entry import Entry, EntryValue
from app.analytics.correlation import CorrelationEngine, prepare_metric_data, CorrelationResult
import numpy as np


class AnalyticsService:
    """Service for analytics operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_correlations(
        self,
        user_id: int,
        metric_ids: Optional[List[int]] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        algorithm: str = 'pearson',
        max_lag: int = 7,
        min_significance: float = 0.05,
        only_significant: bool = False
    ) -> List[CorrelationResult]:
        """
        Calculate correlations between metrics

        Args:
            user_id: User ID
            metric_ids: List of metric IDs to analyze (None = all)
            date_from: Start date for analysis
            date_to: End date for analysis
            algorithm: Correlation algorithm
            max_lag: Maximum lag in days
            min_significance: P-value threshold
            only_significant: Only return significant correlations

        Returns:
            List of CorrelationResult objects
        """
        # Get metrics
        query = self.db.query(Metric).filter(
            Metric.user_id == user_id,
            Metric.archived == False
        )

        if metric_ids:
            query = query.filter(Metric.id.in_(metric_ids))

        metrics = query.all()

        if len(metrics) < 2:
            return []

        # Get entries with date filtering
        entry_query = self.db.query(Entry).filter(Entry.user_id == user_id)

        if date_from:
            entry_query = entry_query.filter(Entry.entry_date >= date_from)
        if date_to:
            entry_query = entry_query.filter(Entry.entry_date <= date_to)

        entries = entry_query.order_by(Entry.entry_date).all()

        if len(entries) < 7:
            return []

        # Prepare data for each metric
        metrics_data = {}
        for metric in metrics:
            # Convert entries to dictionaries for prepare_metric_data
            entry_dicts = []
            for entry in entries:
                entry_dict = {
                    'entry_date': str(entry.entry_date),
                    'values': [
                        {
                            'metric_id': v.metric_id,
                            'value_numeric': v.value_numeric,
                            'value_boolean': v.value_boolean,
                            'value_text': v.value_text
                        }
                        for v in entry.values
                    ]
                }
                entry_dicts.append(entry_dict)

            data = prepare_metric_data(entry_dicts, metric.id, metric.value_type)

            metrics_data[metric.id] = {
                'name': metric.name_key,
                'data': data
            }

        # Run correlation analysis
        engine = CorrelationEngine(
            min_significance=min_significance,
            min_sample_size=7
        )

        results = engine.analyze_all_pairs(
            metrics_data=metrics_data,
            algorithm=algorithm,
            max_lag=max_lag,
            only_significant=only_significant
        )

        return results

    def get_statistics(
        self,
        user_id: int,
        metric_ids: Optional[List[int]] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None
    ) -> Dict:
        """
        Get basic statistics for metrics

        Args:
            user_id: User ID
            metric_ids: List of metric IDs (None = all)
            date_from: Start date
            date_to: End date

        Returns:
            Dictionary with statistics for each metric
        """
        # Get metrics
        query = self.db.query(Metric).filter(
            Metric.user_id == user_id,
            Metric.archived == False
        )

        if metric_ids:
            query = query.filter(Metric.id.in_(metric_ids))

        metrics = query.all()

        # Get entries
        entry_query = self.db.query(Entry).filter(Entry.user_id == user_id)

        if date_from:
            entry_query = entry_query.filter(Entry.entry_date >= date_from)
        if date_to:
            entry_query = entry_query.filter(Entry.entry_date <= date_to)

        entries = entry_query.order_by(Entry.entry_date).all()

        # Calculate statistics for each metric
        statistics = []

        for metric in metrics:
            # Convert entries to dictionaries
            entry_dicts = []
            for entry in entries:
                entry_dict = {
                    'entry_date': str(entry.entry_date),
                    'values': [
                        {
                            'metric_id': v.metric_id,
                            'value_numeric': v.value_numeric,
                            'value_boolean': v.value_boolean
                        }
                        for v in entry.values
                    ]
                }
                entry_dicts.append(entry_dict)

            data = prepare_metric_data(entry_dicts, metric.id, metric.value_type)

            # Remove NaN values
            clean_data = [x for x in data if not np.isnan(x)]

            if len(clean_data) == 0:
                continue

            stats = {
                'metric_id': metric.id,
                'metric_name': metric.name_key,
                'count': len(clean_data),
                'mean': float(np.mean(clean_data)),
                'median': float(np.median(clean_data)),
                'std_dev': float(np.std(clean_data)),
                'min_value': float(np.min(clean_data)),
                'max_value': float(np.max(clean_data))
            }

            statistics.append(stats)

        return statistics
