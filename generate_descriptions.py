import os
import fnmatch
import tenacity
import openai

def read_gitignore():
    """
    This function reads the .gitignore file and returns a list of files/directories to ignore.
    """
    ignore_list = []
    if os.path.isfile('.gitignore'):
        with open('.gitignore', 'r') as file:
            ignore_list = file.read().splitlines()
    return ignore_list

@tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_fixed(2))
def call_chat_model(role_content, filename):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": role_content}
        ],
        max_tokens=500
    )

    # Get the generated description from the response
    description = response['choices'][0]['message']['content'].strip()
    print(f"Role content: {role_content}")  # New debug print statement
    print(f"Generated description for {filename}: {description}")  # New debug print statement
    return description

def generate_description(filename, content, is_dir=False, dir_summary=None):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    if is_dir:
        role_content = f"Based on the following summaries of its files, please describe the purpose of this directory named {filename}: {dir_summary}"
    else:
        role_content = f"Please describe the content of this file named {filename} which contains the following text: {content}"

    # Call the chat model API
    description = call_chat_model(role_content, filename)
    return description

def main():
    ignore_list = ['env']
    ignore_list = [os.path.normpath(path) for path in ignore_list]
    # set folder to user input
    folder_name = input("Enter the folder path: ")
    file_patterns = ["*.svelte"]
    folder_name = os.path.normpath(folder_name)

    file_descriptions = {}
    # recursively walk through the folder and generate descriptions for each file
    for root, dirs, files in os.walk(folder_name):
        dirs[:] = [d for d in dirs if d not in ignore_list]
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.isfile(filepath) and any(fnmatch.fnmatch(filename, pattern) for pattern in file_patterns):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    try:
                        description = generate_description(filename, content, is_dir=False)
                        file_descriptions[filepath] = description
                    except Exception as e:
                        print(f"Error generating description for {filename}: {e}")
        
    directory_descriptions = {}
    for dirname in os.listdir(folder_name):
        dirpath = os.path.join(folder_name, dirname)
        if os.path.isdir(dirpath) and not any(ignore in dirpath for ignore in ignore_list):
            dir_file_descriptions = [desc for path, desc in file_descriptions.items() if dirpath in path]
            dir_summary = ' '.join(dir_file_descriptions)
            try:
                description = generate_description(dirname, "", is_dir=True, dir_summary=dir_summary)
                directory_descriptions[dirpath] = description
            except Exception as e:
                print(f"Error generating description for directory {dirname}: {e}")

    with open(os.path.join(folder_name, 'folder_desc.txt'), 'w', encoding='utf-8') as f:
        for dirpath, description in directory_descriptions.items():
            print(f"Directory: {dirpath}\nDescription: {description}\n")
            f.write(f"Directory: {dirpath}\nDescription: {description}\n\n")

        for filepath, description in file_descriptions.items():
            print(f"File: {filepath}\nDescription: {description}\n")
            f.write(f"File: {filepath}\nDescription: {description}\n\n")

if __name__ == "__main__":
    main()
