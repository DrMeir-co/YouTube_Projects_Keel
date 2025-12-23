import pandas as pd
from unittest.mock import patch
from keel.ticker import get_ticker_data


def test_get_ticker_data_returns_sorted_datetime_index():
    mock_data = {
        "Date": ["2024-01-03", "2024-01-01", "2024-01-02"],
        "Open": [100, 98, 99],
        "High": [102, 100, 101],
        "Low": [99, 97, 98],
        "Close": [101, 99, 100],
        "Volume": [1000, 1100, 1050],
    }
    mock_df = pd.DataFrame(mock_data)

    with patch("keel.ticker.pd.read_csv", return_value=mock_df):
        result = get_ticker_data("AAPL", "us")

    assert isinstance(result.index, pd.DatetimeIndex)
    assert result.index.is_monotonic_increasing
    assert len(result) == 3
