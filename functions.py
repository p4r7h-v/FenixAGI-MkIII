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
import tiktoken
import openai


def create_markdown_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

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

def create_code_search_csv(folder_name):
    root_folder = os.path.join(os.getcwd(), folder_name)

    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    code_search_file = os.path.join(root_folder, "code_search.csv")

    with open('.gitignore', 'r') as f:
        gitignore = f.read()
    gitignore_spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignore.splitlines())

    if os.path.exists(code_search_file):
        df = pd.read_csv(code_search_file)
        df['code_embedding'] = df['code_embedding'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    else:
        code_files = []
        for root, dirs, files in os.walk(folder_name):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    if not gitignore_spec.match_file(file_path):
                        code_files.append(file_path)

        print("Total number of py files:", len(code_files))

        if len(code_files) == 0:
            print("No files detected.")

        all_funcs = []
        for code_file in code_files:
            funcs = list(get_functions(code_file))
            for func in funcs:
                all_funcs.append(func)

        print("Total number of functions extracted:", len(all_funcs))

        df = pd.DataFrame(all_funcs)

        if df.empty:
            print("Warning: No functions found in the code files.")
        else:
            df['code_embedding'] = df['code'].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))
            df['filepath'] = df['filepath'].apply(lambda x: x.replace(folder_name, ""))
            df.to_csv(code_search_file, index=False)
            print("Code Search Online.")
    return df


# Function to get functions from code_file
def get_functions(filepath):
    with open(filepath, 'rb') as f:
        file_content = f.read()
        result = chardet.detect(file_content)
    encoding = result['encoding'] or 'utf-8'
    whole_code = file_content.decode(
        encoding, errors='ignore').replace("\r", "\n")

    try:
        tree = ast.parse(whole_code)
    except SyntaxError:
        # skip files with syntax errors
        return

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_name = node.name
            code = astor.to_source(node)
            yield {"code": code, "function_name": function_name, "filepath": filepath}

# Similarity search code
def similarity_search(df, code_query, n=3, pprint=True, n_lines=7):
    embedding = get_embedding(code_query, engine='text-embedding-ada-002')
    df['similarities'] = df.code_embedding.apply(
        lambda x: cosine_similarity(ast.literal_eval(x) if isinstance(x, str) else x, embedding))
    
    res = df.sort_values('similarities', ascending=False).head(n)
    if pprint:
        for r in res.iterrows():
            print(r[1].filepath+":"+r[1].function_name +
                  "  score=" + str(round(r[1].similarities, 3)))
            print("\n".join(r[1].code.split("\n")[:n_lines]))
            print('-'*70)
    return res

def search_codebase(code_query, n):
    df = create_code_search_csv('.')
    print('Searching functions...')
    res = similarity_search(df, code_query, n=n, pprint=False)

    if res is not None:
        print(colored("Search Results", 'yellow'))
        results = []
        for r in res.iterrows():
            print(colored(f"{r[1].function_name} ({r[1].filepath}): score={round(r[1].similarities, 3)}", 'green'))
            #print(r[1].code)
            print(colored('-'*70, 'yellow'))
            results.append({
                "function_name": r[1].function_name,
                "filepath": r[1].filepath,
                "score": round(r[1].similarities, 3),
                "code": r[1].code,
                })
    return json.dumps(results)

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

def count_tokens_in_string(text, model_name="gpt-3.5-turbo-16k-0613"):
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))

def count_tokens_in_file(file_path, model_name="gpt-3.5-turbo-16k-0613"):
    encoding = tiktoken.encoding_for_model(model_name)
    with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return len(encoding.encode(content))

