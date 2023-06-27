import openai
import os
import json
from functions import function_descriptions, write_file, read_file, delete_file
from termcolor import colored
import re



project_folder = "project"
if not os.path.exists(project_folder):    
    os.mkdir(project_folder)
os.chdir(project_folder)



instructor_system_message = """You are a helpful detail oriented programmer assistant AI bot who generates bullet point instructions and guidance and a list of operations for a full programming applications to be given to another bot who will be writing fullfilling the list of operations and the bullet point guidance which is provided buy you. You only have access to three operations: write, read, delete.

Your goal is to examine the user input however basic or vague it maybe and generate a list of operations and detailed bullet point guidance for the next bot to follow for a full fledged programming application. 

generate detailed bullet points of guidance on what features might be needed for the application and what the user might want to do with the application. giv

User might add neew instructions to the end of current instructions. if there are any new instructions pay closer attention to those wihle still considering earlier instructions.

example user input:

a website for real estate.

example bullet point guidance:

1. Design: Make the site easy to use and nice to look at.
2. Listings: Show important details about each property.
3. Search: Allow users to search for and filter properties.
4. Accounts: Let users create accounts to save favorites and get alerts.
5. Map: Show property locations on a map.
6. Contact: Allow users to easily contact property owners or agents.
7. Submission: Let owners or agents add new property listings.
8. Reviews: Enable rating and reviewing of properties and agents.
9. Blog: Include a section for related articles.
10. Speed: Ensure the website loads quickly.

example list of operations:

["write", "index.html", "write", "style.css", "write", "script.js"]

"""

instructor_function_description = {
    "name": "instructor_function_description",
    "description": "This function will return a list of instructions for file system operations for a bot which applies the operations.",
    "parameters": {
        "type": "object",
        "properties": {
            "guidance": {
                "type": "string",
                "description": "The guidance for the next robot when applying the operations.",
            },
            "list of operations": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "operation": {
                            "type": "string",
                            "description": "The type of operation to be applied. can be one of the following: write delete",
                            "enum": ["write", "delete"],
                        },
                        "filename": {
                            "type": "string",
                            "description": "The name of the file to apply the operation to."
                        },
                    },
                    "required": ["operation", "filename"]
                },
            }
        },
        "required": ["guidance", "list of operations"],
    },
}

list_of_operations = []
cumulative_user_input = ""
second_user_input = ""
while True:
    all_files = os.listdir(os.getcwd())

    # single line user input
    # user_input = input("What program would you like to design? : ")

    # multi line user input
    user_input = ""
    print("Enter your prompt (type 'done' on a new line and press 'enter' when finished):")
    while True:
        line = input().lower()
        if line == "done":
            break
        user_input += line + "\n"
    cumulative_user_input += "\n" + user_input + "\n\n"

    user_instructions = "user instructions in chronological order:\n"
    first_user_input = user_instructions + cumulative_user_input + "\n\n" + f"""Current files and contents of the files in the project folder:"""
    # iterate over each file in the project folder
    for file in all_files:
        # skip directories
        if not os.path.isfile(file):
            continue
        # use the read_file function to get the content of the file
        file_content = read_file(file)
        # append the filename and its content to the user_input
        #if file extension is an image 
        if re.search(r"\.(jpg|jpeg|png|gif|tiff|bmp)$", file):
            first_user_input += f"\nFile: {file}\n"
        else:
            first_user_input += f"\nFile: {file}\nContent: {file_content}\n"

    # print(user_input)


    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": instructor_system_message},
                {"role": "user", "content": first_user_input},
                ],
            temperature=0.3,
            functions=[instructor_function_description],
            function_call={"name": "instructor_function_description", "arguments": {"list of operations": ["write", "read", "delete"]}}
        )
        total_tokens = response["usage"]["total_tokens"]
        response_message = response["choices"][0]["message"]
        # print(response_message)

        function_call = response_message.get('function_call')
        

        arguments = json.loads(function_call['arguments'])

        guidance = arguments['guidance']
        list_of_operations = arguments['list of operations']

        print(colored(f"Guidance: {guidance}", "green"))
        print(colored(f"List of operations: {list_of_operations}", "green"))
    except Exception as e:
        print(e)

    # system message for the second bot
    worker_system_message = f"You are a programmer bot who writes code according to user input and guidance. Here are the general instructions from the instructor bot: \n\n{guidance}\n\nDon't use '`' in your code."

    # iterate over each operation
    for operation in list_of_operations:
        all_files = os.listdir(os.getcwd())
        
        second_user_input = first_user_input
        # iterate over each file in the project folder
        for file in all_files:               
            # skip directories
            if not os.path.isfile(file):
                continue
            # use the read_file function to get the content of the file
            file_content = read_file(file)
            # append the filename and its content to the user_input
            second_user_input = cumulative_user_input + f"\nFile: {file}\nContent: {file_content}\n"
        function_name = operation['operation'] + "_file"  # get the correct function name
        filename = operation['filename']

        # find the function description for this operation
        function_description = next((f for f in function_descriptions if f["name"] == function_name), None)

        if function_description is None:
            print(f"Unknown operation: {function_name}")
            continue

        # make the API call to the second bot
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "system", "content": worker_system_message},
                    {"role": "user", "content": f"here are the current files and their contents: {second_user_input}.\n\nCurrently, you need to write content for the file {filename}. "}
                ],
                temperature=0.3,
                functions=[function_description],
                function_call={"name": function_name}
            )

            response_message = response["choices"][0]["message"]
            # print(response_message)

            function_call = response_message.get('function_call')

            def parse_args(function_args):
                # match content within backticks
                backtick_re = re.compile(r"`(.+?)`", re.DOTALL)

                # function to escape quotes and newlines in matched content
                def replace_special_chars(match):
                    text = match.group(1).replace('\n', '\\n').replace('"', '\\"')
                    # replace template literals `${}` with their escaped form ${{}}
                    text = re.sub(r"\$\{(.*?)\}", r"\$\{\{\1\}\}", text)
                    return f'"{text}"'

                # replace backticks and content within them with double quotes and escaped content
                function_args = backtick_re.sub(replace_special_chars, function_args)

                try:
                    # try to parse the function arguments
                    return json.loads(function_args)
                except json.JSONDecodeError as e:
                    print("Couldn't parse function arguments: ", function_args)
                    print("Error: ", str(e))
                    return None

            if function_call:
                function_name = function_call["name"]
                function_args = function_call.get("arguments")

                # use the function to parse the arguments
                function_args = parse_args(function_args)


                # Check if the function is in the global namespace
                if function_name in globals():
                    # Get the function from the global namespace
                    function_to_call = globals()[function_name]

                    # Check if the function arguments include a file path
                    if function_args.get("file_path"):
                        # Check if the file path includes a directory
                        if "/" in function_args["file_path"]:
                            # Check if the folder is "project_folder"
                            if not function_args["file_path"].startswith("project"):
                                print(f"You are trying to access a file outside of the project folder. Please try again.")
                                continue
                    # Call the function with the parsed arguments
                    function_to_call(**function_args)

                else:
                    print(f"Unknown function: {function_name}")

        except Exception as e:
            print(e)
