import json
import requests
import sqlite3  # Import SQLite library
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import os

url = "https://www.wholefoodsmarket.com/sales-flyer?store-id=10709"

# Set up the Selenium WebDriver (e.g., Chrome)
driver_path = "/usr/bin/chromedriver"  # Specify the path to your ChromeDriver
service = Service(driver_path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)  # Make sure the ChromeDriver is in your PATH
driver.get(url)

# Wait for the page to load completely
time.sleep(5)  # Adjust the sleep time as needed

# Get the page source and parse it with BeautifulSoup
page_source = driver.page_source
whole_soup = BeautifulSoup(page_source, "html.parser")

# Close the WebDriver
driver.quit()

# Scrape item names
item_names = whole_soup.select('span.bds--heading-5.pb-1.text-squid-ink, span[data-testid="clickable-hero-name"], span[data-testid="clickable-subhero-name"], a[data-testid="clickable-hero-name"], a[data-testid="clickable-subhero-name"]')

# Find all 'span' tags with the class 'bds--heading-4.items-center.bg-citron.px-1' for item prices
item_discounts = whole_soup.select('span.bds--heading-4.items-center.bg-citron.px-1')

# Print the number of items and discounts scraped
print(f"Number of items scraped: {len(item_names)}")
print(f"Number of discounts scraped: {len(item_discounts)}")

# Check if the number of item names matches the number of item discounts
if len(item_names) != len(item_discounts):
    print("The number of item names and discounts do not match.")
else:
    # Store the scraped content in a list of dictionaries
    scraped_items = [{"name": name.text.strip(), "discount": discount.text.strip()} for name, discount in zip(item_names, item_discounts)]

    # Print the scraped content to the console
    for item in scraped_items:
        print(item)

    # Save the scraped items to a JSON file, replacing any previous items
    with open('scraped_items.json', 'w') as file:
        json.dump(scraped_items, file, indent=4)

    # Connect to the SQLite database (or create it if it doesn't exist)
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'whole_foods.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraped_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            discount TEXT NOT NULL
        )
    ''')

    # Clear the table before inserting new items
    cursor.execute('DELETE FROM scraped_items')

    # Insert the new items into the database
    cursor.executemany('INSERT INTO scraped_items (name, discount) VALUES (?, ?)', [(item['name'], item['discount']) for item in scraped_items])

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    # Send data to Flask server
    response = requests.post('http://127.0.0.1:5555/scraped_items', json=scraped_items)

    # Print server response
    try:
        print(response.json())
    except requests.exceptions.JSONDecodeError:
        print("Response content is not in JSON format:")
        print(response.text)