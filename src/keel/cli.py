from datetime import datetime
import logging

import typer

from keel.logger import configure_logger
from keel.ticker import get_ticker_data

logger, handler = configure_logger(logfile="errors.log", level=logging.ERROR)


def record_failure(msg: str) -> None:
    """Failure logging helper."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    handler.stream.write(f"{'=' * 80}\n" f"{timestamp}\n" f"{'=' * 80}\n")
    handler.flush()
    logger.exception(msg)


app = typer.Typer()


@app.command()
def fetch(ticker: str, country: str = "US", source: str = "stooq"):
    """Fetch and display ticker data"""

    try:
        df = get_ticker_data(source, ticker, country)
        print(df)
    except Exception:
        msg = f"Error fetching data for {ticker}.{country} from {source.title()}"
        record_failure(msg)
        typer.echo(msg)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
