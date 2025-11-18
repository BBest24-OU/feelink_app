"""
Correlation analysis engine for FeelInk

Implements Pearson, Spearman, and Kendall correlation coefficients
with lag correlation analysis and statistical significance testing.
"""

from typing import List, Dict, Tuple, Optional
import pandas as pd
import numpy as np
from scipy import stats
from dataclasses import dataclass


@dataclass
class CorrelationResult:
    """Result of a correlation analysis between two metrics"""
    metric_1_id: int
    metric_1_name: str
    metric_2_id: int
    metric_2_name: str
    coefficient: float
    p_value: float
    lag: int
    strength: str  # 'weak', 'moderate', 'strong'
    significant: bool
    direction: str  # 'positive', 'negative', 'none'
    sample_size: int
    algorithm: str  # 'pearson', 'spearman', 'kendall'


class CorrelationEngine:
    """Correlation analysis engine"""

    def __init__(self, min_significance: float = 0.05, min_sample_size: int = 7):
        """
        Initialize correlation engine

        Args:
            min_significance: P-value threshold for significance (default 0.05)
            min_sample_size: Minimum number of data points required (default 7)
        """
        self.min_significance = min_significance
        self.min_sample_size = min_sample_size

    def calculate_correlation(
        self,
        x: List[float],
        y: List[float],
        algorithm: str = 'pearson'
    ) -> Tuple[float, float]:
        """
        Calculate correlation coefficient and p-value

        Args:
            x: First variable data
            y: Second variable data
            algorithm: 'pearson', 'spearman', or 'kendall'

        Returns:
            Tuple of (coefficient, p_value)
        """
        if len(x) < self.min_sample_size or len(y) < self.min_sample_size:
            raise ValueError(f"Insufficient data points (min {self.min_sample_size} required)")

        if len(x) != len(y):
            raise ValueError("Data arrays must have the same length")

        # Remove NaN pairs
        mask = ~(np.isnan(x) | np.isnan(y))
        x_clean = np.array(x)[mask]
        y_clean = np.array(y)[mask]

        if len(x_clean) < self.min_sample_size:
            raise ValueError(f"Insufficient valid data points after cleaning (min {self.min_sample_size} required)")

        if algorithm == 'pearson':
            coefficient, p_value = stats.pearsonr(x_clean, y_clean)
        elif algorithm == 'spearman':
            coefficient, p_value = stats.spearmanr(x_clean, y_clean)
        elif algorithm == 'kendall':
            coefficient, p_value = stats.kendalltau(x_clean, y_clean)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        return float(coefficient), float(p_value)

    def calculate_lag_correlation(
        self,
        x: List[float],
        y: List[float],
        max_lag: int = 7,
        algorithm: str = 'pearson'
    ) -> Tuple[float, float, int]:
        """
        Calculate correlation with time lags (delayed effects)

        Args:
            x: First variable data (predictor)
            y: Second variable data (outcome)
            max_lag: Maximum lag in days to test
            algorithm: Correlation algorithm to use

        Returns:
            Tuple of (best_coefficient, best_p_value, best_lag)
        """
        best_correlation = 0.0
        best_p_value = 1.0
        best_lag = 0

        # Test lag 0 (no delay)
        try:
            coef, p_val = self.calculate_correlation(x, y, algorithm)
            if abs(coef) > abs(best_correlation):
                best_correlation = coef
                best_p_value = p_val
                best_lag = 0
        except ValueError:
            pass

        # Test positive lags (x predicts future y)
        for lag in range(1, max_lag + 1):
            if lag >= len(x):
                break

            # Shift y forward by lag days
            x_lagged = x[:-lag]
            y_lagged = y[lag:]

            try:
                coef, p_val = self.calculate_correlation(x_lagged, y_lagged, algorithm)
                if abs(coef) > abs(best_correlation):
                    best_correlation = coef
                    best_p_value = p_val
                    best_lag = lag
            except ValueError:
                continue

        return best_correlation, best_p_value, best_lag

    def classify_strength(self, coefficient: float) -> str:
        """
        Classify correlation strength

        Args:
            coefficient: Correlation coefficient

        Returns:
            'weak', 'moderate', or 'strong'
        """
        abs_coef = abs(coefficient)
        if abs_coef < 0.3:
            return 'weak'
        elif abs_coef < 0.7:
            return 'moderate'
        else:
            return 'strong'

    def classify_direction(self, coefficient: float) -> str:
        """
        Classify correlation direction

        Args:
            coefficient: Correlation coefficient

        Returns:
            'positive', 'negative', or 'none'
        """
        if abs(coefficient) < 0.1:
            return 'none'
        return 'positive' if coefficient > 0 else 'negative'

    def analyze_metric_pair(
        self,
        metric_1_id: int,
        metric_1_name: str,
        metric_1_data: List[float],
        metric_2_id: int,
        metric_2_name: str,
        metric_2_data: List[float],
        algorithm: str = 'pearson',
        max_lag: int = 7
    ) -> Optional[CorrelationResult]:
        """
        Analyze correlation between two metrics

        Args:
            metric_1_id: ID of first metric
            metric_1_name: Name of first metric
            metric_1_data: Data for first metric
            metric_2_id: ID of second metric
            metric_2_name: Name of second metric
            metric_2_data: Data for second metric
            algorithm: Correlation algorithm
            max_lag: Maximum lag to test

        Returns:
            CorrelationResult if analysis succeeds, None otherwise
        """
        try:
            coefficient, p_value, lag = self.calculate_lag_correlation(
                metric_1_data,
                metric_2_data,
                max_lag=max_lag,
                algorithm=algorithm
            )

            # Count valid samples
            mask = ~(np.isnan(metric_1_data) | np.isnan(metric_2_data))
            sample_size = int(np.sum(mask))

            return CorrelationResult(
                metric_1_id=metric_1_id,
                metric_1_name=metric_1_name,
                metric_2_id=metric_2_id,
                metric_2_name=metric_2_name,
                coefficient=coefficient,
                p_value=p_value,
                lag=lag,
                strength=self.classify_strength(coefficient),
                significant=p_value < self.min_significance,
                direction=self.classify_direction(coefficient),
                sample_size=sample_size,
                algorithm=algorithm
            )
        except ValueError:
            return None

    def analyze_all_pairs(
        self,
        metrics_data: Dict[int, Dict[str, any]],
        algorithm: str = 'pearson',
        max_lag: int = 7,
        only_significant: bool = False
    ) -> List[CorrelationResult]:
        """
        Analyze correlations between all metric pairs

        Args:
            metrics_data: Dict mapping metric_id to {name, data}
            algorithm: Correlation algorithm
            max_lag: Maximum lag to test
            only_significant: Only return significant results

        Returns:
            List of CorrelationResult objects
        """
        results = []
        metric_ids = list(metrics_data.keys())

        # Analyze all unique pairs
        for i, id1 in enumerate(metric_ids):
            for id2 in metric_ids[i + 1:]:
                result = self.analyze_metric_pair(
                    metric_1_id=id1,
                    metric_1_name=metrics_data[id1]['name'],
                    metric_1_data=metrics_data[id1]['data'],
                    metric_2_id=id2,
                    metric_2_name=metrics_data[id2]['name'],
                    metric_2_data=metrics_data[id2]['data'],
                    algorithm=algorithm,
                    max_lag=max_lag
                )

                if result:
                    if only_significant and not result.significant:
                        continue
                    results.append(result)

        # Sort by absolute coefficient (strongest first)
        results.sort(key=lambda r: abs(r.coefficient), reverse=True)

        return results


def prepare_metric_data(
    entries: List[Dict],
    metric_id: int,
    value_type: str
) -> List[float]:
    """
    Prepare metric data from entries for correlation analysis

    Args:
        entries: List of entry dictionaries with values
        metric_id: ID of metric to extract
        value_type: Type of metric ('boolean', 'numeric', etc.)

    Returns:
        List of values (with NaN for missing data)
    """
    data = []

    for entry in entries:
        value_found = False

        for value in entry.get('values', []):
            if value.get('metric_id') == metric_id:
                if value_type == 'boolean':
                    data.append(1.0 if value.get('value_boolean') else 0.0)
                else:
                    numeric_val = value.get('value_numeric')
                    data.append(float(numeric_val) if numeric_val is not None else np.nan)
                value_found = True
                break

        if not value_found:
            data.append(np.nan)

    return data
