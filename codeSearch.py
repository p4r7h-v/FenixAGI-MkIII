import os
import pandas as pd
import ast
import astor
import chardet
from termcolor import colored
import pathspec
from openai.embeddings_utils import get_embedding
from openai.embeddings_utils import cosine_similarity
import json



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
        #print(f"Before conversion: {type(df['code_embedding'].iloc[0])}")  # Add this line
        df['code_embedding'] = df['code_embedding'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        #print(f"After conversion: {type(df['code_embedding'].iloc[0])}")  # And this line
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



def interactive_code_search(df, n):
    while True:
        code_query = input("Code Search (type 'exit' to quit): ")   
        if code_query.lower() == 'exit':
            break

        print('Searching functions...')
        res = similarity_search(df, code_query, n=n, pprint=False)

        if res is not None:
            print(colored("Search Results", 'yellow'))
            results = []
            for r in res.iterrows():
                print(colored(f"{r[1].function_name} ({r[1].filepath}): score={round(r[1].similarities, 3)}", 'green'))
                print(r[1].code)
                print(colored('-'*70, 'yellow'))
                results.append({
                    "function_name": r[1].function_name,
                    "filepath": r[1].filepath,
                    "score": round(r[1].similarities, 3),
                    "code": r[1].code,
                })
    return results

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

if __name__ == "__main__":
    df = create_code_search_csv('.')
    interactive_code_search(df,3)
