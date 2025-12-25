import pandas as pd
import requests
from urllib.error import HTTPError, URLError


def fetch_from_stooq(ticker):
    """
    Fetch raw ticker data from Stooq.

    Args:
        ticker (str): ticker symbol of the form "AAPL.US".

    Returns:
        pd.DataFrame: DataFrame with columns Date, Open, High, Low, Close, Volume.
    """
    url = f"https://stooq.com/q/d/l/?s={ticker}&i=d"
    return pd.read_csv(url)


def validate_ticker_df(df: pd.DataFrame) -> None:
    """
    Validate that df is a non-empty DataFrame with required columns.
    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"Expected a pandas DataFrame, got {type(df)!r}")
    if df.empty:
        raise ValueError("Received an empty DataFrame")
    required = {"Date", "Close"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def get_ticker_data(source, ticker, country):
    """
    Fetch ticker data from a configured data source.

    Args:
        source (str): data source name (e.g., "stooq").
        ticker (str): ticker symbol (e.g., "AAPL").
        country (str): country suffix (e.g., "US").

    Returns:
        pd.DataFrame: DataFrame containing the fetched price data.
    """
    symbol = ticker if "." in str(ticker) else f"{ticker}.{country}"

    try:
        if source == "stooq":
            df = fetch_from_stooq(symbol.lower())
        else:
            raise ValueError(f"Unsupported data source: {source!r}")
    except (
        HTTPError,
        URLError,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
        requests.exceptions.RequestException,
    ) as e:
        raise RuntimeError(
            f"Failed to fetch data from {source!r} for {symbol!r}"
        ) from e

    validate_ticker_df(df)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date").sort_index()
    return df
