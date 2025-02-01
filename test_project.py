import pytest
from utils import select_time_frame, generate_table  # Importing utility functions
from main import generate_report  # Importing function from main

def test_select_time_frame(monkeypatch):
    """Test if the time frame selection returns a valid list."""
    mock_input = iter(["1", "2"])  # Simulate user selecting "By Day" then "Yesterday"
    monkeypatch.setattr('builtins.input', lambda _: next(mock_input))
    dates = select_time_frame()
    assert isinstance(dates, list), "Expected a list of dates"
    assert all(isinstance(date, str) for date in dates), "All elements should be strings"

def test_generate_table():
    """Test if generate_table can process and display data without errors."""
    sample_data = [("123", "Test Video", 1000, 100), ("124", "Another Video", 500, 50)]  # Added Likes
    try:
        generate_table(sample_data, columns=[0, 1, 2, 3], summary=True)
        assert True  # If no error, test passes
    except Exception as e:
        pytest.fail(f"generate_table raised an exception: {e}")

def test_generate_report():
    """Test if generate_report function executes without errors."""
    sample_date = "2025-01-15"  # Single string, NOT a list
    try:
        generate_report(sample_date)  # Pass a single string instead of a list
        assert True  # If function executes without error, test passes
    except Exception as e:
        pytest.fail(f"generate_report raised an exception: {e}")

if __name__ == "__main__":
    pytest.main()
