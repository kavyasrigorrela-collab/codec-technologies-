# scheduler.py
import schedule
import time
from scraper import init_db, scrape_quotes, export_to_csv

# Initialize database
init_db()

# Schedule tasks
schedule.every(1).minutes.do(scrape_quotes)  # scrape every 1 minute
schedule.every(5).minutes.do(export_to_csv)  # export every 5 minutes

print("Scheduler started... (Press Ctrl+C to stop)")

while True:
    schedule.run_pending()
    time.sleep(1)
