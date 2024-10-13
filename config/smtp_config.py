import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

SMTP_SERVER = "smtp.gmail.com"  # Adjust if using a different SMTP server
SMTP_PORT = 587  # For TLS
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
