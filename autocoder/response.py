import os
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

def generate_description(filename, content, is_dir=False, dir_summary=None):
    """
    This function takes a filename and its content as inputs and returns a description using the GPT API call
    """
    # Your OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key

    # Construct a prompt based on whether the target is a file or directory
    if is_dir:
        role_content = f"Based on the following summaries of its files, please describe the purpose of this directory named {filename}: {dir_summary}"
    else:
        role_content = f"Please describe the content of this file named {filename} which contains the following text: {content}"

    # Make a chat model API call with the given prompt
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
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


def main():
    # Manually set the ignore_list to only contain the env/ folder
    ignore_list = ['env']

    # Normalize paths in ignore_list
    ignore_list = [os.path.normpath(path) for path in ignore_list]

    # Walk the directory and generate descriptions for each file
    file_descriptions = {}
    for root, dirs, files in os.walk("."):
        root = os.path.normpath(root)
        for filename in files:
            filepath = os.path.join(root, filename)
            filepath = os.path.normpath(filepath)
            if not any(ignore in filepath for ignore in ignore_list) and filename.endswith((".txt", ".py")):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                try:
                    description = generate_description(filename, content, is_dir=False)
                    file_descriptions[filepath] = description
                except Exception as e:
                    print(f"Error generating description for {filename}: {e}")

    # Walk the directory again and generate descriptions for each directory based on the file descriptions
    directory_descriptions = {}
    for root, dirs, _ in os.walk("."):
        root = os.path.normpath(root)
        for dirname in dirs:
            dirpath = os.path.join(root, dirname)
            dirpath = os.path.normpath(dirpath)
            if not any(ignore in dirpath for ignore in ignore_list):
                dir_file_descriptions = [desc for path, desc in file_descriptions.items() if dirpath in path]
                dir_summary = ' '.join(dir_file_descriptions)
                try:
                    description = generate_description(dirname, "", is_dir=True, dir_summary=dir_summary)
                    directory_descriptions[dirpath] = description
                except Exception as e:
                    print(f"Error generating description for directory {dirname}: {e}")
    
    # Print and write the descriptions
    with open('output.txt', 'w') as f:
        for filepath, description in file_descriptions.items():
            print(f"File: {filepath}\nDescription: {description}\n")
            f.write(f"File: {filepath}\nDescription: {description}\n")

        for dirpath, description in directory_descriptions.items():
            print(f"Directory: {dirpath}\nDescription: {description}\n")
            f.write(f"Directory: {dirpath}\nDescription: {description}\n")

if __name__ == "__main__":
    main()