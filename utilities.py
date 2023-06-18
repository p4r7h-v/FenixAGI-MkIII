import json
from termcolor import colored
import re
import os

def sanitize_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', "", filename)
    return filename[:100]  # limit filename length

def write_functions_from_json_to_files():
    # extract code from betweeen ```python and ``` using regex
    with open('async.json', errors="ignore") as f:
        data = json.load(f)
        for item in data:
            for key, value in item.items():
                if key == "code":
                    try:
                        match = re.findall(r"```python(.*?)```", value, re.DOTALL)
                        code = match[0].strip()
                        file_name = sanitize_filename(f"{item['purpose']}.py")
                        file_path = os.path.join('python_functions', file_name)
                        file_path = sanitize_filename(file_path)
                        # check if pyton_functions directory exists
                        if not os.path.exists('python_functions'):
                            os.makedirs('python_functions')
                        if os.path.exists(file_path):
                            i = 1
                            while os.path.exists(os.path.join('python_functions', f"{item['purpose']}_{i}.py")):
                                i += 1
                            file_path = os.path.join('python_functions', f"{item['purpose']}_{i}.py")
                        with open(file_path, "w") as f:
                            try:
                                f.write(code)
                            except UnicodeEncodeError:
                                print(colored(f"Error writing code to {item['purpose']}", "red"))
                                continue
                    except IndexError:
                        print(colored(f"Error extracting code from {item['purpose']}", "red"))
                        continue

write_functions_from_json_to_files()

# create a search over file names of python_functions directory .implement lowercase search. take user input
import os

def search_python_functions():
    while True:
        query = input("Enter a search query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        files = []
        for file in os.listdir('python_functions'):
            if query.lower() in file.lower():
                files.append(file)
        if len(files) == 0:
            print("No files found")
            continue
        print("Files found:")
        for i, file in enumerate(files):
            print(f"{i+1}. {file}")
        while True:
            try:
                choice = int(input("Enter the number of the file you want to save to temp.py (or '0' to perform a new search): "))
                if choice < 0 or choice > len(files):
                    raise ValueError
                if choice == 0:
                    break
                file = files[choice-1]
                with open(os.path.join('python_functions', file)) as f:
                    # write the contents of the file to temp.py
                    with open('temp.py', 'w') as temp:
                        temp.write(f.read())
                print(f"File {file} has been saved to temp.py")
                break
            except ValueError:
                print("Invalid choice. Please enter a number between 1 and", len(files), "or '0' to perform a new search.")


search_python_functions()
