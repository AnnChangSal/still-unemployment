# Still Unemployment?

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![GitHub Issues](https://img.shields.io/github/issues/AnnChangSal/still-unemployment)
![GitHub Forks](https://img.shields.io/github/forks/AnnChangSal/still-unemployment)
![GitHub Stars](https://img.shields.io/github/stars/AnnChangSal/still-unemployment)

## Table of Contents

- [About The Project](#about-the-project)
- [Features](#features)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Set Up Virtual Environment](#set-up-virtual-environment)
  - [Install Dependencies](#install-dependencies)
  - [Configure Environment Variables](#configure-environment-variables)
- [Usage](#usage)
  - [Running the Scripts](#running-the-scripts)
  - [Scheduling with Cron](#scheduling-with-cron)
- [Project Structure](#project-structure)
  

## About The Project

![Project Screenshot](assets/screenshot.png)

**Still Unemployment?** is a Python-based project designed to help individuals manage and analyze their job application emails. By leveraging Gmail's IMAP protocol, the application fetches relevant emails, classifies them based on predefined phrases, and organizes them for easy review. This tool aims to streamline the job search process, allowing users to focus on responding to potential opportunities while efficiently handling rejection notices.

- Just check how many you got rejected with me

## Features

- **Email Fetching:** Connects to Gmail's IMAP server to retrieve emails from the inbox.
- **Authentication:** Utilizes secure App Passwords for authenticating with Gmail.
- **Email Classification:** Categorizes emails based on selected and non-selected phrases.
- **Data Storage:** Saves fetched and processed emails in a structured format for easy access.
- **Logging:** Maintains detailed logs for monitoring and troubleshooting.
- **Automation Ready:** Easily schedulable using cron jobs or Windows Task Scheduler for regular email fetching.

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- **Python 3.8+**
- **Git**

### Clone the Repository

```
bash
git clone https://github.com/AnnChangSal/still-unemployment.git
cd still-unemployment
```

### Set Up Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

On macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

On Windows:
```
python -m venv venv
venv\Scripts\activate
```
### Install Dependencies
```
pip install -r requirements.txt
```

### Configure Environment Variables
1. Create a .env File:

  In the project root directory, create a file named .env
2. Add the Floowing Variables:
```
# .env

# Gmail Credentials
GMAIL_EMAIL=your_gmail@gmail.com
GMAIL_PASSWORD=your_gmail_app_password

# SMTP Credentials (Optional, for sending notifications)
SMTP_EMAIL=your_smtp_email@gmail.com
SMTP_PASSWORD=your_smtp_password

# Classification Phrases
SELECTED_PHRASES=["congratulations", "pleased to inform you", "welcome to the team", "interview with us", "we are excited to have you", "you have been selected", "you are hired", "we would like to offer you", "successful application"]
NOT_SELECTED_PHRASES=["will not be moving your application forward", "decided not to move forward", "regret to inform you", "decided to move forward with other candidates", "thank you for your interest", "unfortunately, we have decided", "your application has been rejected", "we appreciate your interest", "no longer considering your application", "not selected for the position", "application unsuccessful", "moving forward with other applicants"]

```
**Need to change the variables**
1. your_gmail@gmail.com
2. your_gmail_app_password
3. your_smtp_email@gmail.com
4. your_smtp_password

5. (option) you can change SELECTED_PHRASES and NOT_SELECTED_PHRASES to your own

3. Generate a Gmail App Password:

   If you have Two-Factor Authentication (2FA) enabled on your Gmail account, you'll need to generate an App Password.
   - Steps to Generate an App Password:
      1. Go to your Google Account.
      2. Navigate to "Security".
      3. Under "Signing in to Google", select "App passwords".
      4. You might need to sign in again.
      5. Select "Mail" as the app and "Other (Custom name)" as the device (e.g., StillUnemploymentApp).
      6. Click "Generate" and copy the generated 16-character password (without spaces).
      7. Paste this password as the value for GMAIL_PASSWORD in your .env file (without spaces).
    

### Usage

### Running the Scripts
1. Activate Virtual Environment:
    On macOS/Linux:
   ```
   source venv/bin/activate
   ```
    On Windows:
   ```
   venv\Scripts\activate
   ```
2. Run the Email Fetching Script:
   ```
   python3 scripts/fetch_emails.py
   ```
   Output:
   ```
   Fetched X emails and saved to 'data/fetched_emails.txt'.
   ```
3. Run the Master Script (If Applicable):
   If you have a master script to run all components(in here, run_all):
   ```
   python3 run_all.py
    ```

### Scheduling with Cron
To automate the email fetching process, you can schedule the script to run at regular intervals using cron (on macOS/Linux) or Task Scheduler (on Windows).

Example (Using Cron on macOS/Linux):
1. Open Crontab Editor:
   ```
   crontab -e
   ```
2. Add the Following Line to Schedule the Scirpt Daily at 9 AM:
   ```
   0 9 * * * /path/to/your/venv/bin/python3 /path/to/your/project/scripts/fetch_emails.py >> /path/to/your/project/logs/cron.log 2>&1
   ```
   - 0 9 * * *: Runs the script every day at 9:00 AM.
   - Replace /path/to/your/venv/ and /path/to/your/project/ with the actual paths.
3. Save and Exit:
   - In nano, press Ctrl + O to save and Ctrl + X to exit.


### Project Structure
```
still-unemployment/
├── data/
│   └── fetched_emails.txt
├── logs/
│   ├── fetch_emails.log
│   └── cron.log
├── scripts/
│   ├── fetch_emails.py
│   └── other_scripts.py
├── config/
│   └── config.py
├── venv/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
└── run_all.py
```
- data/: Stores fetched and processed email data.
- logs/: Contains log files for monitoring and troubleshooting.
- scripts/: Houses individual Python scripts for various tasks.
- config/: Contains configuration files.
- venv/: Virtual environment directory.
- .env: Environment variables file (should be excluded from version control).
- .gitignore: Specifies intentionally untracked files to ignore.
- README.md: Project documentation.
- requirements.txt: Lists Python dependencies.
- run_all.py: Master script to execute all components.
