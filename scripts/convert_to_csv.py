# scripts/convert_to_csv.py

import os
import sys
import logging
import csv
import re

# Determine the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logs_dir = os.path.join(project_root, 'logs')

# Create logs directory if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(logs_dir, 'convert_to_csv.log'),
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Adjust the path to import config (if needed)
sys.path.append(os.path.join(project_root, 'config'))
import config

def extract_email_components(email_block):
    """
    Extracts Subject, From, and Body from a single email block.
    """
    subject = ""
    from_ = ""
    body = ""
    for line in email_block.split('\n'):
        if line.startswith("Subject: "):
            subject = line.replace("Subject: ", "").strip()
        elif line.startswith("From: "):
            from_ = line.replace("From: ", "").strip()
        elif line.startswith("Body: "):
            body = line.replace("Body: ", "").strip()
    return subject, from_, body

def convert_to_csv():
    data_dir = os.path.join(project_root, 'data')
    classified_files = {
        "selected_emails.csv": "selected_emails.txt",
        "not_selected_emails.csv": "not_selected_emails.txt",
        "uncategorized_emails.csv": "uncategorized_emails.txt"
    }

    try:
        for csv_filename, txt_filename in classified_files.items():
            txt_path = os.path.join(data_dir, txt_filename)
            csv_path = os.path.join(data_dir, csv_filename)

            if not os.path.exists(txt_path):
                logging.warning(f"'{txt_path}' does not exist. Skipping conversion.")
                print(f"No '{txt_filename}' found. Skipping CSV conversion for this category.")
                continue

            with open(txt_path, "r", encoding="utf-8") as f:
                # Split emails based on the delimiter
                email_blocks = re.split(r'-{50}\n', f.read())

            if not email_blocks or all(not email_block.strip() for email_block in email_blocks):
                logging.warning(f"No emails found in '{txt_filename}'.")
                print(f"No emails to convert in '{txt_filename}'.")
                continue

            emails = []
            for email_block in email_blocks:
                if not email_block.strip():
                    continue
                subject, from_, body = extract_email_components(email_block)
                emails.append({
                    "Subject": subject,
                    "From": from_,
                    "Body": body
                })

            # Write to CSV
            with open(csv_path, "w", newline='', encoding="utf-8") as csvfile:
                fieldnames = ["Subject", "From", "Body"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for email_data in emails:
                    writer.writerow(email_data)

            logging.info(f"Converted {len(emails)} emails from '{txt_filename}' to '{csv_filename}'.")
            print(f"Converted {len(emails)} emails from '{txt_filename}' to '{csv_filename}'.")

    except Exception as e:
        logging.error(f"Failed to convert emails to CSV: {e}")
        print(f"An error occurred during CSV conversion: {e}")

def main():
    convert_to_csv()

if __name__ == "__main__":
    main()
