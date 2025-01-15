from src.operators.gsheet_reader import load_df
from src.operators.email_sender import query_data_and_send_emails
from src.configurations.config import URL


df =load_df(URL)
print(df)
query_data_and_send_emails(df)
print("Emails Sent")


if __name__ == "__main__":
    pass


