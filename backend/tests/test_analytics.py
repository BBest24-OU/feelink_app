"""
Unit tests for analytics API endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestAnalyticsAPI:
    """Tests for analytics API endpoints"""

    def test_correlations_empty_data(self, client: TestClient, auth_headers: dict):
        """Test correlations with no entries"""
        response = client.post("/api/v1/analytics/correlations", json={}, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "correlations" in data
        assert len(data["correlations"]) == 0

    def test_correlations_with_data(self, client: TestClient, auth_headers: dict,
                                   test_metrics: list, test_entries: list):
        """Test correlations with existing data"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": 0,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "correlations" in data
        assert len(data["correlations"]) >= 0  # May or may not find correlations

        # If correlations found, check structure
        if len(data["correlations"]) > 0:
            corr = data["correlations"][0]
            assert "metric_1_id" in corr
            assert "metric_2_id" in corr
            assert "coefficient" in corr
            assert "p_value" in corr
            assert "lag" in corr
            assert "strength" in corr
            assert "significant" in corr
            assert "direction" in corr
            assert "sample_size" in corr
            assert "algorithm" in corr

    def test_correlations_pearson_algorithm(self, client: TestClient, auth_headers: dict,
                                           test_metrics: list, test_entries: list):
        """Test correlations with Pearson algorithm"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": 0,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check that algorithm is set correctly
        for corr in data["correlations"]:
            assert corr["algorithm"] == "pearson"

    def test_correlations_spearman_algorithm(self, client: TestClient, auth_headers: dict,
                                            test_metrics: list, test_entries: list):
        """Test correlations with Spearman algorithm"""
        request_data = {
            "algorithm": "spearman",
            "max_lag": 0,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check that algorithm is set correctly
        for corr in data["correlations"]:
            assert corr["algorithm"] == "spearman"

    def test_correlations_kendall_algorithm(self, client: TestClient, auth_headers: dict,
                                           test_metrics: list, test_entries: list):
        """Test correlations with Kendall algorithm"""
        request_data = {
            "algorithm": "kendall",
            "max_lag": 0,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check that algorithm is set correctly
        for corr in data["correlations"]:
            assert corr["algorithm"] == "kendall"

    def test_correlations_with_lag(self, client: TestClient, auth_headers: dict,
                                  test_metrics: list, test_entries: list):
        """Test correlations with lag correlation"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": 3,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check that lag is within bounds
        for corr in data["correlations"]:
            assert 0 <= corr["lag"] <= 3

    def test_correlations_only_significant(self, client: TestClient, auth_headers: dict,
                                          test_metrics: list, test_entries: list):
        """Test correlations with only_significant filter"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": 0,
            "only_significant": True
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # All returned correlations should be significant
        for corr in data["correlations"]:
            assert corr["significant"] is True

    def test_correlations_with_date_range(self, client: TestClient, auth_headers: dict,
                                         test_metrics: list, test_entries: list):
        """Test correlations with date range filter"""
        from datetime import datetime, timedelta

        today = datetime.utcnow().date()
        date_from = (today - timedelta(days=5)).isoformat()
        date_to = today.isoformat()

        request_data = {
            "algorithm": "pearson",
            "max_lag": 0,
            "date_from": date_from,
            "date_to": date_to,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "correlations" in data

    def test_correlations_with_specific_metrics(self, client: TestClient, auth_headers: dict,
                                               test_metrics: list, test_entries: list):
        """Test correlations with specific metric IDs"""
        metric_ids = [test_metrics[0].id, test_metrics[1].id]

        request_data = {
            "algorithm": "pearson",
            "max_lag": 0,
            "metric_ids": metric_ids,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # All correlations should involve only the specified metrics
        for corr in data["correlations"]:
            assert corr["metric_1_id"] in metric_ids
            assert corr["metric_2_id"] in metric_ids

    def test_correlations_invalid_algorithm(self, client: TestClient, auth_headers: dict):
        """Test correlations with invalid algorithm"""
        request_data = {
            "algorithm": "invalid_algo",
            "max_lag": 0
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        # Should return validation error
        assert response.status_code == 422

    def test_correlations_negative_max_lag(self, client: TestClient, auth_headers: dict):
        """Test correlations with negative max_lag"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": -5
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        # Should return validation error
        assert response.status_code == 422

    def test_correlations_unauthorized(self, client: TestClient):
        """Test correlations without authentication"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": 0
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data)

        assert response.status_code == 401

    def test_statistics_empty_data(self, client: TestClient, auth_headers: dict):
        """Test statistics with no entries"""
        response = client.get("/api/v1/analytics/statistics", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "statistics" in data

    def test_statistics_with_data(self, client: TestClient, auth_headers: dict,
                                 test_metrics: list, test_entries: list):
        """Test statistics with existing data"""
        response = client.get("/api/v1/analytics/statistics", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "statistics" in data

        # If statistics found, check structure
        if len(data["statistics"]) > 0:
            stat = data["statistics"][0]
            assert "metric_id" in stat
            assert "metric_name" in stat
            assert "count" in stat
            assert "mean" in stat or "mode" in stat  # numeric has mean, boolean has mode

    def test_statistics_with_specific_metrics(self, client: TestClient, auth_headers: dict,
                                             test_metrics: list, test_entries: list):
        """Test statistics with specific metric IDs"""
        metric_ids = f"{test_metrics[0].id},{test_metrics[1].id}"

        response = client.get(f"/api/v1/analytics/statistics?metric_ids={metric_ids}",
                            headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "statistics" in data

        # Should only return stats for specified metrics
        returned_metric_ids = [stat["metric_id"] for stat in data["statistics"]]
        for mid in returned_metric_ids:
            assert mid in [test_metrics[0].id, test_metrics[1].id]

    def test_statistics_with_date_range(self, client: TestClient, auth_headers: dict,
                                       test_metrics: list, test_entries: list):
        """Test statistics with date range filter"""
        from datetime import datetime, timedelta

        today = datetime.utcnow().date()
        date_from = (today - timedelta(days=5)).isoformat()
        date_to = today.isoformat()

        response = client.get(
            f"/api/v1/analytics/statistics?date_from={date_from}&date_to={date_to}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "statistics" in data

    def test_statistics_unauthorized(self, client: TestClient):
        """Test statistics without authentication"""
        response = client.get("/api/v1/analytics/statistics")

        assert response.status_code == 401

    def test_correlation_strength_classification(self, client: TestClient, auth_headers: dict,
                                                 test_metrics: list, test_entries: list):
        """Test that correlation strength is correctly classified"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": 0,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check that strength is one of the valid values
        valid_strengths = ["weak", "moderate", "strong"]
        for corr in data["correlations"]:
            assert corr["strength"] in valid_strengths

    def test_correlation_direction_classification(self, client: TestClient, auth_headers: dict,
                                                  test_metrics: list, test_entries: list):
        """Test that correlation direction is correctly classified"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": 0,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check that direction is one of the valid values
        valid_directions = ["positive", "negative", "none"]
        for corr in data["correlations"]:
            assert corr["direction"] in valid_directions

    def test_correlation_coefficient_bounds(self, client: TestClient, auth_headers: dict,
                                           test_metrics: list, test_entries: list):
        """Test that correlation coefficients are within [-1, 1]"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": 0,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check that coefficients are within bounds
        for corr in data["correlations"]:
            assert -1.0 <= corr["coefficient"] <= 1.0

    def test_correlation_p_value_bounds(self, client: TestClient, auth_headers: dict,
                                       test_metrics: list, test_entries: list):
        """Test that p-values are within [0, 1]"""
        request_data = {
            "algorithm": "pearson",
            "max_lag": 0,
            "only_significant": False
        }

        response = client.post("/api/v1/analytics/correlations", json=request_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check that p-values are within bounds
        for corr in data["correlations"]:
            assert 0.0 <= corr["p_value"] <= 1.0
