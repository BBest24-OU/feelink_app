"""
User Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    language: str = Field(default="en", pattern="^(en|pl)$")
    timezone: str = Field(default="UTC")


class UserRegister(UserBase):
    """Schema for user registration"""
    password: str = Field(min_length=8, max_length=128)

    @validator('password')
    def validate_password(cls, v):
        """Validate password strength"""
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v

    @validator('email')
    def validate_email_lowercase(cls, v):
        """Ensure email is lowercase"""
        return v.lower()


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

    @validator('email')
    def validate_email_lowercase(cls, v):
        """Ensure email is lowercase"""
        return v.lower()


class RefreshTokenRequest(BaseModel):
    """Schema for refresh token request"""
    refresh_token: str


class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    name: Optional[str] = Field(None, max_length=100)
    language: Optional[str] = Field(None, pattern="^(en|pl)$")
    timezone: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    id: int
    email: str
    name: Optional[str] = None
    language: str
    timezone: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for authentication token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 86400  # 24 hours in seconds


class AuthResponse(BaseModel):
    """Schema for complete authentication response"""
    user: UserResponse
    tokens: TokenResponse
