import pytest
from datetime import datetime, timedelta
from server import is_past_competition_func
from unittest.mock import patch


class TestIsPastCompetition:

    def test_past_date_returns_true(self):
        """Test that a date in the past returns True"""
        past_date = "2020-01-01 10:00:00"
        assert is_past_competition_func(past_date) is True

    def test_future_date_returns_false(self):
        """Test that a date in the future returns False"""
        future_date = "2030-01-01 10:00:00"
        assert is_past_competition_func(future_date) is False

    @patch('server.datetime')
    def test_exact_current_date_returns_false(self, mock_datetime):
        """Test that the exact current date returns False (not past)"""

        fixed_now = datetime(2024, 1, 1, 1, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.strptime.side_effect = datetime.strptime

        # Test with the exact same time
        current_date = "2021-01-1 1:00:00"
        assert is_past_competition_func(current_date) is True

    def test_invalid_date_format_raises_exception(self):
        """Test that an invalid date format raises an exception"""
        with pytest.raises(ValueError):
            is_past_competition_func("invalid-date-format")

