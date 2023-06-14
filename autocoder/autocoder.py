import openai
import subprocess
import re
from termcolor import colored
import winsound
import sys

### ALWAYS BE CAREFUL WHEN AUTO EXECUTING AI GENERATED CODE ###

when_gpt_4 = 2 # after how many iterations should we use gpt-4

# read the existing code
with open('autocoder/content.py', 'r') as f:
    content = f.read()

# user instructions
user_input = ""
print(colored("Enter user instructions (write 'done' and then press 'enter' when done to continue):", 'blue'))
while True:
    line = input()
    if line.lower() == "done":
        break
    user_input += line + "\n"

def request_correction(content, user_input, previous_code, stdout, stderr, iteration):
    # print which iteration we are on
    print(colored(f"Iteration: {iteration}", 'red'))
    # decide which model to use based on iteration count
    if iteration % when_gpt_4 == 0:
        
        model = "gpt-4"
        print(colored("Using GPT-4 this turn", 'yellow'))
    else:
        print(colored("Using GPT-3.5-turbo this turn", 'yellow'))
        model = "gpt-3.5-turbo"


    if iteration == 1:  # first iteration
        message_content = f"""
        Your goal is to write python programs which follows the user instructions exceptionally carefully and create code which runs effectively and without any errors.
        When you run into errors, Always ry to Use print statements to print the error message where necessary to identify and understand the error so you can fix it.
        You will return the code as a single code block(markdown) always
        Do not include any regular text within your response. Only include code and comments and docstrings.
        always use a comment or docstring starting with a # or in between ''' and ''' to add your thoughts and strategy.


        content: 
        
        {content}

        User instructions:
        {user_input}
        """
    else:  # subsequent iterations
        message_content = f"""
        You are be provided code content(as "previous_content") that contains relevant code to the user instructions. Pay attention to the code content and use it effectively.
        You have previously written code based on the given content and user instructions, and you have access to the outputs as "stdout" and "stderr" to decide what to do next.
        Add your thoughts on what the error is and your strategy to fix it as a comment or a docstring. Never add it as regular text as it will throw an error.
        Do not include any regular text within your response. Only include code and comments and docstrings.
        always use a comment or docstring starting with a # or in between ''' and ''' to add your thoughts and strategy.


        code content: {content}

        User instructions:
        {user_input}

        Previous code:
        {previous_code}

        Stdout:
        {stdout}

        Stderr:
        {stderr}
        """

    response = openai.ChatCompletion.create(model=model, stream=True, messages=[
        {"role": "system", "content": """
        You are be provided code content(as content) that contains relevant code to the user instructions. Use the content effectively.
        Your goal is to create code based on user instructions which runs effectively and without any errors.
        When you run into errors, Always try to Use print statements to print the error message where necessary to identify and understand the error so you can fix it.
        take a look at the content for information on how to correctly write the code.
        You will return the code as a single code(markdown) block always
        if you want to add explanation to the code, always add it as a comment or a docstring. Never add it as regular text as it will throw an error.
        Do not include any regular text within your response outside of comments and docstrings. Only include code and comments and docstrings.
        always use a comment or docstring starting with a # or in between ''' and ''' to add your thoughts and strategy.
        in the beginning outline the strategy based on user instructions. 
        attention! : entire response should be valid python code
        """},
        {"role": "user", "content": message_content}])
    
    responses = ''
    # Extract the response text from the API response and write it to the file at the end
    with open('autocoder/response.py', 'w') as f:
        for chunk in response:
            if "role" in chunk["choices"][0]["delta"]:
                continue
            elif "content" in chunk["choices"][0]["delta"]:
                r_text = chunk["choices"][0]["delta"]["content"]
                responses += r_text
                print(r_text, end='', flush=True)

                    
        # Remove the code block formatting from the response
        response_text = re.sub(r"```python", "", responses)
        response_text = re.sub(r"```", "", response_text)

        # Write the response to the "autocoder/response.py" file
        f.write(response_text)

    
    # run the generated Python code and capture output and error
    # Capture stdout and stderr separately
    # sys.exit()
    result = subprocess.run(['python', 'autocoder/response.py'], capture_output=True, text=True)
    print("STDOUT:")
    print(result.stdout)
    print("STDERR:")
    print(result.stderr)


    # if there is an error
    if result.returncode != 0:
        print(colored("An error occurred:", 'red'))
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)

        # ask for additional instructions from user every five iterations
        if iteration % (when_gpt_4 ) == 0:
            # make a sound to notify the user
            # winsound.Beep(frequency = 2500, duration = 1000)
            
            print(colored("Please provide additional instructions to fix the error (write 'done' and then press 'enter' when done to continue):", 'blue'))
            additional_input = ""
            while True:
                line = input()
                if line.lower() == "done":
                    break
                additional_input += line + "\n"

            user_input += additional_input

        # make a recursive call to fix the code
        request_correction(content, user_input, response, result.stdout, result.stderr, iteration+1)
    else:
        # make a sound to notify the user
        # winsound.Beep(frequency = 2500, duration = 1000)
        print(colored("The program executed successfully. Here is the output:", 'green'))
        print(result.stdout)
        
        # ask user if the code is running as intended
        print(colored("Is the code running as intended? (yes/no):", 'blue'))
        feedback = input().lower()
        if feedback != "yes":
            print(colored("Please provide additional instructions (or press 'enter' to continue without additional instructions):", 'blue'))
            additional_input = ""
            while True:
                line = input()
                if line.lower() == "done":
                    break
                additional_input += line + "\n"

            user_input += additional_input

            # make a recursive call to modify the code
            request_correction(content, user_input, response, result.stdout, result.stderr, iteration+1)
        else:
            print(colored("The code is running as intended!", 'green'))

# start the first iteration
request_correction(content, user_input, "", "", "", 1)
