"""
Unit tests for correlation analysis engine
"""
import pytest
import numpy as np
from app.analytics.correlation import CorrelationEngine, CorrelationResult


class TestCorrelationEngine:
    """Tests for the CorrelationEngine class"""

    def test_init_default_params(self):
        """Test engine initialization with default parameters"""
        engine = CorrelationEngine()
        assert engine.min_significance == 0.05
        assert engine.min_sample_size == 7

    def test_init_custom_params(self):
        """Test engine initialization with custom parameters"""
        engine = CorrelationEngine(min_significance=0.01, min_sample_size=10)
        assert engine.min_significance == 0.01
        assert engine.min_sample_size == 10

    def test_calculate_correlation_pearson_perfect_positive(self):
        """Test Pearson correlation with perfect positive correlation"""
        engine = CorrelationEngine()
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        coefficient, p_value = engine.calculate_correlation(x, y, algorithm='pearson')

        assert coefficient == pytest.approx(1.0, abs=1e-10)
        assert p_value < 0.05

    def test_calculate_correlation_pearson_perfect_negative(self):
        """Test Pearson correlation with perfect negative correlation"""
        engine = CorrelationEngine()
        x = [1, 2, 3, 4, 5]
        y = [10, 8, 6, 4, 2]

        coefficient, p_value = engine.calculate_correlation(x, y, algorithm='pearson')

        assert coefficient == pytest.approx(-1.0, abs=1e-10)
        assert p_value < 0.05

    def test_calculate_correlation_pearson_no_correlation(self):
        """Test Pearson correlation with no correlation"""
        engine = CorrelationEngine()
        x = [1, 2, 3, 4, 5]
        y = [3, 3, 3, 3, 3]  # Constant values

        coefficient, p_value = engine.calculate_correlation(x, y, algorithm='pearson')

        # With constant y, correlation is NaN
        assert np.isnan(coefficient)

    def test_calculate_correlation_spearman(self):
        """Test Spearman rank correlation"""
        engine = CorrelationEngine()
        x = [1, 2, 3, 4, 5]
        y = [1, 4, 9, 16, 25]  # Quadratic relationship

        coefficient, p_value = engine.calculate_correlation(x, y, algorithm='spearman')

        # Spearman should detect monotonic relationship
        assert coefficient == pytest.approx(1.0, abs=1e-10)
        assert p_value < 0.05

    def test_calculate_correlation_kendall(self):
        """Test Kendall tau correlation"""
        engine = CorrelationEngine()
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]

        coefficient, p_value = engine.calculate_correlation(x, y, algorithm='kendall')

        assert coefficient == pytest.approx(1.0, abs=1e-10)
        assert p_value < 0.05

    def test_calculate_correlation_with_nan(self):
        """Test correlation calculation with NaN values"""
        engine = CorrelationEngine()
        x = [1, 2, np.nan, 4, 5]
        y = [2, 4, 6, np.nan, 10]

        coefficient, p_value = engine.calculate_correlation(x, y, algorithm='pearson')

        # Should filter out NaN pairs and calculate on remaining data
        assert not np.isnan(coefficient)
        # Only 3 valid pairs remain: (1,2), (2,4), (5,10)
        # Perfect positive correlation
        assert coefficient == pytest.approx(1.0, abs=1e-10)

    def test_calculate_lag_correlation_no_lag(self):
        """Test lag correlation when best correlation is at lag 0"""
        engine = CorrelationEngine()
        x = [1, 2, 3, 4, 5, 6, 7]
        y = [2, 4, 6, 8, 10, 12, 14]

        coefficient, p_value, lag = engine.calculate_lag_correlation(
            x, y, max_lag=3, algorithm='pearson'
        )

        assert lag == 0
        assert coefficient == pytest.approx(1.0, abs=1e-10)
        assert p_value < 0.05

    def test_calculate_lag_correlation_with_lag(self):
        """Test lag correlation when there's a delayed effect"""
        engine = CorrelationEngine()
        # x affects y after 2 days
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [0, 0, 2, 4, 6, 8, 10, 12, 14, 16]  # y = 2*(x lagged by 2)

        coefficient, p_value, lag = engine.calculate_lag_correlation(
            x, y, max_lag=5, algorithm='pearson'
        )

        # Should detect lag of 2
        assert lag == 2
        assert abs(coefficient) > 0.9  # Strong correlation

    def test_classify_strength_strong(self):
        """Test strength classification for strong correlation"""
        engine = CorrelationEngine()

        assert engine.classify_strength(0.8) == "strong"
        assert engine.classify_strength(-0.7) == "strong"

    def test_classify_strength_moderate(self):
        """Test strength classification for moderate correlation"""
        engine = CorrelationEngine()

        assert engine.classify_strength(0.5) == "moderate"
        assert engine.classify_strength(-0.4) == "moderate"

    def test_classify_strength_weak(self):
        """Test strength classification for weak correlation"""
        engine = CorrelationEngine()

        assert engine.classify_strength(0.2) == "weak"
        assert engine.classify_strength(-0.1) == "weak"

    def test_classify_direction_positive(self):
        """Test direction classification for positive correlation"""
        engine = CorrelationEngine()

        assert engine.classify_direction(0.5) == "positive"

    def test_classify_direction_negative(self):
        """Test direction classification for negative correlation"""
        engine = CorrelationEngine()

        assert engine.classify_direction(-0.5) == "negative"

    def test_classify_direction_zero(self):
        """Test direction classification for zero correlation"""
        engine = CorrelationEngine()

        assert engine.classify_direction(0.0) == "none"

    def test_analyze_pair_sufficient_data(self):
        """Test analyze_pair with sufficient data"""
        engine = CorrelationEngine()

        metric1_data = {'name': 'Sleep', 'data': [7, 8, 6, 7, 8, 7, 6, 8]}
        metric2_data = {'name': 'Mood', 'data': [7, 8, 6, 7, 9, 7, 6, 8]}

        result = engine.analyze_pair(
            metric1_id=1,
            metric1_data=metric1_data,
            metric2_id=2,
            metric2_data=metric2_data,
            algorithm='pearson',
            max_lag=0
        )

        assert result is not None
        assert result.metric_1_id == 1
        assert result.metric_2_id == 2
        assert result.metric_1_name == 'Sleep'
        assert result.metric_2_name == 'Mood'
        assert result.algorithm == 'pearson'
        assert result.sample_size == 8
        assert result.strength in ['weak', 'moderate', 'strong']
        assert result.direction in ['positive', 'negative', 'none']

    def test_analyze_pair_insufficient_data(self):
        """Test analyze_pair with insufficient data"""
        engine = CorrelationEngine(min_sample_size=10)

        metric1_data = {'name': 'Sleep', 'data': [7, 8, 6]}  # Only 3 points
        metric2_data = {'name': 'Mood', 'data': [7, 8, 6]}

        result = engine.analyze_pair(
            metric1_id=1,
            metric1_data=metric1_data,
            metric2_id=2,
            metric2_data=metric2_data,
            algorithm='pearson',
            max_lag=0
        )

        assert result is None

    def test_analyze_pair_mismatched_lengths(self):
        """Test analyze_pair with mismatched data lengths"""
        engine = CorrelationEngine()

        metric1_data = {'name': 'Sleep', 'data': [7, 8, 6, 7, 8]}
        metric2_data = {'name': 'Mood', 'data': [7, 8, 6]}  # Shorter

        # Should pad with NaN
        result = engine.analyze_pair(
            metric1_id=1,
            metric1_data=metric1_data,
            metric2_id=2,
            metric2_data=metric2_data,
            algorithm='pearson',
            max_lag=0
        )

        # Should only use the overlapping 3 values
        assert result is None or result.sample_size == 3

    def test_analyze_all_pairs_basic(self):
        """Test analyze_all_pairs with basic data"""
        engine = CorrelationEngine()

        metrics_data = {
            1: {'name': 'Sleep', 'data': [7, 8, 6, 7, 8, 7, 6, 8]},
            2: {'name': 'Mood', 'data': [7, 8, 6, 7, 9, 7, 6, 8]},
            3: {'name': 'Exercise', 'data': [1, 1, 0, 1, 1, 1, 0, 1]},
        }

        results = engine.analyze_all_pairs(
            metrics_data=metrics_data,
            algorithm='pearson',
            max_lag=0,
            only_significant=False
        )

        # Should have 3 pairs: (1,2), (1,3), (2,3)
        assert len(results) == 3

        # Check all pairs are present
        pairs = {(r.metric_1_id, r.metric_2_id) for r in results}
        assert (1, 2) in pairs or (2, 1) in pairs
        assert (1, 3) in pairs or (3, 1) in pairs
        assert (2, 3) in pairs or (3, 2) in pairs

    def test_analyze_all_pairs_only_significant(self):
        """Test analyze_all_pairs filtering only significant results"""
        engine = CorrelationEngine()

        metrics_data = {
            1: {'name': 'Sleep', 'data': [7, 8, 6, 7, 8, 7, 6, 8, 7, 8]},
            2: {'name': 'Mood', 'data': [7, 8, 6, 7, 9, 7, 6, 8, 7, 8]},
            3: {'name': 'Random', 'data': [5, 3, 8, 2, 9, 1, 4, 7, 6, 2]},  # Random
        }

        results_all = engine.analyze_all_pairs(
            metrics_data=metrics_data,
            algorithm='pearson',
            max_lag=0,
            only_significant=False
        )

        results_significant = engine.analyze_all_pairs(
            metrics_data=metrics_data,
            algorithm='pearson',
            max_lag=0,
            only_significant=True
        )

        # Should have fewer or equal significant results
        assert len(results_significant) <= len(results_all)

        # All returned results should be significant
        for result in results_significant:
            assert result.significant is True

    def test_correlation_result_dataclass(self):
        """Test CorrelationResult dataclass"""
        result = CorrelationResult(
            metric_1_id=1,
            metric_1_name="Sleep",
            metric_2_id=2,
            metric_2_name="Mood",
            coefficient=0.75,
            p_value=0.01,
            lag=0,
            strength="strong",
            significant=True,
            direction="positive",
            sample_size=10,
            algorithm="pearson"
        )

        assert result.metric_1_id == 1
        assert result.metric_1_name == "Sleep"
        assert result.metric_2_id == 2
        assert result.metric_2_name == "Mood"
        assert result.coefficient == 0.75
        assert result.p_value == 0.01
        assert result.lag == 0
        assert result.strength == "strong"
        assert result.significant is True
        assert result.direction == "positive"
        assert result.sample_size == 10
        assert result.algorithm == "pearson"

    def test_real_world_scenario_sleep_mood(self):
        """Test with realistic sleep-mood correlation data"""
        engine = CorrelationEngine()

        # Realistic scenario: better sleep leads to better mood
        sleep_hours = [7, 8, 6, 5, 7, 8, 9, 6, 7, 8, 7, 6, 8, 7]
        mood_scores = [7, 8, 5, 4, 7, 8, 9, 5, 7, 8, 7, 5, 8, 7]

        coefficient, p_value = engine.calculate_correlation(
            sleep_hours, mood_scores, algorithm='pearson'
        )

        # Should show positive correlation
        assert coefficient > 0.5
        assert p_value < 0.05

    def test_edge_case_all_nan(self):
        """Test with all NaN values"""
        engine = CorrelationEngine()

        x = [np.nan, np.nan, np.nan]
        y = [np.nan, np.nan, np.nan]

        coefficient, p_value = engine.calculate_correlation(x, y, algorithm='pearson')

        # Should return NaN
        assert np.isnan(coefficient)
        assert np.isnan(p_value)

    def test_edge_case_single_valid_pair(self):
        """Test with only one valid pair after NaN filtering"""
        engine = CorrelationEngine()

        x = [1, np.nan, np.nan]
        y = [2, np.nan, np.nan]

        coefficient, p_value = engine.calculate_correlation(x, y, algorithm='pearson')

        # Cannot calculate correlation with only one pair
        assert np.isnan(coefficient)
        assert np.isnan(p_value)
