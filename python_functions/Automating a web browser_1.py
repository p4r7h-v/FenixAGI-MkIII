from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def automate_browser(url):
    # Initialize the web browser
    browser = webdriver.Chrome()

    # Open the given URL
    browser.get(url)

    # Find the search box element (assuming it's Google)
    search_box = browser.find_element_by_name("q")

    # Send keys to the search box
    search_box.send_keys("Automation with Python and Selenium")
    search_box.send_keys(Keys.RETURN)

    # Wait for the results to load
    time.sleep(5)

    # Close the browser
    browser.quit()

# Usage Example:
automate_browser("https://www.google.com")