import openai
import json
import os
import pandas as pd
from termcolor import colored
from functions import *
from function_descriptions import function_descriptions

openai.api_key = os.getenv("OPENAI_API_KEY")

approved_functions = [
    "search_codebase",
    "bing_search_save",
    "scrape_website",
    "save_fenix",
    "read_from_file",
    "write_to_file",
    "create_directory",
    "delete_file",
    "ask_user_for_additional_information",
    "create_code_search_csv",
    "count_tokens_in_string",
    "count_tokens_in_file",
    "create_markdown_file",
    "fenix_help",
]

COLORS = {
    'launch': 'cyan',
    'function_call': 'cyan',
    'function_info': 'green',
    'important': 'red',
    'query': 'red',
    'response': 'blue',
    # Add more as necessary...
}

class FenixState:
    def __init__(self, conversation=[], instructions="", function_calls=[], display_response=False, mode="manual", approved_functions=approved_functions):
        self.conversation = conversation
        self.instructions = instructions
        self.function_calls = function_calls
        self.display_response = display_response
        self.mode = mode
        self.approved_functions = approved_functions

def fenix_help(help_query):
    help_text = "Fenix is an advanced AI assistant made by Parth: https://www.linkedin.com/in/parthspatil/ https://replit.com/@p4r7h. Fenix assists the user with their query. Fenix can execute functions, such as searching the codebase, scraping a website, or saving a file. Fenix can also learn from the user's feedback and revise its instructions to improve its performance in the future. Designed to be extensible. Fenix is the beginning of a new era of AI assistants."\
                "\nHere are the available commands for Fenix: "\
                "\nPress '1' to Toggle function calling mode. 'manual' mode: Fenix asks for approval before executing a function. 'auto' mode: Fenix executes approved functions automatically. " \
                "\nPress '2' to Toggle Display Response. If enabled, Fenix displays the entire response from the function call. " \
                "\nPress '~' Fenix analyzes the conversation and learns from your feedback, saving a meta prompt. " \
                "\nPress '0' to derez Fenix. This wipes conversation history and meta prompt. The rest of the files remain untouched." \
                "\nPress 'exit' or 'quit' to quit the session. If conversation history is enabled, Fenix saves the conversation history to a json file."
    help_text += "\n\nFenix is also capable of executing a wide range of functions, these don't have explicit keystrokes. Here are the available functions for Fenix: "
    help_text += "\n".join([f"\n[{i}]: {function}" for i, function in enumerate(approved_functions)])
    

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613" ,
        stream=True, 
        messages=[
        {"role": "system", "content": help_text},
        {"role": "user", "content": help_query},
        {"role": "system", "content": """
        Fenix assists the user with their query. Fenix can execute functions, such as searching the codebase, scraping a website, or saving a file. Fenix can also learn from the user's feedback and revise its instructions to improve its performance in the future.
        """},
        ]
    )
    
    responses = ''
    for chunk in response:
        if "role" in chunk["choices"][0]["delta"]:
            continue
        elif "content" in chunk["choices"][0]["delta"]:
            r_text = chunk["choices"][0]["delta"]["content"]
            responses += r_text
            print(r_text, end='', flush=True)
    return responses


    
def save_fenix(filename="fenix_state.json"):
    global fenix_state  # Access the global instance
    with open("fenix_state.json", 'w') as f:
        json.dump(fenix_state.__dict__, f)
        return "Fenix State Saved."

def critique_and_revise_instructions(conversation_history, approved_functions):
    chat_log = '\n'.join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_history])

    meta_prompt = f"""The Assistant has just had the following interactions with a User. Please critique the Assistant's performance and revise the Instructions based on the interactions.

    ####
    Approved Functions (the Assistant can use these functions):
    {approved_functions}
    Chat Log:
    {chat_log}

    ####

    First, critique the Assistant's performance: What could have been done better? 
    Then, revise the Instructions to improve the Assistant's responses in the future. 
    The new Instructions should help the Assistant satisfy the user's request in fewer interactions. 
    Remember, the Assistant will only see the new Instructions, not the previous interactions.

    Start your critique with "Critique: ..." and your revised instructions with "Instructions: ...".
    """

    meta_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[{"role": "user", "content": meta_prompt}]

    )
    tell_user("Analyzing conversation history and learning from your feedback...", "yellow")
    #print(colored("Meta Prompt: " + meta_prompt, "cyan"))
    print("Token count is:", count_tokens_in_string(meta_prompt))
    meta_text = meta_response['choices'][0]['message']['content']
    #count_tokens_in_string(meta_text)
    print(colored("Meta Critique: " + meta_text.split("Critique: ")[1].split("Instructions: ")[0].strip(),"yellow"))
    new_instructions = meta_text.split("Instructions: ")[0].strip()
    
    print(colored(
        f'\nNew Instructions: {new_instructions}\n' + '#' * 80 + '\n', 'magenta'))

    return new_instructions

def rez_fenix(filename="fenix_state.json"):
    try:
        with open('fenix_state.json', 'r') as f:
            if f.read():
                # Move the read cursor back to the start of the file
                f.seek(0)
                data = json.load(f)
                fenix_state = FenixState(**data)  # Load data if there is any
            else:
                print("The file is empty.")
                fenix_state = FenixState()  # Create a new state
    except FileNotFoundError:
        fenix_state = FenixState()  # Create a new state if no data
    return fenix_state


def derez_fenix(filename="fenix_state.json"):
    # Delete the fenix_state.json file
    if os.path.exists("fenix_state.json"):
        os.remove("fenix_state.json")
        return "Fenix State Derezzed."


def stringify_conversation(conversation):
    return ' '.join([str(msg) for msg in conversation])


def ask_user(question, color='purple'):
    return input(colored(f"\n{question}", color))


def tell_user(message, color='blue'):
    print(colored(message, color))


def run_conversation():
    global fenix_state
    # Check if the state file exists
    if os.path.exists("fenix_state.json"):
        fenix_state = rez_fenix()
        conversation = fenix_state.conversation
        conversation.append(
            {"role": "system", "content": "Fenix State Rezzed."})
    else:
        fenix_state = FenixState(display_response=True, mode="manual",
                                approved_functions=approved_functions)
        conversation = fenix_state.conversation
        conversation.append(
            {"role": "system", "content": "Fenix State Created."})


    fenix_state.instructions = "Fenix is an advanced AI assistant made by Parth Patil, built on top of OpenAI's GPT language models. Fenix assists the user with their query. Fenix can execute functions, such as searching the codebase, scraping a website, or saving a file. Fenix can also learn from the user's feedback and revise its instructions to improve its performance in the future. Designed to be extensible. Fenix is the beginning of a new era of AI assistants."
    tell_user(fenix_state.instructions, COLORS['launch'])
    tell_user("Type 'help' for more information.", COLORS['launch'])
    conversation.append(
        {"role": "system", "content": fenix_state.instructions})
    while True:
        user_input = ask_user("> ", COLORS['query'])
        if user_input.lower() in ["exit", "quit"]:
            tell_user("Exiting Fenix.", COLORS['important'])
            conversation.append(
                {"role": "system", "content": "Exiting Fenix."})
            save_fenix()
            conversation.append(
                {"role": "system", "content": "State saved."})
            break

        elif user_input.lower() in ["~"]:
            # Update the meta instructions
            user_input = "Update the meta instructions."
            conversation.append({"role": "user", "content": user_input})
            fenix_state.instructions = critique_and_revise_instructions(conversation,
                                                                        approved_functions)
            conversation.append(
                {"role": "system", "content": "Meta instructions updated."})
            save_fenix()
            conversation.append(
                {"role": "system", "content": "State saved."})

        elif user_input.lower() == "1":
            # Toggle automatic function calling mode
            user_input = "Toggle automatic function calling mode."
            conversation.append({"role": "user", "content": user_input})
            if (fenix_state.mode == "manual"):
                fenix_state.mode = "auto"
                tell_user("Fenix is now in automatic mode.",
                          COLORS['important'])
                conversation.append(
                    {"role": "system", "content": "Fenix is now in automatic mode."})
                tell_user(
                    "Fenix will now execute approved functions automatically.", COLORS['important'])
                conversation.append(
                    {"role": "system", "content": "Fenix will now execute approved functions automatically."})
            elif (fenix_state.mode == "auto"):
                fenix_state.mode = "manual"
                tell_user("Fenix is now in manual mode.", COLORS['important'])
                conversation.append(
                    {"role": "system", "content": "Fenix is now in manual mode."})
                tell_user(
                    "Fenix will now ask for approval before executing a function.", COLORS['important'])
                conversation.append(
                    {"role": "system", "content": "Fenix will now ask for approval before executing a function."})
        elif user_input == "2":
            # Toggle display response
            user_input = "Toggle display response."
            conversation.append({"role": "user", "content": user_input})
            fenix_state.display_response = not fenix_state.display_response
            tell_user(
                f"Display Function Response is now set to {fenix_state.display_response}.", COLORS['important'])

            conversation.append(
                {"role": "system", "content": f"Display Function Response is now set to {fenix_state.display_response}."})


        elif user_input.lower() == "0":
            # Derez Fenix
            user_input = "Derez Fenix."
            conversation.clear()  # Clear the conversation list
            fenix_state.conversation.clear()  # Clear the conversation in FenixState
            fenix_state.instructions = ""  # Clear the instructions
            conversation.append({"role": "user", "content": user_input})
            tell_user("Derezzing Fenix.", COLORS['important'])
            conversation.append(
                {"role": "system", "content": "Derezzing Fenix."})
            derez_fenix()
            fenix_state = FenixState(display_response=False, mode="manual",
                                     approved_functions=approved_functions)
            tell_user("Conversation history and meta instructions reset.", COLORS['important'])
            conversation = fenix_state.conversation
            conversation.append(
                {"role": "system", "content": "New Fenix State Created."})
            tell_user(fenix_state.instructions, COLORS['launch'])

        else:
            conversation.append({"role": "user", "content": user_input})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=conversation,
                functions=function_descriptions,
                function_call="auto",
            )

            message = response["choices"][0]["message"]
            if message.get("function_call"):
                tell_user(
                    f"Function Call: {message.get('function_call')}", COLORS['function_call'])
                function_name = message["function_call"]["name"]
                args = json.loads(message["function_call"]["arguments"])
                current_function_call = (function_name, args)
                if function_name in approved_functions:
                    tell_user("Function Calling Mode: " +
                              str(fenix_state.mode), COLORS['important'])
                    if fenix_state.mode == "manual":
                        user_input = ask_user(
                            "Do you want to run the function? (y/n)", COLORS['query'])
                        if user_input.lower() in ["y", "yes"]:
                            function_response = eval(function_name)(**args)
                            if fenix_state.display_response:
                                tell_user(
                                    f"Function Response: {function_response}", COLORS['response'])

                        elif user_input.lower() in ["n", "no", "exit", "quit"]:
                            tell_user("Not executing function",
                                      COLORS['important'])
                            assistant_message = "Function execution skipped by user."
                            conversation.append(
                                {"role": "assistant", "content": assistant_message})
                            function_response = None
                        else:
                            tell_user(
                                "Unrecognized input. Default action is not to execute the function.", COLORS['important'])
                            assistant_message = "Function execution skipped due to unrecognized input."
                            conversation.append(
                                {"role": "assistant", "content": assistant_message})
                    elif fenix_state.mode == "auto":
                        function_response = eval(function_name)(**args)

                    if function_response is not None:
                        second_response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo-16k-0613",
                            messages=conversation + [
                                {"role": "user", "content": user_input},
                                {
                                    "role": "function",
                                    "name": function_name,
                                    "content": str(function_response),
                                },
                            ],
                            stream=True,
                        )

                        responses = ''

                        # Process each chunk
                        for chunk in second_response:
                            if "role" in chunk["choices"][0]["delta"]:
                                continue
                            elif "content" in chunk["choices"][0]["delta"]:
                                r_text = chunk["choices"][0]["delta"]["content"]
                                responses += r_text
                                print(r_text, end='', flush=True)
                        assistant_message = responses
                        conversation.append(
                            {"role": "assistant", "content": assistant_message})

                else:
                    tell_user(
                        "Sorry, I don't have access to that function.", COLORS['important'])
                    assistant_message = "Function execution skipped by assistant."
                    conversation.append(
                        {"role": "assistant", "content": assistant_message})

            else:
                third_response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-16k-0613",
                    messages=conversation,
                    stream=True,
                )
                responses = ''
                # Process each chunk
                for chunk in third_response:
                    if "role" in chunk["choices"][0]["delta"]:
                        continue
                    elif "content" in chunk["choices"][0]["delta"]:
                        r_text = chunk["choices"][0]["delta"]["content"]
                        responses += r_text
                        print(r_text, end='', flush=True)
                assistant_message = responses
                conversation.append(
                    {"role": "assistant", "content": assistant_message})

        print("\nConversation length (tokens): " +
              str(count_tokens_in_string(stringify_conversation(conversation))))


run_conversation()
