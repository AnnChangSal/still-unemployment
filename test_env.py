# test_env.py

import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Fetch environment variables
gmail_email = os.getenv("GMAIL_EMAIL")
gmail_password = os.getenv("GMAIL_PASSWORD")

print(f"GMAIL_EMAIL: {gmail_email}")
print(f"GMAIL_PASSWORD: {'***' if gmail_password else 'None'}")  # Mask the password
