"""
Pytest configuration and fixtures
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from typing import Generator
import os

from app.models.base import Base
from app.models.user import User
from app.models.metric import Metric
from app.models.entry import Entry
from app.main import app
from app.utils.database import get_db
from app.security.password import hash_password
from app.security.jwt import create_access_token


# Test database URL (using SQLite in-memory for tests)
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "sqlite:///:memory:"
)


@pytest.fixture(scope="function")
def test_db() -> Generator[Session, None, None]:
    """
    Create a test database session.
    Creates all tables before test and drops them after.
    """
    # Create test engine
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in TEST_DATABASE_URL else {}
    )

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database dependency override.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(test_db: Session) -> User:
    """
    Create a test user in the database.
    """
    user = User(
        email="test@example.com",
        password_hash=hash_password("testpassword123"),
        language="en",
        timezone="UTC"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_user_token(test_user: User) -> str:
    """
    Create an access token for the test user.
    """
    return create_access_token(data={"sub": test_user.email, "user_id": test_user.id})


@pytest.fixture(scope="function")
def auth_headers(test_user_token: str) -> dict:
    """
    Create authorization headers with test user token.
    """
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture(scope="function")
def test_metrics(test_db: Session, test_user: User) -> list[Metric]:
    """
    Create test metrics for the test user.
    """
    metrics = [
        Metric(
            user_id=test_user.id,
            name_key="metric.sleep_hours",
            category="physical",
            value_type="numeric",
            unit="hours",
            min_value=0,
            max_value=24,
            display_order=1,
            archived=False
        ),
        Metric(
            user_id=test_user.id,
            name_key="metric.mood",
            category="mental",
            value_type="numeric",
            unit="scale",
            min_value=1,
            max_value=10,
            display_order=2,
            archived=False
        ),
        Metric(
            user_id=test_user.id,
            name_key="metric.exercise",
            category="physical",
            value_type="boolean",
            display_order=3,
            archived=False
        ),
    ]

    for metric in metrics:
        test_db.add(metric)

    test_db.commit()

    for metric in metrics:
        test_db.refresh(metric)

    return metrics


@pytest.fixture(scope="function")
def test_entries(test_db: Session, test_user: User, test_metrics: list[Metric]) -> list[Entry]:
    """
    Create test entries with values for the test user.
    """
    from datetime import datetime, timedelta
    from app.models.entry import EntryValue

    entries = []

    # Create entries for the last 10 days
    for i in range(10):
        entry_date = (datetime.utcnow() - timedelta(days=i)).date()

        entry = Entry(
            user_id=test_user.id,
            entry_date=entry_date,
            notes=f"Test entry {i}"
        )
        test_db.add(entry)
        test_db.flush()

        # Add values for each metric
        for j, metric in enumerate(test_metrics):
            if metric.value_type == "numeric":
                value = EntryValue(
                    entry_id=entry.id,
                    metric_id=metric.id,
                    value_numeric=7.0 + (i % 3)  # Varying values
                )
            else:  # boolean
                value = EntryValue(
                    entry_id=entry.id,
                    metric_id=metric.id,
                    value_boolean=i % 2 == 0
                )
            test_db.add(value)

        entries.append(entry)

    test_db.commit()

    for entry in entries:
        test_db.refresh(entry)

    return entries
