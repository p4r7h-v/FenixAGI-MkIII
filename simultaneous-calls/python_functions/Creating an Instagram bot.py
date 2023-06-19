from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def instagram_bot(username, password):
    url = 'https://www.instagram.com/'
    chrome_driver_path = './chromedriver'  # Replace this with the path to the downloaded Chrome WebDriver

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
      
    # Go to Instagram's URL
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    # Find username and password input fields and enter the credentials
    username_input = driver.find_element_by_name("username")
    password_input = driver.find_element_by_name("password")

    username_input.send_keys(username)
    password_input.send_keys(password)

    # Press Enter key to submit the login form
    password_input.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for successful login
    
    # Close the notification pop-up if it appears
    try:
        not_now_btn = driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")
        not_now_btn.click()
    except Exception:
        pass
    
    print("Logged in to Instagram successfully!")

# Usage example:
username = 'your_username'  # Replace with your Instagram username
password = 'your_password'  # Replace with your Instagram password

instagram_bot(username, password)