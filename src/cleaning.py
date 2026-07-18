import pandas as pd

def clean_data(df):
    """
    Clean the stock dataset.
    """

    # Drop Notes column if it exists
    if "Notes" in df.columns:
        df = df.drop(columns=["Notes"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Remove rows with missing values
    df = df.dropna()

    # Sort by ticker and date
    df = df.sort_values(["Ticker", "Date"])

    # Reset index
    df = df.reset_index(drop=True)

    return df