
import yfinance as yf
import pandas as pd
from pathlib import Path


def extract_stock_data(symbol="AAPL"):
    """Download and save historical stock prices."""

    print(f"Downloading stock data for {symbol}...")

    df = yf.download(
        symbol,
        period="1mo",
        interval="1d",
        progress=False
    )

    if df.empty:
        raise ValueError(
            "No stock data received. Check your internet connection."
        )

    # Convert multi-level columns into simple column names
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.reset_index()

    # Save the extracted data inside the project folder
    output_file = (
        Path(__file__).parent / f"{symbol}_stock_data.xlsx"
    )

    df.to_excel(output_file, index=False)

    print(f"Saved {len(df)} rows to {output_file}")

    return df


if __name__ == "__main__":
    stock_data = extract_stock_data("AAPL")
    print(stock_data.tail())
