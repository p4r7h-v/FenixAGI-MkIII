from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

url = "https://www.parth.club"  # Make sure to include 'http://' or 'https://' in the URL

def open_website(url):
    # Initialize the webdriver       
    driver = webdriver.Edge()  # You can specify the path to the webdriver here if needed

    # Open the website
    driver.get(url)


    # Get User input
    input("Enter User details to continue...")
    
    # Find an element by its tag name (returns the first match)
    first_product = driver.find_element(By.CLASS_NAME,'product-card__title')
    first_product.price = driver.find_element(By.CLASS_NAME,'product-card__price')
    # Print the text inside this element
    print(first_product.text)
    print(first_product.price.text)

    # Find elements by class name (returns a list of matching elements)
    divs = driver.find_elements(By.CLASS_NAME,'product-card__title')
    divs_price = driver.find_elements(By.CLASS_NAME,'product-card__price')

    # Loop through the list and print the text inside each div
    for div in divs:
        print(div.text)
    for div in divs_price:
        print(div.text)
    # Close the browser
    driver.quit()
# Call the function to open the website
open_website(url)
