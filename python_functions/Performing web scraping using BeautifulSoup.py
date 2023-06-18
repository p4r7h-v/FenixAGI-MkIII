import requests
from bs4 import BeautifulSoup

def web_scraping(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        else:
            print(f"Error {response.status_code}: Unable to access the URL.")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

# Example usage:
url = "https://www.example.com"
soup = web_scraping(url)
if soup:
    print(soup.prettify())