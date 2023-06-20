import requests
from bs4 import BeautifulSoup

def scrape_website(url, target_tag):
    try:
        # Access the website
        response = requests.get(url)
        response.raise_for_status()

        # Fetch and parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        tags = soup.find_all(target_tag)

        # Extract and print the data
        data = [tag.get_text() for tag in tags]
        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while accessing the website: {e}")
        return None

# Example usage:
url = "https://docs.langchain.com/docs/"
target_tag = "p"
data = scrape_website(url, target_tag)
print(data)