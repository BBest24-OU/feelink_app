"""
Unit tests for metrics API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.metric import Metric


class TestMetricsAPI:
    """Tests for metrics API endpoints"""

    def test_list_metrics_empty(self, client: TestClient, auth_headers: dict):
        """Test listing metrics when none exist"""
        response = client.get("/api/v1/metrics", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert len(data["metrics"]) == 0

    def test_list_metrics_with_data(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test listing metrics with existing data"""
        response = client.get("/api/v1/metrics", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "metrics" in data
        assert len(data["metrics"]) == 3

        # Check metric structure
        metric = data["metrics"][0]
        assert "id" in metric
        assert "name_key" in metric
        assert "category" in metric
        assert "value_type" in metric

    def test_list_metrics_include_archived(self, client: TestClient, auth_headers: dict,
                                           test_db: Session, test_user: User):
        """Test listing metrics including archived ones"""
        # Create archived metric
        archived_metric = Metric(
            user_id=test_user.id,
            name_key="metric.archived",
            category="mental",
            value_type="numeric",
            archived=True
        )
        test_db.add(archived_metric)
        test_db.commit()

        # Without includeArchived
        response = client.get("/api/v1/metrics", headers=auth_headers)
        assert response.status_code == 200
        active_count = len(response.json()["metrics"])

        # With includeArchived
        response = client.get("/api/v1/metrics?includeArchived=true", headers=auth_headers)
        assert response.status_code == 200
        all_count = len(response.json()["metrics"])

        assert all_count > active_count

    def test_list_metrics_unauthorized(self, client: TestClient):
        """Test listing metrics without authentication"""
        response = client.get("/api/v1/metrics")

        assert response.status_code == 401

    def test_create_metric_success(self, client: TestClient, auth_headers: dict):
        """Test creating a new metric"""
        metric_data = {
            "name_key": "metric.new_metric",
            "category": "mental",
            "value_type": "numeric",
            "unit": "scale",
            "min_value": 1,
            "max_value": 10
        }

        response = client.post("/api/v1/metrics", json=metric_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["name_key"] == "metric.new_metric"
        assert data["category"] == "mental"
        assert data["value_type"] == "numeric"
        assert "id" in data

    def test_create_metric_boolean_type(self, client: TestClient, auth_headers: dict):
        """Test creating a boolean metric"""
        metric_data = {
            "name_key": "metric.did_exercise",
            "category": "physical",
            "value_type": "boolean"
        }

        response = client.post("/api/v1/metrics", json=metric_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["value_type"] == "boolean"
        assert data.get("unit") is None
        assert data.get("min_value") is None
        assert data.get("max_value") is None

    def test_create_metric_invalid_category(self, client: TestClient, auth_headers: dict):
        """Test creating metric with invalid category"""
        metric_data = {
            "name_key": "metric.test",
            "category": "invalid_category",
            "value_type": "numeric"
        }

        response = client.post("/api/v1/metrics", json=metric_data, headers=auth_headers)

        assert response.status_code == 422  # Validation error

    def test_create_metric_invalid_value_type(self, client: TestClient, auth_headers: dict):
        """Test creating metric with invalid value_type"""
        metric_data = {
            "name_key": "metric.test",
            "category": "mental",
            "value_type": "invalid_type"
        }

        response = client.post("/api/v1/metrics", json=metric_data, headers=auth_headers)

        assert response.status_code == 422  # Validation error

    def test_create_metric_unauthorized(self, client: TestClient):
        """Test creating metric without authentication"""
        metric_data = {
            "name_key": "metric.test",
            "category": "mental",
            "value_type": "numeric"
        }

        response = client.post("/api/v1/metrics", json=metric_data)

        assert response.status_code == 401

    def test_get_metric_success(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test getting a specific metric"""
        metric_id = test_metrics[0].id

        response = client.get(f"/api/v1/metrics/{metric_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == metric_id
        assert data["name_key"] == test_metrics[0].name_key

    def test_get_metric_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting non-existent metric"""
        response = client.get("/api/v1/metrics/99999", headers=auth_headers)

        assert response.status_code == 404

    def test_get_metric_unauthorized(self, client: TestClient, test_metrics: list):
        """Test getting metric without authentication"""
        metric_id = test_metrics[0].id

        response = client.get(f"/api/v1/metrics/{metric_id}")

        assert response.status_code == 401

    def test_update_metric_success(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test updating a metric"""
        metric_id = test_metrics[0].id
        update_data = {
            "name_key": "metric.updated_name",
            "unit": "updated_unit"
        }

        response = client.put(f"/api/v1/metrics/{metric_id}", json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == metric_id
        assert data["name_key"] == "metric.updated_name"
        assert data["unit"] == "updated_unit"

    def test_update_metric_not_found(self, client: TestClient, auth_headers: dict):
        """Test updating non-existent metric"""
        update_data = {
            "name_key": "metric.test"
        }

        response = client.put("/api/v1/metrics/99999", json=update_data, headers=auth_headers)

        assert response.status_code == 404

    def test_update_metric_unauthorized(self, client: TestClient, test_metrics: list):
        """Test updating metric without authentication"""
        metric_id = test_metrics[0].id
        update_data = {"name_key": "metric.test"}

        response = client.put(f"/api/v1/metrics/{metric_id}", json=update_data)

        assert response.status_code == 401

    def test_archive_metric_success(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test archiving a metric"""
        metric_id = test_metrics[0].id

        response = client.delete(f"/api/v1/metrics/{metric_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["archived"] is True

        # Verify it's not in active list
        response = client.get("/api/v1/metrics", headers=auth_headers)
        active_metrics = response.json()["metrics"]
        active_ids = [m["id"] for m in active_metrics]
        assert metric_id not in active_ids

    def test_archive_metric_not_found(self, client: TestClient, auth_headers: dict):
        """Test archiving non-existent metric"""
        response = client.delete("/api/v1/metrics/99999", headers=auth_headers)

        assert response.status_code == 404

    def test_archive_metric_unauthorized(self, client: TestClient, test_metrics: list):
        """Test archiving metric without authentication"""
        metric_id = test_metrics[0].id

        response = client.delete(f"/api/v1/metrics/{metric_id}")

        assert response.status_code == 401

    def test_user_can_only_see_own_metrics(self, client: TestClient, test_db: Session,
                                           auth_headers: dict, test_metrics: list):
        """Test that users can only see their own metrics"""
        # Create another user with metrics
        from app.security.password import hash_password
        from app.security.jwt import create_access_token

        other_user = User(
            email="other@example.com",
            password_hash=hash_password("password"),
            language="en",
            timezone="UTC"
        )
        test_db.add(other_user)
        test_db.commit()
        test_db.refresh(other_user)

        other_metric = Metric(
            user_id=other_user.id,
            name_key="metric.other_user",
            category="mental",
            value_type="numeric"
        )
        test_db.add(other_metric)
        test_db.commit()

        # Test user should not see other user's metrics
        response = client.get("/api/v1/metrics", headers=auth_headers)

        assert response.status_code == 200
        metrics = response.json()["metrics"]
        metric_ids = [m["id"] for m in metrics]
        assert other_metric.id not in metric_ids

    def test_reorder_metrics_success(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test reordering metrics"""
        metric_ids = [m.id for m in test_metrics]
        # Reverse the order
        reorder_data = {
            "metric_ids": list(reversed(metric_ids))
        }

        response = client.post("/api/v1/metrics/reorder", json=reorder_data, headers=auth_headers)

        assert response.status_code == 200

        # Verify new order
        response = client.get("/api/v1/metrics", headers=auth_headers)
        metrics = response.json()["metrics"]

        # Should be in new order
        assert metrics[0]["id"] == metric_ids[2]
        assert metrics[1]["id"] == metric_ids[1]
        assert metrics[2]["id"] == metric_ids[0]

    def test_metric_display_order_maintained(self, client: TestClient, auth_headers: dict):
        """Test that metrics maintain display order"""
        # Create metrics with specific order
        for i in range(3):
            metric_data = {
                "name_key": f"metric.order_{i}",
                "category": "mental",
                "value_type": "numeric",
                "display_order": i
            }
            client.post("/api/v1/metrics", json=metric_data, headers=auth_headers)

        # Retrieve metrics
        response = client.get("/api/v1/metrics", headers=auth_headers)
        metrics = response.json()["metrics"]

        # Should be ordered by display_order
        for i in range(len(metrics) - 1):
            assert metrics[i]["display_order"] <= metrics[i + 1]["display_order"]
