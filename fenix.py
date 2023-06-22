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
    "save_state",
    "load_state",
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
    def __init__(self, conversation=[], instructions="", function_calls=[], display_response=True, mode="manual", approved_functions=[], autosave=False):
        self.conversation = conversation
        self.instructions = instructions
        self.function_calls = function_calls
        self.display_response = display_response
        self.mode = mode
        self.autosave = False
        self.approved_functions = approved_functions


fenix_state = FenixState(display_response=True, mode="manual")


def save_state():
    global fenix_state  # Access the global instance
    with open("fenix_state.json", 'w') as f:
        print("Saving state...")
        json.dump(fenix_state.__dict__, f)
        return "State saved."


def load_state(filename):
    global fenix_state
    if os.path.exists(filename):  # Check if the file exists
        with open(filename, 'r') as f:
            data = json.load(f)
            if data:
                fenix_state = FenixState(**data)  # Load data if there is any
                return fenix_state
            else:
                fenix_state = FenixState()  # Return a new state if the file is empty
                return fenix_state
    else:
        # Return a new state if the file doesn't exist
        fenix_state = FenixState()
        return fenix_state


def stringify_conversation(conversation):
    return ' '.join([str(msg) for msg in conversation])


def ask_user(question, color='purple'):
    return input(colored(f"\n{question}", color))


def tell_user(message, color='blue'):
    print(colored(message, color))


def tell_and_ask_user(message, question, tell_color='blue', ask_color='yellow'):
    tell_user(message, tell_color)
    return ask_user(question, ask_color)


def run_conversation():
    global fenix_state
    fenix_state = load_state("fenix_state.json")
    conversation = fenix_state.conversation
    instructions = fenix_state.instructions
    function_calls = fenix_state.function_calls
    display_response = fenix_state.display_response
    autosave = fenix_state.autosave

    tell_user("Launching Fenix", COLORS['launch'])
    immutable_instructions = "Fenix is a helpful assistant that can help you complete tasks. Fenix can search the codebase for functions, scrape websites, and search the web. Fenix can also learn from your feedback and improve over time."
    tell_user(immutable_instructions, COLORS['launch'])
    tell_user("Type 'help' for more information.", COLORS['launch'])
    conversation.append(
        {"role": "system", "content": immutable_instructions + instructions})
    while True:
        user_input = ask_user("> ", COLORS['query'])
        conversation.append({"role": "user", "content": user_input})

        if user_input.lower() in ["exit", "quit"]:
            if fenix_state.autosave:
                save_state()
            break

        if user_input.lower() in ["~"]:
            instructions = critique_and_revise_instructions(conversation,
                                                            approved_functions)
            if fenix_state.autosave:
                save_state()
            continue

        elif user_input.lower() == "1":
            # Toggle mode
            if (fenix_state.mode == "manual"):
                fenix_state.mode = "auto"
                tell_user("Fenix is now in auto mode.", COLORS['important'])
                tell_user(
                    "Fenix will now execute approved functions automatically.", COLORS['important'])
            elif (fenix_state.mode == "auto"):
                fenix_state.mode = "manual"
                tell_user("Fenix is now in manual mode.", COLORS['important'])
                tell_user(
                    "Fenix will now ask for approval before executing a function.", COLORS['important'])
        elif user_input == "2":
            fenix_state.display_response = not fenix_state.display_response
            tell_user(
                f"Display response is now set to {fenix_state.display_response}.", COLORS['important'])

        elif user_input.lower() == "0":
            # Toggle autosave
            if (fenix_state.autosave == True):
                fenix_state.autosave = False
                tell_user("Autosave is now off.", COLORS['important'])

            elif (fenix_state.autosave == False):
                fenix_state.autosave = True
                tell_user("Autosave is now on.", COLORS['important'])


        elif user_input.lower() == "help":
            tell_user(("Function Calling Mode: "+fenix_state.mode), COLORS['important'])
            print("Display response: " + str(display_response))
            print("Autosave: " + str(fenix_state.autosave))
            print("Instructions: " + fenix_state.instructions)
            print("Approved functions: " + str(fenix_state.approved_functions))
            tell_user(
                "Fenix can search the codebase for functions, scrape websites, and search the web. Fenix can also learn from your feedback and improve over time.", COLORS['launch'])
            tell_user(
                "\n'1' to toggle mode.\n - If Fenix is in manual mode, Fenix will ask you for approval before executing a function.\n - If Fenix is in auto mode, Fenix will execute approved functions automatically.", COLORS['important'])
            tell_user(
                "\n'2' to toggle display response. Fenix will display the response from the function call.", COLORS['launch'])
            tell_user(
                "\n'0' to toggle auto-save. Fenix will periodically save the conversation history to a json file.", COLORS['launch'])
            tell_user(
                "\n'~' for reflection and revision of instructions. Fenix will analyze the conversation and learn from your feedback.", COLORS['launch'])
            tell_user(
                "\n'exit' to quit. If conversation history is enabled, Fenix will save the conversation history to a json file.", COLORS['launch'])
            continue
        else:
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
                        "name": "save_state",
                        "description": "Save the current state of Fenix",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "filename": {
                                    "type": "string",
                                    "description": "he filename to save the state to. This should always be 'fenix_state.json'",
                                }
                            },
                        },
                    },
                    {
                        "name": "load_state",
                        "description": "Load a saved state of Fenix",
                        "parameters": {
                                "type": "object",
                                "properties": {
                                    "filename": {
                                        "type": "string",
                                        "description": "The filename to load the state from",
                                    }
                                },
                            "required": ["filename"],
                        }
                    },
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
                    tell_user("Function Calling Mode: " + str(fenix_state.mode), COLORS['important'])
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
                        else:
                            tell_user(
                                "Unrecognized input. Default action is not to execute the function.", COLORS['important'])
                            assistant_message = "Function execution skipped due to unrecognized input."
                            conversation.append(
                                {"role": "assistant", "content": assistant_message})
                    elif fenix_state.mode == "auto":
                        function_response = eval(function_name)(**args)

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
