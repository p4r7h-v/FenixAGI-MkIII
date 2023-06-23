import os
from termcolor import colored
import pandas as pd
import ast
import astor
import pathspec
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity
import json
import chardet
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
        url="https://a16z.com/2023/06/20/emerging-architectures-for-llm-applications",
    )
    print(data)
def write_to_file(file_path, content):
    print(colored(f"GPT Writing to file: {file_path}", "magenta"))
    try:
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(content)
        print(colored(f"Successfully wrote to file: {file_path}", "green"))
        return f"Successfully wrote to file: {file_path}"
    except Exception as e:
        print(colored(f"Error writing to file: {e}", "red"))
        return f"Error writing to file: {e}"
    
def read_from_file(file_path):
    print(colored(f"GPT Reading from file: {file_path}", "magenta"))
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
            content = f.read()
        print(colored(f"Successfully read from file: {file_path}", "green"))
        return f"Here are the contents of {file_path}:\n{content}"
    except Exception as e:
        print(colored(f"Error reading from file: {e}", "red"))
        return f"Error reading from file: {e}"
    
def delete_file(file_path):
    print(colored(f"GPT Deleting file: {file_path}", "magenta"))
    try:
        os.remove(file_path)
        print(colored(f"Successfully deleted file: {file_path}", "green"))
        return f"Successfully deleted file: {file_path}"
    except Exception as e:
        print(colored(f"Error deleting file: {e}", "red"))
        return f"Error deleting file: {e}"
    
def create_directory(directory_path):
    print(colored(f"GPT Creating directory: {directory_path}", "magenta"))
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        print(colored(f"Successfully created directory: {directory_path}", "green"))
        return f"Successfully created directory: {directory_path}"
    except Exception as e:
        print(colored(f"Error creating directory: {e}", "red"))
        return f"Error creating directory: {e}"
        
def ask_user_for_additional_information(question_for_additional_information):
    user_provided_additional_information = ''
    print(colored("\nThe following a multiline input, you can put as much detail as you want in here. write 'done' in a newline and press enter", "green"))
    print(colored("\nGPT: Please provide additional information for the following question:", "green"))
    print(colored(f"\n{question_for_additional_information}", "yellow"))
    while True:
        line = input()
        if line.strip().lower() == 'done':
            break
        user_provided_additional_information += line + '\n'

    return user_provided_additional_information

def done(done=""):
    return "done"

