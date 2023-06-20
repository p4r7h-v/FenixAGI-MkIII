import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a HTTP request to the URL of the webpage you want to access
    response = requests.get(url)

    # If the HTTP request has been successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        page_content = response.content

        # Create a BeautifulSoup object and specify the parser
        soup = BeautifulSoup(page_content, 'html.parser')

        # Empty list to hold scraped data
        scraped_data = []

        # Find elements you need - in this case, let's say we are finding 'p' elements
        elements = soup.find_all('p')
        
        # Iterate through each element of interest
        for element in elements:
            # Append the data to scraped_data list
            scraped_data.append(element.text)

        # Write data to a file
        with open('scraped_data.txt', 'w') as f:
            for item in scraped_data:
                f.write("%s\n" % item)

        print('Data scraped and saved successfully.')
    else:
        print('Failed to retrieve page.')

# Use the function
scrape_website('https://www.example.com')