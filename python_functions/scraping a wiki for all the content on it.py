import requests
from bs4 import BeautifulSoup

def scrape_wiki(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    for each in soup.find_all('p'): # 'p' tags are for paragraphs
        print(each.get_text())

# Use function like this:
# scrape_wiki("https://en.wikipedia.org/wiki/Python_(programming_language)")