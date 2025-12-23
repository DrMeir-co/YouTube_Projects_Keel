import pandas as pd
import requests


def get_ticker_data(ticker, country, start="1600-01-01"):
    ticker_suffix = f"{ticker}.{country}"  # Stooq uses suffixes like .us, .uk, etc.
    url = f"https://stooq.com/q/d/l/?s={ticker_suffix}&i=d"

    try:
        df = pd.read_csv(url)  # columns usually: Date, Open, High, Low, Close, Volume
    except (requests.ConnectionError, requests.Timeout, pd.errors.ParserError) as e:
        raise ConnectionError(
            f"Failed to fetch data for {ticker_suffix} from Stooq: {e}"
        )

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.set_index("Date").sort_index()
    return df
