import requests
import json

def search_google(query, api_key, cx_key):
    api_key = "AIzaSyD0V-Y3NcDaOtsbGEbFmL5XUnjN9_F9ivk"
    URL = f"https://www.googleapis.com/customsearch/v1"
    PARAMETERS = {'q':query, 'key':api_key, 'cx':cx_key}

    response = requests.get(URL, params=PARAMETERS)
    response_json = response.json()

    # Save the results to a JSON file
    with open('results.json', 'w') as outfile:
        json.dump(response_json, outfile)

    print("Results are saved in results.json")