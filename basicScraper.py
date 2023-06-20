import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    """Scrape a website and return the data"""
    target_tag = "p"
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

if __name__ == "__main__":
    # Scrape the website
    data = scrape_website(
        url="https://en.wikipedia.org/wiki/Python_(programming_language)",
        target_tag="p",
    )
    print(data)