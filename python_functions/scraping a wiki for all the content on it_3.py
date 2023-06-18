import requests
from bs4 import BeautifulSoup

def scrape_wiki(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    for p in soup.find_all('p'):
        print(p.get_text())

# Example usage:
# scrape_wiki('https://en.wikipedia.org/wiki/Web_scraping')