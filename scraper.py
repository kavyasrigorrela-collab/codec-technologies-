# scraper.py
import requests
from bs4 import BeautifulSoup
import sqlite3
import csv
import os

DB_FILE = "database.db"

# Create table if not exists
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT,
            author TEXT
        )
    """)
    conn.commit()
    conn.close()

# Scrape function
def scrape_quotes():
    url = "http://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    quotes = []
    for quote in soup.find_all("span", class_="text"):
        text = quote.get_text()
        author = quote.find_next("small", class_="author").get_text()
        quotes.append((text, author))

    # Save to DB
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    for text, author in quotes:
        c.execute("INSERT INTO quotes (text, author) VALUES (?, ?)", (text, author))
    conn.commit()
    conn.close()

    print(f"✅ Scraped and saved {len(quotes)} quotes.")

# Export to CSV
def export_to_csv(csv_file="quotes.csv"):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM quotes")
    rows = c.fetchall()
    conn.close()

    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Text", "Author"])
        writer.writerows(rows)
    print(f"📁 Data exported to {csv_file}")

# Run once for testing
if __name__ == "_main_":
    init_db()
    scrape_quotes()
    export_to_csv()