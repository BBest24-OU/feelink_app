"""
Analytics API schemas
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class CorrelationRequest(BaseModel):
    """Request schema for correlation analysis"""
    metric_ids: Optional[List[int]] = Field(
        None,
        description="List of metric IDs to analyze (default: all)"
    )
    date_from: Optional[date] = Field(
        None,
        description="Start date for analysis"
    )
    date_to: Optional[date] = Field(
        None,
        description="End date for analysis"
    )
    algorithm: str = Field(
        'pearson',
        description="Correlation algorithm: pearson, spearman, or kendall"
    )
    max_lag: int = Field(
        7,
        description="Maximum lag in days for lag correlation"
    )
    min_significance: float = Field(
        0.05,
        description="P-value threshold for significance"
    )
    only_significant: bool = Field(
        False,
        description="Return only statistically significant correlations"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "metric_ids": [1, 2, 3],
                "date_from": "2024-01-01",
                "date_to": "2024-12-31",
                "algorithm": "pearson",
                "max_lag": 7,
                "min_significance": 0.05,
                "only_significant": True
            }
        }


class CorrelationResultSchema(BaseModel):
    """Single correlation result"""
    metric_1_id: int
    metric_1_name: str
    metric_2_id: int
    metric_2_name: str
    coefficient: float = Field(description="Correlation coefficient (-1 to 1)")
    p_value: float = Field(description="Statistical significance (p-value)")
    lag: int = Field(description="Time lag in days (0 = no delay)")
    strength: str = Field(description="Correlation strength: weak, moderate, strong")
    significant: bool = Field(description="Is statistically significant")
    direction: str = Field(description="Correlation direction: positive, negative, none")
    sample_size: int = Field(description="Number of data points used")
    algorithm: str = Field(description="Algorithm used: pearson, spearman, kendall")

    class Config:
        json_schema_extra = {
            "example": {
                "metric_1_id": 1,
                "metric_1_name": "Sleep Hours",
                "metric_2_id": 3,
                "metric_2_name": "Mood",
                "coefficient": 0.73,
                "p_value": 0.002,
                "lag": 0,
                "strength": "strong",
                "significant": True,
                "direction": "positive",
                "sample_size": 45,
                "algorithm": "pearson"
            }
        }


class CorrelationResponse(BaseModel):
    """Response schema for correlation analysis"""
    correlations: List[CorrelationResultSchema]
    algorithm_used: str
    date_range: dict
    total_correlations: int

    class Config:
        json_schema_extra = {
            "example": {
                "correlations": [
                    {
                        "metric_1_id": 1,
                        "metric_1_name": "Sleep Hours",
                        "metric_2_id": 3,
                        "metric_2_name": "Mood",
                        "coefficient": 0.73,
                        "p_value": 0.002,
                        "lag": 0,
                        "strength": "strong",
                        "significant": True,
                        "direction": "positive",
                        "sample_size": 45,
                        "algorithm": "pearson"
                    }
                ],
                "algorithm_used": "pearson",
                "date_range": {
                    "from": "2024-01-01",
                    "to": "2024-12-31"
                },
                "total_correlations": 1
            }
        }


class MetricStatistics(BaseModel):
    """Statistics for a single metric"""
    metric_id: int
    metric_name: str
    count: int
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float


class StatisticsResponse(BaseModel):
    """Response schema for statistics endpoint"""
    statistics: List[MetricStatistics]
    date_range: dict

    class Config:
        json_schema_extra = {
            "example": {
                "statistics": [
                    {
                        "metric_id": 1,
                        "metric_name": "Sleep Hours",
                        "count": 30,
                        "mean": 7.5,
                        "median": 7.0,
                        "std_dev": 1.2,
                        "min_value": 5.0,
                        "max_value": 9.5
                    }
                ],
                "date_range": {
                    "from": "2024-01-01",
                    "to": "2024-12-31"
                }
            }
        }
