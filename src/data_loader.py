import pandas as pd


def load_dataset(path):
    """
    Load CSV dataset.
    """

    df = pd.read_csv(path)

    df["Date"] = pd.to_datetime(df["Date"])

    return df


if __name__ == "__main__":
    df = load_dataset("Data/Raw_data/nifty500_complete_daily_data.csv")
    print(df.head())
    print(df.shape)