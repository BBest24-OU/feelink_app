"""
Unit tests for entries API endpoints
"""
import pytest
from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.user import User


class TestEntriesAPI:
    """Tests for entries API endpoints"""

    def test_list_entries_empty(self, client: TestClient, auth_headers: dict):
        """Test listing entries when none exist"""
        response = client.get("/api/v1/entries", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "entries" in data
        assert len(data["entries"]) == 0

    def test_list_entries_with_data(self, client: TestClient, auth_headers: dict, test_entries: list):
        """Test listing entries with existing data"""
        response = client.get("/api/v1/entries", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "entries" in data
        assert len(data["entries"]) == 10

        # Check entry structure
        entry = data["entries"][0]
        assert "id" in entry
        assert "entry_date" in entry
        assert "values" in entry
        assert "notes" in entry

    def test_list_entries_with_date_range(self, client: TestClient, auth_headers: dict, test_entries: list):
        """Test listing entries with date range filter"""
        today = datetime.utcnow().date()
        date_from = (today - timedelta(days=5)).isoformat()
        date_to = today.isoformat()

        response = client.get(
            f"/api/v1/entries?date_from={date_from}&date_to={date_to}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        entries = data["entries"]

        # Should have 6 entries (today + 5 days back)
        assert len(entries) == 6

        # All entries should be within range
        for entry in entries:
            entry_date = datetime.fromisoformat(entry["entry_date"]).date()
            assert datetime.fromisoformat(date_from).date() <= entry_date <= datetime.fromisoformat(date_to).date()

    def test_list_entries_unauthorized(self, client: TestClient):
        """Test listing entries without authentication"""
        response = client.get("/api/v1/entries")

        assert response.status_code == 401

    def test_create_entry_success(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test creating a new entry"""
        entry_data = {
            "entry_date": datetime.utcnow().date().isoformat(),
            "notes": "Test entry",
            "values": [
                {
                    "metric_id": test_metrics[0].id,
                    "value_numeric": 8.0
                },
                {
                    "metric_id": test_metrics[1].id,
                    "value_numeric": 7.5
                }
            ]
        }

        response = client.post("/api/v1/entries", json=entry_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["entry_date"] == entry_data["entry_date"]
        assert data["notes"] == "Test entry"
        assert len(data["values"]) == 2
        assert "id" in data

    def test_create_entry_with_boolean_value(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test creating entry with boolean metric value"""
        entry_data = {
            "entry_date": datetime.utcnow().date().isoformat(),
            "values": [
                {
                    "metric_id": test_metrics[2].id,  # Boolean metric
                    "value_boolean": True
                }
            ]
        }

        response = client.post("/api/v1/entries", json=entry_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["values"][0]["value_boolean"] is True
        assert data["values"][0]["value_numeric"] is None

    def test_create_entry_without_notes(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test creating entry without notes"""
        entry_data = {
            "entry_date": datetime.utcnow().date().isoformat(),
            "values": [
                {
                    "metric_id": test_metrics[0].id,
                    "value_numeric": 8.0
                }
            ]
        }

        response = client.post("/api/v1/entries", json=entry_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["notes"] is None or data["notes"] == ""

    def test_create_entry_duplicate_date(self, client: TestClient, auth_headers: dict,
                                        test_metrics: list, test_entries: list):
        """Test creating entry for date that already exists"""
        existing_date = test_entries[0].entry_date.isoformat()

        entry_data = {
            "entry_date": existing_date,
            "values": [
                {
                    "metric_id": test_metrics[0].id,
                    "value_numeric": 8.0
                }
            ]
        }

        response = client.post("/api/v1/entries", json=entry_data, headers=auth_headers)

        # Should return error (constraint violation)
        assert response.status_code == 400

    def test_create_entry_invalid_metric(self, client: TestClient, auth_headers: dict):
        """Test creating entry with non-existent metric"""
        entry_data = {
            "entry_date": datetime.utcnow().date().isoformat(),
            "values": [
                {
                    "metric_id": 99999,
                    "value_numeric": 8.0
                }
            ]
        }

        response = client.post("/api/v1/entries", json=entry_data, headers=auth_headers)

        assert response.status_code == 400

    def test_create_entry_unauthorized(self, client: TestClient, test_metrics: list):
        """Test creating entry without authentication"""
        entry_data = {
            "entry_date": datetime.utcnow().date().isoformat(),
            "values": [
                {
                    "metric_id": test_metrics[0].id,
                    "value_numeric": 8.0
                }
            ]
        }

        response = client.post("/api/v1/entries", json=entry_data)

        assert response.status_code == 401

    def test_get_entry_success(self, client: TestClient, auth_headers: dict, test_entries: list):
        """Test getting a specific entry"""
        entry_id = test_entries[0].id

        response = client.get(f"/api/v1/entries/{entry_id}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == entry_id
        assert "values" in data
        assert len(data["values"]) > 0

    def test_get_entry_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting non-existent entry"""
        response = client.get("/api/v1/entries/99999", headers=auth_headers)

        assert response.status_code == 404

    def test_get_entry_unauthorized(self, client: TestClient, test_entries: list):
        """Test getting entry without authentication"""
        entry_id = test_entries[0].id

        response = client.get(f"/api/v1/entries/{entry_id}")

        assert response.status_code == 401

    def test_update_entry_success(self, client: TestClient, auth_headers: dict,
                                  test_entries: list, test_metrics: list):
        """Test updating an entry"""
        entry_id = test_entries[0].id

        update_data = {
            "notes": "Updated notes",
            "values": [
                {
                    "metric_id": test_metrics[0].id,
                    "value_numeric": 9.0
                }
            ]
        }

        response = client.put(f"/api/v1/entries/{entry_id}", json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == entry_id
        assert data["notes"] == "Updated notes"

    def test_update_entry_not_found(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test updating non-existent entry"""
        update_data = {
            "notes": "Test",
            "values": [
                {
                    "metric_id": test_metrics[0].id,
                    "value_numeric": 9.0
                }
            ]
        }

        response = client.put("/api/v1/entries/99999", json=update_data, headers=auth_headers)

        assert response.status_code == 404

    def test_update_entry_unauthorized(self, client: TestClient, test_entries: list, test_metrics: list):
        """Test updating entry without authentication"""
        entry_id = test_entries[0].id
        update_data = {
            "values": [
                {
                    "metric_id": test_metrics[0].id,
                    "value_numeric": 9.0
                }
            ]
        }

        response = client.put(f"/api/v1/entries/{entry_id}", json=update_data)

        assert response.status_code == 401

    def test_delete_entry_success(self, client: TestClient, auth_headers: dict, test_entries: list):
        """Test deleting an entry"""
        entry_id = test_entries[0].id

        response = client.delete(f"/api/v1/entries/{entry_id}", headers=auth_headers)

        assert response.status_code == 204

        # Verify it's deleted
        response = client.get(f"/api/v1/entries/{entry_id}", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_entry_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting non-existent entry"""
        response = client.delete("/api/v1/entries/99999", headers=auth_headers)

        assert response.status_code == 404

    def test_delete_entry_unauthorized(self, client: TestClient, test_entries: list):
        """Test deleting entry without authentication"""
        entry_id = test_entries[0].id

        response = client.delete(f"/api/v1/entries/{entry_id}")

        assert response.status_code == 401

    def test_user_can_only_see_own_entries(self, client: TestClient, test_db: Session,
                                           auth_headers: dict, test_entries: list, test_metrics: list):
        """Test that users can only see their own entries"""
        # Create another user with entry
        from app.security.password import hash_password
        from app.models.entry import Entry

        other_user = User(
            email="other@example.com",
            password_hash=hash_password("password"),
            language="en",
            timezone="UTC"
        )
        test_db.add(other_user)
        test_db.commit()
        test_db.refresh(other_user)

        other_entry = Entry(
            user_id=other_user.id,
            entry_date=datetime.utcnow().date(),
            notes="Other user entry"
        )
        test_db.add(other_entry)
        test_db.commit()

        # Test user should not see other user's entries
        response = client.get("/api/v1/entries", headers=auth_headers)

        assert response.status_code == 200
        entries = response.json()["entries"]
        entry_ids = [e["id"] for e in entries]
        assert other_entry.id not in entry_ids

    def test_get_entry_by_date_success(self, client: TestClient, auth_headers: dict, test_entries: list):
        """Test getting entry by specific date"""
        target_date = test_entries[0].entry_date.isoformat()

        response = client.get(f"/api/v1/entries/by-date/{target_date}", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["entry_date"] == target_date

    def test_get_entry_by_date_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting entry by date when none exists"""
        future_date = (datetime.utcnow().date() + timedelta(days=365)).isoformat()

        response = client.get(f"/api/v1/entries/by-date/{future_date}", headers=auth_headers)

        assert response.status_code == 404

    def test_entry_values_validation(self, client: TestClient, auth_headers: dict, test_metrics: list):
        """Test that entry values are validated against metric constraints"""
        # Try to create entry with value outside metric's min/max range
        entry_data = {
            "entry_date": datetime.utcnow().date().isoformat(),
            "values": [
                {
                    "metric_id": test_metrics[0].id,
                    "value_numeric": 100.0  # Exceeds max_value of 24
                }
            ]
        }

        response = client.post("/api/v1/entries", json=entry_data, headers=auth_headers)

        # Should return validation error
        assert response.status_code == 400
