"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.utils.database import get_db
from app.schemas import UserRegister, UserLogin, AuthResponse, UserResponse, TokenResponse
from app.services import UserService
from app.security import create_access_token, create_refresh_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user account.

    Args:
        user_data: User registration data (email, password, language, timezone)
        db: Database session

    Returns:
        User object and authentication tokens

    Raises:
        400: If email already exists
    """
    # Create user
    user = UserService.create_user(db, user_data)

    # Generate tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return AuthResponse(
        user=UserResponse.from_orm(user),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    )


@router.post("/login", response_model=AuthResponse)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password.

    Args:
        credentials: Email and password
        db: Database session

    Returns:
        User object and authentication tokens

    Raises:
        401: If credentials are invalid
    """
    # Authenticate user
    user = UserService.authenticate_user(
        db,
        credentials.email,
        credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Generate tokens
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return AuthResponse(
        user=UserResponse.from_orm(user),
        tokens=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.

    Args:
        refresh_token: Valid refresh token
        db: Database session

    Returns:
        New authentication tokens

    Raises:
        401: If refresh token is invalid
    """
    from app.security import verify_token

    # Verify refresh token
    payload = verify_token(refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user_id = payload.get("sub")
    user = UserService.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    # Generate new tokens
    new_access_token = create_access_token(data={"sub": user.id})
    new_refresh_token = create_refresh_token(data={"sub": user.id})

    return TokenResponse(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )
