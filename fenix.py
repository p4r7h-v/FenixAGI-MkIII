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
from metaPrompter.metaPrompter import load_instructions_from_file, save_instructions_to_file, critique_and_revise_instructions

openai.api_key = os.getenv("OPENAI_API_KEY")

approved_functions = [
    "search_codebase",
    "bing_search_save",
    "scrape_website",
    "load_instructions_from_file",
]

def stringify_conversation(conversation):
    return ' '.join([str(msg) for msg in conversation])

# Step 1, send model the user query and what functions it has access to
def run_conversation():
    instructions = load_instructions_from_file("fenix_instructions.txt")
    print(colored(f"Launching Fenix", "yellow"))
    user_input = input(colored("\nFenix: Enter a query or type 'exit' to quit.\n", 'yellow'))
    conversation = [{"role": "system", "content": instructions}, {
            "role": "user", "content": user_input}]
    while True:
        # Exit Instructions
        if user_input.lower() in ["exit", "quit"]:
            break
        
        # Critique and Revise Instructions
        if user_input.lower() in ["critique", "revise"]:
            instructions = critique_and_revise_instructions(conversation)
            save_instructions_to_file("fenix_instructions.txt", instructions)
            user_input = input(colored("\nFenix: Enter a query or type 'exit' to quit.\n", 'yellow'))
        
        print("Conversation length (tokens): " + str(count_tokens(stringify_conversation(conversation))))
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
                    "description": "Scrape a website and save the results to a txt file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The url to scrape",
                            }
                        },
                        "required": ["url"],
                    }
                },
                {
                    "name": "load_instructions_from_file",
                    "description": "Load instructions from a file",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string",
                                "description": "The filepath to load",
                            }
                        },
                        "required": ["filepath"],
                    }
                },
            ],
            function_call="auto", 
        )
        

        message = response["choices"][0]["message"]
        print(colored("Function Call:" + str(message.get("function_call")), 'blue'))
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            args = json.loads(message["function_call"]["arguments"])
            if function_name in ["search_codebase","bing_search_save","scrape_website","load_instructions_from_file"]:
                print(colored("Function Name: " + function_name, 'green'))
                print(colored("Function Args: " + str(args), 'green'))
                # Execute Function?
                user_input = input(colored("Execute Function? (y/n): ", 'yellow'))
                if user_input.lower() in ["y", "yes"]:
                    function_response = eval(function_name)(**args)
                elif user_input.lower() in ["n", "no"]:
                    print(colored("Not executing function", 'red'))
                    continue
                else:
                    continue
            else:
                print(colored("Unexpected function name: " + function_name, 'red'))
                continue
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=[
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
        else:
            # Call OpenAI API to get response
            #print("Conversation so far: " + str(conversation))
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

        # Add the response to the conversation
        conversation.append(
            {"role": "system", "content": assistant_message}
        )

        # Prompt the user for the next input
        user_input = input(colored("\nFenix: Enter a query or type 'exit' to quit.\n", 'yellow'))
        
        # Add the response to the conversation
        conversation.append(
            {"role": "user", "content": user_input}
        )


run_conversation()
