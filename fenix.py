import openai
import json
import os
import pandas as pd
from token_counter import count_tokens
from termcolor import colored
import codeSearch
from codeSearch import search_codebase
from bingSearch import bing_search_save
from basicScraper import scrape_website
from metaPrompter.metaPrompter import critique_and_revise_instructions

openai.api_key = os.getenv("OPENAI_API_KEY")

approved_functions = [
    "search_codebase",
    "bing_search_save",
    "scrape_website",
    "save_fenix",
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
    def __init__(self, conversation=[], instructions="", function_calls=[], display_response=False, mode="manual", approved_functions=approved_functions, autosave=False):
        self.conversation = conversation
        self.instructions = instructions
        self.function_calls = function_calls
        self.display_response = display_response
        self.mode = mode
        self.autosave = autosave
        self.approved_functions = approved_functions


def save_fenix(filename="fenix_state.json"):
    global fenix_state  # Access the global instance
    with open("fenix_state.json", 'w') as f:
        json.dump(fenix_state.__dict__, f)
        return "Fenix State Saved."


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
                                 autosave=False, approved_functions=approved_functions)
        conversation = fenix_state.conversation
        conversation.append(
            {"role": "system", "content": "Fenix State Created."})


    fenix_state.instructions = "Fenix is a helpful assistant that can help you complete tasks. Fenix can search the codebase for functions, scrape websites, and search the web. Fenix can also learn from your feedback and improve over time."
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
            if fenix_state.autosave:
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
            if fenix_state.autosave:
                save_fenix()
                conversation.append(
                    {"role": "system", "content": "State saved."})
            continue

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

        elif user_input.lower() == "3":
            # Toggle autosave
            user_input = "Toggle autosave."
            conversation.append({"role": "user", "content": user_input})
            if (fenix_state.autosave == True):
                fenix_state.autosave = False
                tell_user("Autosave is now off.", COLORS['important'])
                conversation.append(
                    {"role": "system", "content": "Autosave is now off."})

            elif (fenix_state.autosave == False):
                fenix_state.autosave = True
                tell_user("Autosave is now on.", COLORS['important'])
                conversation.append(
                    {"role": "system", "content": "Autosave is now on."})

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
            fenix_state = FenixState(display_response=False, mode="manual", autosave=False,
                                     approved_functions=approved_functions)
            tell_user("Conversation history and meta instructions reset.", COLORS['important'])
            conversation = fenix_state.conversation
            conversation.append(
                {"role": "system", "content": "New Fenix State Created."})

        elif user_input.lower() == "help":
            tell_user("\nHere are the available commands for Fenix: ",
                      COLORS['important'])
            conversation.append(
                {"role": "system", "content": "Here are the available commands for Fenix: "})

            help_text = "\n[1]: Toggle function calling mode. 'manual' mode: Fenix asks for approval before executing a function. 'auto' mode: Fenix executes approved functions automatically. " \
                        "\n[2]: Toggle display response. If enabled, Fenix displays the response from the function call. " \
                        "\n[3]: Toggle auto-save. If enabled, Fenix periodically saves the conversation history to a json file. " \
                        "\n[0]: Derez Fenix. This wipes conversation history and meta prompt." \
                        "\n[~]: Reflection and revision of instructions. Fenix analyzes the conversation and learns from your feedback. " \
                        "\n['exit' or 'quit']: Quit the session. If conversation history is enabled, Fenix saves the conversation history to a json file."

            tell_user(help_text, COLORS['launch'])
            conversation.append({"role": "system", "content": help_text})

            settings_text = "Current Settings: " \
                            "\nFunction Calling Mode: "+fenix_state.mode + \
                            "\nDisplay response: " + str(fenix_state.display_response) + \
                            "\nAutosave: " + str(fenix_state.autosave) + \
                            "\nInstructions: " + fenix_state.instructions + \
                            "\nApproved functions: " + \
                str(fenix_state.approved_functions)

            tell_user(settings_text, COLORS['launch'])

        else:
            conversation.append({"role": "user", "content": user_input})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=conversation,
                functions=[
                    {
                        "name": "search_codebase",
                        "description": "Search the codebase dataframe of python functions for the function with the most similar results",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "code_query": {
                                    "type": "string",
                                    "description": "The code_query to search for",
                                },
                                "n": {
                                    "type": "integer",
                                    "description": "The number of results to return",
                                },
                            },
                            "required": ["code_query", "n"],
                        },
                    },
                    {
                        "name": "bing_search_save",
                        "description": "Search bing and save the results to a csv",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "The query to search for",
                                }
                            },
                            "required": ["query"],
                        }
                    },
                    {
                        "name": "scrape_website",
                        "description": "Scrape or read a website and save the results to a txt file",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "url": {
                                    "type": "string",
                                    "description": "The url to scrape or read",
                                }
                            },
                            "required": ["url"],
                        }
                    },
                    {
                        "name": "save_fenix",
                        "description": "Save the current state of Fenix",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "filename": {
                                    "type": "string",
                                    "description": "",
                                }
                            },
                        },
                    }
                ],
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
              str(count_tokens(stringify_conversation(conversation))))


run_conversation()
