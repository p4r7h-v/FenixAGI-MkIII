import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def check_broken_links(url):
    broken_links = []
    parsed_base_url = urlparse(url)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.RequestException as e:
        print(f"Error: {str(e)}")
        return broken_links

    page_content = response.content
    soup = BeautifulSoup(page_content, "html.parser")
    for link_tag in soup.find_all("a"):
        href = link_tag.attrs.get("href")
        if href == "" or href is None:
            continue

        href = urljoin(url, href)
        parsed_href = urlparse(href)
        if parsed_href.netloc != parsed_base_url.netloc:
            continue

        try:
            sub_response = requests.head(href, headers=headers)
            if sub_response.status_code >= 400:
                broken_links.append(href)
        except requests.exceptions.RequestException as e:
            print(f"Error: {str(e)}")
            broken_links.append(href)

    return broken_links

# URL to check for broken links
url = "https://your-website-url.com"

broken_links = check_broken_links(url)
if not broken_links:
    print("No broken links found!")
else:
    print("Broken links found:")
    for link in broken_links:
        print(link)