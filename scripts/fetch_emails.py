# scripts/fetch_emails.py

import imaplib
import email
from email.header import decode_header
import sys
import os
import logging

# Determine the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
logs_dir = os.path.join(project_root, 'logs')

# Create logs directory if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(logs_dir, 'fetch_emails.log'),
    level=logging.DEBUG,  # Set to DEBUG for detailed logs
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Adjust the path to import config
sys.path.append(os.path.join(project_root, 'config'))
import config

def clean_subject(subject):
    if subject is None:
        logging.debug("Subject is None. Setting to 'No Subject'.")
        return "No Subject"
    try:
        decoded_parts = decode_header(subject)
        subject, encoding = decoded_parts[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")
        logging.debug(f"Decoded Subject: {subject}")
    except Exception as e:
        logging.error(f"Error decoding subject: {e}")
        subject = "No Subject"
    return subject

def clean_from(from_):
    if from_ is None:
        logging.debug("From field is None. Setting to 'Unknown Sender'.")
        return "Unknown Sender"
    try:
        decoded_parts = decode_header(from_)
        from_, encoding = decoded_parts[0]
        if isinstance(from_, bytes):
            from_ = from_.decode(encoding if encoding else "utf-8")
        logging.debug(f"Decoded From: {from_}")
    except Exception as e:
        logging.error(f"Error decoding from field: {e}")
        from_ = "Unknown Sender"
    return from_

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                body = part.get_payload(decode=True)
                if body is None:
                    logging.debug("Body payload is None.")
                    continue
                body = body.decode()
                logging.debug("Decoded multipart body.")
            except Exception as e:
                logging.error(f"Error decoding body: {e}")
                body = ""
            if content_type == "text/plain" and "attachment" not in content_disposition:
                logging.debug("Found text/plain part without attachment.")
                return body
    else:
        content_type = msg.get_content_type()
        try:
            body = msg.get_payload(decode=True)
            if body is None:
                logging.debug("Body payload is None.")
                return ""
            body = body.decode()
            logging.debug("Decoded non-multipart body.")
        except Exception as e:
            logging.error(f"Error decoding body: {e}")
            body = ""
        if content_type == "text/plain":
            logging.debug("Found text/plain email.")
            return body
    return ""

def fetch_emails(email_user, email_pass, imap_server):
    try:
        # Connect to the server
        mail = imaplib.IMAP4_SSL(imap_server)
        logging.info(f"Connected to IMAP server: {imap_server}")

        # Login to account
        mail.login(email_user, email_pass)
        logging.info(f"Logged in as {email_user}")

        # Select the mailbox you want to use
        mail.select("inbox")
        logging.info("Selected mailbox: INBOX")

        # Search for all emails
        status, messages = mail.search(None, "ALL")
        if status != "OK":
            logging.error(f"Failed to search emails in {imap_server}")
            return []

        # Convert messages to a list of email IDs
        email_ids = messages[0].split()
        logging.info(f"Total emails found: {len(email_ids)}")

        emails = []

        for mail_id in email_ids[-100:]:  # Fetch the last 100 emails
            status, msg_data = mail.fetch(mail_id, "(RFC822)")
            if status != "OK":
                logging.warning(f"Failed to fetch email ID {mail_id}")
                continue

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = clean_subject(msg["Subject"])
                    from_ = clean_from(msg.get("From"))
                    body = get_email_body(msg)
                    emails.append({
                        "Subject": subject,
                        "From": from_,
                        "Body": body
                    })

        logging.info(f"Fetched {len(emails)} emails from {imap_server}")

    except imaplib.IMAP4.error as e:
        logging.error(f"IMAP error: {e}")
        return []
    except Exception as e:
        logging.exception(f"Failed to fetch emails from {imap_server}: {e}")
        return []
    finally:
        try:
            mail.logout()
            logging.info(f"Logged out from {imap_server}")
        except Exception as e:
            logging.error(f"Error logging out: {e}")

    return emails

def main():
    try:
        # Fetch Gmail Emails
        gmail_emails = fetch_emails(
            config.GMAIL_EMAIL,
            config.GMAIL_PASSWORD,
            "imap.gmail.com"
        )

        # Since we're focusing solely on Gmail, no need to fetch from Outlook

        all_emails = gmail_emails

        # Save to a File
        data_dir = os.path.join(project_root, 'data')
        os.makedirs(data_dir, exist_ok=True)
        fetched_emails_path = os.path.join(data_dir, "fetched_emails.txt")

        with open(fetched_emails_path, "w", encoding="utf-8") as f:
            for email_data in all_emails:
                # Ensure all fields are strings
                subject = email_data.get('Subject') or "No Subject"
                from_ = email_data.get('From') or "Unknown Sender"
                body = email_data.get('Body') or ""
                
                f.write(f"Subject: {subject}\n")
                f.write(f"From: {from_}\n")
                f.write(f"Body: {body}\n")
                f.write("-" * 50 + "\n")

        logging.info(f"Fetched {len(all_emails)} emails and saved to '{fetched_emails_path}'.")
        print(f"Fetched {len(all_emails)} emails and saved to 'fetched_emails.txt'.")

    except Exception as e:
        logging.exception(f"An error occurred in main: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
