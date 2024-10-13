# scripts/classify_emails.py

import os
import sys
import logging
import re

# Determine the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logs_dir = os.path.join(project_root, 'logs')

# Create logs directory if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(logs_dir, 'classify_emails.log'),
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Adjust the path to import config
sys.path.append(os.path.join(project_root, 'config'))
import config

def classify_emails():
    selected_phrases = config.SELECTED_PHRASES
    not_selected_phrases = config.NOT_SELECTED_PHRASES

    data_dir = os.path.join(project_root, 'data')
    fetched_emails_path = os.path.join(data_dir, "fetched_emails.txt")
    selected_emails_path = os.path.join(data_dir, "selected_emails.txt")
    not_selected_emails_path = os.path.join(data_dir, "not_selected_emails.txt")
    uncategorized_emails_path = os.path.join(data_dir, "uncategorized_emails.txt")

    try:
        if not os.path.exists(fetched_emails_path):
            logging.warning(f"'{fetched_emails_path}' does not exist. No emails to classify.")
            print(f"No fetched emails found. Skipping classification.")
            return

        with open(fetched_emails_path, "r", encoding="utf-8") as f:
            emails = f.read().split("-" * 50 + "\n")

        if not emails or all(not email_block.strip() for email_block in emails):
            logging.warning("No emails found in 'fetched_emails.txt'.")
            print("No emails to classify.")
            return

        selected_emails = []
        not_selected_emails = []
        uncategorized_emails = []

        for email_block in emails:
            if not email_block.strip():
                continue

            # Convert email content to lowercase for case-insensitive matching
            email_content = email_block.lower()

            # Flag to check classification
            classified = False

            # Check for selected phrases
            for phrase in selected_phrases:
                if re.search(re.escape(phrase.lower()), email_content):
                    selected_emails.append(email_block.strip())
                    classified = True
                    logging.debug(f"Email classified as SELECTED based on phrase: '{phrase}'")
                    break  # Stop checking if matched

            if classified:
                continue  # Move to next email

            # Check for not selected phrases
            for phrase in not_selected_phrases:
                if re.search(re.escape(phrase.lower()), email_content):
                    not_selected_emails.append(email_block.strip())
                    classified = True
                    logging.debug(f"Email classified as NOT_SELECTED based on phrase: '{phrase}'")
                    break  # Stop checking if matched

            if classified:
                continue  # Move to next email

            # If no phrases matched, categorize as uncategorized
            uncategorized_emails.append(email_block.strip())
            logging.debug("Email classified as UNCATEGORIZED.")

        # Save classified emails
        with open(selected_emails_path, "w", encoding="utf-8") as f:
            for email_data in selected_emails:
                f.write(email_data + "\n" + "-" * 50 + "\n")

        with open(not_selected_emails_path, "w", encoding="utf-8") as f:
            for email_data in not_selected_emails:
                f.write(email_data + "\n" + "-" * 50 + "\n")

        with open(uncategorized_emails_path, "w", encoding="utf-8") as f:
            for email_data in uncategorized_emails:
                f.write(email_data + "\n" + "-" * 50 + "\n")

        logging.info(f"Classified emails: {len(selected_emails)} selected, {len(not_selected_emails)} not selected, {len(uncategorized_emails)} uncategorized.")
        print(f"Classified emails: {len(selected_emails)} selected, {len(not_selected_emails)} not selected, {len(uncategorized_emails)} uncategorized.")

    except Exception as e:
        logging.error(f"Failed to classify emails: {e}")
        print(f"An error occurred during classification: {e}")

def main():
    classify_emails()

if __name__ == "__main__":
    main()
