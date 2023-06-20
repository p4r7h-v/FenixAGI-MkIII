import os
import requests
import json

def bing_search_save(query):
    subscription_key = os.getenv("BING_SEARCH_KEY")

    base_url = "https://api.bing.microsoft.com/v7.0/search"
    
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": query, "count": 50, "offset": 0}
    
    response = requests.get(base_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    links = []
    with open('bing_search_results.txt', 'w') as file:
        for result in search_results["webPages"]["value"]:
            file.write(result["url"] + "\n")
            links.append(result["url"])
    return links
    

# Execute function with a search query
bing_search_save("langchain")
