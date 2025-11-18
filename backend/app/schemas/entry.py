"""
Entry Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, validator
from datetime import date, datetime
from typing import Optional, Union
from decimal import Decimal


class EntryValueBase(BaseModel):
    """Base entry value schema"""
    metric_id: int
    value: Union[Decimal, bool, str]


class EntryValueCreate(EntryValueBase):
    """Schema for creating an entry value"""
    pass


class EntryValueResponse(BaseModel):
    """Schema for entry value response"""
    id: int
    entry_id: int
    metric_id: int
    value_numeric: Optional[Decimal]
    value_boolean: Optional[bool]
    value_text: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class EntryBase(BaseModel):
    """Base entry schema"""
    entry_date: date
    notes: Optional[str] = None

    @validator('entry_date')
    def validate_date_not_future(cls, v):
        """Ensure entry date is not in the future"""
        if v > date.today():
            raise ValueError('Entry date cannot be in the future')
        return v


class EntryCreate(EntryBase):
    """Schema for creating a new entry"""
    values: list[EntryValueCreate] = Field(min_length=1)


class EntryUpdate(BaseModel):
    """Schema for updating an entry"""
    notes: Optional[str] = None
    values: Optional[list[EntryValueCreate]] = None


class EntryResponse(BaseModel):
    """Schema for entry response"""
    id: int
    user_id: int
    entry_date: date
    notes: Optional[str]
    values: list[EntryValueResponse]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EntryListResponse(BaseModel):
    """Schema for list of entries response"""
    entries: list[EntryResponse]
    total: int
    has_more: bool
