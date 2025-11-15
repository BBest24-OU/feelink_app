"""
Metric Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from decimal import Decimal


class MetricBase(BaseModel):
    """Base metric schema"""
    name_key: str = Field(min_length=1, max_length=100, pattern="^[a-z0-9_.]+$")
    category: str = Field(
        ...,
        pattern="^(physical|psychological|triggers|medications|selfcare|wellness|notes)$"
    )
    value_type: str = Field(
        ...,
        pattern="^(range|number|boolean|count|text)$"
    )
    min_value: Optional[Decimal] = None
    max_value: Optional[Decimal] = None
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)

    @validator('max_value')
    def validate_range(cls, v, values):
        """Validate that max_value > min_value for range type"""
        if values.get('value_type') == 'range':
            if v is None or values.get('min_value') is None:
                raise ValueError('min_value and max_value are required for range type')
            if v <= values.get('min_value'):
                raise ValueError('max_value must be greater than min_value')
        return v


class MetricCreate(MetricBase):
    """Schema for creating a new metric"""
    pass


class MetricUpdate(BaseModel):
    """Schema for updating a metric"""
    name_key: Optional[str] = Field(None, min_length=1, max_length=100, pattern="^[a-z0-9_.]+$")
    category: Optional[str] = Field(
        None,
        pattern="^(physical|psychological|triggers|medications|selfcare|wellness|notes)$"
    )
    description: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    icon: Optional[str] = Field(None, max_length=50)
    display_order: Optional[int] = None
    archived: Optional[bool] = None


class MetricResponse(BaseModel):
    """Schema for metric response"""
    id: int
    user_id: int
    name_key: str
    category: str
    value_type: str
    min_value: Optional[Decimal]
    max_value: Optional[Decimal]
    description: Optional[str]
    color: Optional[str]
    icon: Optional[str]
    display_order: int
    archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MetricListResponse(BaseModel):
    """Schema for list of metrics response"""
    metrics: list[MetricResponse]
    total: int
