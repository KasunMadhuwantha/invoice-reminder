from datetime import date  # core python module
import pandas as pd  # pip install pandas
from apscheduler.schedulers.blocking import BlockingScheduler
from send_email import send_email  # local python module
import signal
import sys

# Public GoogleSheets URL - not secure!
SHEET_ID = "18iZ2cDnvyaNpjytD-NHZykfSTQECMiidV-cW8c2vAVQ"  # !!! CHANGE ME !!!
SHEET_NAME = "Invoice-client-list"  # !!! CHANGE ME !!!
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

def load_df(url):
    """Load the Google Sheets data into a DataFrame."""
    parse_dates = ["due_date", "reminder_date"]
    df = pd.read_csv(url, parse_dates=parse_dates)
    return df

def query_data_and_send_emails(df):
    """Query the DataFrame and send email reminders."""
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        if (present >= row["reminder_date"].date()) and (row["has_paid"] == "no"):
            send_email(
                subject=f'[Invoice Reminder] Invoice: {row["invoice_no"]}',
                receiver_email=row["email"],
                name=row["name"],
                due_date=row["due_date"].strftime("%d, %b %Y"),  # e.g., 11, Aug 2022
                invoice_no=row["invoice_no"],
                amount=row["amount"],
            )
            email_counter += 1
    return f"Total Emails Sent: {email_counter}"

def cron_job():
    """Function to load data, query, and send emails."""
    print("Running cron job...")
    try:
        df = load_df(URL)
        result = query_data_and_send_emails(df)
        print(result)
    except Exception as e:
        print(f"Error occurred: {e}")

# Gracefully exit when Ctrl+C is pressed
def handle_exit(sig, frame):
    print("\nScheduler stopped by user.")
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handler for graceful exit
    signal.signal(signal.SIGINT, handle_exit)

    # Initialize the scheduler
    scheduler = BlockingScheduler()
    
    # Schedule the cron job to run daily at 19:17 (adjust as needed)
    scheduler.add_job(cron_job, "cron", hour=19, minute=18)
    print("Scheduler started! Waiting for the next scheduled run...")

    # Start the scheduler
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")
