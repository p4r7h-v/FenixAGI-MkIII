from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def automate_web_browser(url, search_term=None):
    try:
        # Make sure to download and mention the correct path for your browser's webdriver. Replace 'chromedriver.exe' accordingly.
        driver = webdriver.Chrome(executable_path='./chromedriver.exe')

        # Open the website with the provided URL
        driver.get(url)

        # If a search term is provided, search on the website
        if search_term:
            # Locate the search bar on the website (this may change depending on the website)
            search_bar = driver.find_element_by_name("q")

            # Clear the search bar, type the search term and press Enter
            search_bar.clear()
            search_bar.send_keys(search_term)
            search_bar.send_keys(Keys.RETURN)

            # Wait for the search results to load
            time.sleep(3)

            # Print the search results' titles and URLs
            search_results = driver.find_elements_by_css_selector(".g a h3")
            for result in search_results:
                print(result.text)
                print(result.find_element_by_xpath("./..").get_attribute("href"))
                print()

        # Pause for demonstration purposes
        time.sleep(5)

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Close the webdriver
        driver.quit()

# Usage example
automate_web_browser("https://www.google.com", "python programming")