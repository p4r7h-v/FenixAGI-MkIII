import os
from termcolor import colored
import colorcet as cc
import numpy as np
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
import markdown
from sklearn.manifold import TSNE
import plotly.express as px
import plotly.io as pio
import plotly.graph_objs as go
import keyboard



def get_folder_hierarchy(folder_path):
    if not os.path.exists(folder_path):
        folder_path = '.'
    gitignore_path = os.path.join(folder_path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as gitignore_file:
            gitignore = gitignore_file.read()
        spec = pathspec.PathSpec.from_lines(pathspec.patterns.GitWildMatchPattern, gitignore.splitlines())

    def get_folder_contents(folder_path, level):
        indent = "  " * level
        hierarchy = ""
        for item in sorted(os.listdir(folder_path)):
            item_path = os.path.join(folder_path, item)
            if os.path.exists(gitignore_path) and spec.match_file(os.path.relpath(item_path, folder_path)):
                continue
            if os.path.isdir(item_path):
                hierarchy += f"{indent}- {item}/\n"
                hierarchy += get_folder_contents(item_path, level + 1)
            else:
                hierarchy += f"{indent}- {item}\n"
        return hierarchy

    hierarchy = "# Folder Hierarchy\n\n"
    hierarchy += get_folder_contents(folder_path, 0)
    return hierarchy


def create_markdown_file(file_name, content):
    # if the file_path doesn't exist save to "content" folder
    if not os.path.exists(file_name):
        file_path = "./content/"+file_name
    # Now you can safely write your file
    with open(file_path, 'w') as file:
        file.write(content)
    return f"Successfully created file: {file_path}"



def bing_search_save(file_name, query):
    subscription_key = os.getenv("BING_SEARCH_KEY")
    base_url = "https://api.bing.microsoft.com/v7.0/search"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": query, "count": 50, "offset": 0, "freshness": "Month"}
    file_path = "./web_searches/"+file_name
    response = requests.get(base_url, headers=headers, params=params)
    # if 401, then return error
    if response.status_code == 401:
        return "Error: Invalid Bing Search Key"
    
    response.raise_for_status()
    search_results = response.json()

    folder_path = "."+os.path.dirname(file_path)

    if not os.path.exists(folder_path):
        try:
            os.makedirs(folder_path)
        except OSError as e:
            return f"Error creating directory: {str(e)}"

    with open(file_path, 'w', encoding='utf-8') as file:

        if 'webPages' in search_results:
            for result in search_results["webPages"]["value"]:
                file.write(f"- [{result['name']}]({result['url']})\n")
        else:
            print("'webPages' not in search results")
    return f"Response saved to: {file_path}, {len(search_results['webPages']['value'])} results found. Content: {search_results['webPages']['value']}"


def create_code_search_csv(folder_name):
    root_folder = os.path.join(os.getcwd(), folder_name)

    if not os.path.exists(root_folder):
        os.makedirs(root_folder)

    code_search_file = os.path.join(root_folder, "code_search.csv")

    with open('.gitignore', 'r') as f:
        gitignore = f.read()
    gitignore_spec = pathspec.PathSpec.from_lines(
        pathspec.patterns.GitWildMatchPattern, gitignore.splitlines())

    if os.path.exists(code_search_file):
        df = pd.read_csv(code_search_file)
        df['code_embedding'] = df['code_embedding'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
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
            df['code_embedding'] = df['code'].apply(
                lambda x: get_embedding(x, engine='text-embedding-ada-002'))
            df['filepath'] = df['filepath'].apply(
                lambda x: x.replace(folder_name, ""))
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
            print(colored(
                f"{r[1].function_name} ({r[1].filepath}): score={round(r[1].similarities, 3)}", 'green'))
            # print(r[1].code)
            print(colored('-'*70, 'yellow'))
            results.append({
                "function_name": r[1].function_name,
                "filepath": r[1].filepath,
                "score": round(r[1].similarities, 3),
                "code": r[1].code,
            })
    return json.dumps(results)


def visualize_data_3d(code_search_csv_path):
    print("Visualizing data in 3D...")
    if not os.path.exists(code_search_csv_path):
        print("Code search csv file does not exist. Setting default path.")
        code_search_csv_path = "./code_search.csv"
    df = pd.read_csv(code_search_csv_path)
    print("Total number of functions:", len(df))
    print("Total number of unique files:", len(df['filepath'].unique()))
    print("Total number of unique functions:",
          len(df['function_name'].unique()))
    print("Total number of unique code embeddings:",
          len(df['code_embedding'].unique()))
    embeddings = [ast.literal_eval(i) for i in df['code_embedding'].tolist()]
    embeddings_array = np.array(embeddings)
    function_names = df['function_name'].tolist()
    filepaths = df['filepath'].tolist()

    tsne = TSNE(n_components=3, random_state=42,
                perplexity=len(embeddings_array)-1)
    embeddings_array = np.array(embeddings)
    reduced_embeddings = tsne.fit_transform(embeddings_array)

    vis_df = pd.DataFrame(reduced_embeddings, columns=['x', 'y', 'z'])
    vis_df['function_name'] = function_names
    vis_df['filepath'] = filepaths

    unique_filepaths = list(vis_df['filepath'].unique())
    colors = cc.palette['glasbey_dark']
    num_colors = len(colors)

    plot_markers = []
    for idx, filepath in enumerate(unique_filepaths):
        temp_df = vis_df[vis_df['filepath'] == filepath]
        color_idx = idx % num_colors  # cycle through colors using modulo operator
        marker = go.Scatter3d(x=temp_df['x'],
                              y=temp_df['y'],
                              z=temp_df['z'],
                              mode='markers+text',
                              text=temp_df['function_name'],
                              name=filepath,
                              textposition='top center',
                              hovertext=temp_df['filepath'],
                              hoverinfo='text',
                              marker={'color': colors[color_idx], 'symbol': 'circle', 'size': 8})
        plot_markers.append(marker)

    layout = go.Layout(title='Code Visualization',
                       scene=dict(xaxis_title='X', yaxis_title='Y',
                                  zaxis_title='Z'),
                       showlegend=False,
                       hovermode='closest',
                       margin={'t': 50, 'b': 50, 'l': 50, 'r': 50},
                       legend=dict(orientation="h", yanchor="bottom",
                                   y=1.02, xanchor="right", x=1, title="Filepaths"),
                       template='plotly_dark')

    fig = go.Figure(data=plot_markers, layout=layout)

    fig.show()
    return "The visualization is ready."


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


def suggest_function_chain(task, available_functions):
    """Suggest a chain of functions to accomplish a task"""

    # Generate messages including the task and available functions
    messages = [
        {"role": "system", "content": f'You are given a task and a list of available functions. Your task is to develop a chain of functions to accomplish the task. The task is: {task}.'},
        {"role": "user", "content": 'User: Using only the available functions: ' +
            available_functions + ', develop a chain of functions to accomplish the task.'},
        {"role": "assistant", "content": 'Assistant:'},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
        max_tokens=100,
        n=1,
        stop=None
    )
    print(response.choices[0].message["content"])
    suggested_functions = response.choices[0].message["content"]

    return suggested_functions


def list_files_in_directory(directory_path):
    files = []
    for file in os.listdir(directory_path):
        if os.path.isfile(os.path.join(directory_path, file)):
            files.append(file)
    return files


def write_file(file_path, content):
    print(colored(f"GPT Writing to file: {file_path}", "magenta"))
    try:
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(content)
        print(colored(f"Successfully wrote to file: {file_path}", "green"))
        return f"Successfully wrote to file: {file_path}"
    except Exception as e:
        print(colored(f"Error writing to file: {e}", "red"))
        return f"Error writing to file: {e}"


def read_file(file_path):
    # print(colored(f"GPT Reading from file: {file_path}", "magenta"))
    try:
        with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
            # if file is an image then skip it
            if file_path.endswith(".png") or file_path.endswith(".jpg") or file_path.endswith(".jpeg"):
                return
            else:
                content = f.read()
        # print(colored(f"Successfully read from file: {file_path}", "green"))
        return f"Here are the contents of {file_path}:\n{content}"
    except Exception as e:
        print(colored(f"Error reading from file: {e}", "red"))
        return f"Error reading from file: {e}"


def move_file(source_path, destination_path):
    try:
        os.rename(source_path, destination_path)
        return f"1 File moved: {source_path} to {destination_path}."
    except Exception as e:
        return f"Error moving file: {e}"


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
        print(
            colored(f"Successfully created directory: {directory_path}", "green"))
        return f"Successfully created directory: {directory_path}"
    except Exception as e:
        print(colored(f"Error creating directory: {e}", "red"))
        return f"Error creating directory: {e}"


def ask_user_for_additional_information(question_for_additional_information):
    user_provided_additional_information = ''
    print(colored("\nThe following a multiline input, you can put as much detail as you want in here. write 'done' in a newline and press enter", "green"))
    print(colored(
        "\nGPT: Please provide additional information for the following question:", "green"))
    print(colored(f"\n{question_for_additional_information}", "yellow"))
    while True:
        line = input()
        if line.strip().lower() == 'done':
            break
        user_provided_additional_information += line + '\n'

    return user_provided_additional_information


def count_tokens_in_string(text, model_name="gpt-3.5-turbo-16k-0613"):
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))


def count_tokens_in_file(file_path, model_name="gpt-3.5-turbo-16k-0613"):
    encoding = tiktoken.encoding_for_model(model_name)
    with open(file_path, 'r', encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return len(encoding.encode(content))
