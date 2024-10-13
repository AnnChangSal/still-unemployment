

import os
from dotenv import load_dotenv
import ast

# Determine the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Load variables from .env file located at project root
load_dotenv(os.path.join(project_root, '.env'))

# Gmail Credentials
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

if not GMAIL_EMAIL or not GMAIL_PASSWORD:
    raise ValueError("GMAIL_EMAIL and GMAIL_PASSWORD must be set in the .env file.")

# SMTP Credentials (Optional, if you plan to send notifications)
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# Classification Phrases
SELECTED_PHRASES = [
    "congratulations",
    "pleased to inform you",
    "welcome to the team",
    "interview with us",
    "we are excited to have you",
    "you have been selected",
    "you are hired",
    "we would like to offer you",
    "successful application"
]

NOT_SELECTED_PHRASES = [
    "will not be moving your application forward",
    "decided not to move forward",
    "regret to inform you",
    "decided to move forward with other candidates",
    "thank you for your interest",
    "unfortunately, we have decided",
    "your application has been rejected",
    "we appreciate your interest",
    "no longer considering your application",
    "not selected for the position",
    "application unsuccessful",
    "moving forward with other applicants"
]
