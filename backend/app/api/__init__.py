"""
API routers
"""
from .auth import router as auth_router
from .users import router as users_router
from .metrics import router as metrics_router
from .entries import router as entries_router
from .analytics import router as analytics_router
from .demo_data import router as demo_data_router

__all__ = [
    "auth_router",
    "users_router",
    "metrics_router",
    "entries_router",
    "analytics_router",
    "demo_data_router",
]
