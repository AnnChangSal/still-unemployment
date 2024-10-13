# scripts/run_all.py

import subprocess
import time
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
    filename=os.path.join(logs_dir, 'run_all.log'),
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

def run_script(script_name):
    try:
        # Construct the absolute path to the script
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        # Pass the current environment variables to the subprocess
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True,
            env=os.environ
        )
        logging.info(f"✅ {script_name} ran successfully.")
        logging.info(f"Output:\n{result.stdout}")
        print(f"✅ {script_name} ran successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ {script_name} failed.")
        logging.error(f"Error Output:\n{e.stderr}")
        print(f"❌ {script_name} failed.")
        print("Error Output:")
        print(e.stderr)

def main():
    while True:
        try:
            logging.info("🔄 Starting the email processing cycle.")
            print("🔄 Starting the email processing cycle.")

            scripts = [
                "fetch_emails.py",
                "classify_emails.py",
                "convert_to_csv.py"
            ]

            for script in scripts:
                run_script(script)

            logging.info("🔔 Email processing cycle completed.")
            print("🔔 Email processing cycle completed.")

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            print(f"An unexpected error occurred: {e}")

        finally:
            logging.info("🔔 Setting the next check in 1 minutes.")
            print("🔔 Setting the next check in 1 minutes.")
            time.sleep(60)  # Wait for 60 seconds before the next run

if __name__ == "__main__":
    main()
