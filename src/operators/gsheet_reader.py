import pandas as pd

def load_df(url):
    """Load the Google Sheets data into a DataFrame."""
    parse_dates = ["due_date", "reminder_date"]
    df = pd.read_csv(url, parse_dates=parse_dates)
    return df