import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path

# from dotenv import load_dotenv 

PORT = 587  
EMAIL_SERVER = "smtp.gmail.com"  # Adjust server address, if you are not using @outlook

# # Load the environment variables
# current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
# envars = current_dir / ".env"
# load_dotenv(envars)

# Read environment variables
# sender_email = os.getenv("EMAIL")
# password_email = os.getenv("PASSWORD")

sender_email = "marketing.dozen@gmail.com"
password_email ="whmwyyhaiuyjaiqb" 


def send_email(subject, receiver_email, name, due_date, invoice_no, amount):
    # Create the base text message.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Dozen Solutions.", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        Hi {name},
        I hope you are well.
        I just wanted to drop you a quick note to remind you that LKR {amount} in respect of our invoice {invoice_no} is due for payment on {due_date}.
        I would be really grateful if you could confirm that everything is on track for payment.
        Best regards
        Dozen Solutions
        """
    )
    # Add the html version.  This converts the message into a multipart/alternative
    # container, with the original text message as the first part and the new html
    # message as the second part.
    msg.add_alternative(
        f"""\
    <html>
      <body>
        <p>Hi {name},</p>
        <p>I hope you are well.</p>
        <p>I just wanted to drop you a quick note to remind you that <strong> LKR {amount}</strong>  in respect of our invoice {invoice_no} is due for payment on <strong>{due_date}</strong>.</p>
        <p>I would be really grateful if you could confirm that everything is on track for payment.</p>
        <p>Best regards</p>
        <p>Dozen Solutions</p>
      </body>
    </html>
    """,
        subtype="html",
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, password_email)
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == "__main__":
    send_email(
        subject="Invoice Reminder",
        name="Venura Pussella",
        receiver_email="venurajithmal@gmail.com",
        due_date="11, Aug 2024",
        invoice_no="INV-21-12-009",
        amount="5 000.00",
    )
