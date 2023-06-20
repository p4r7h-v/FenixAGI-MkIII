import openai
import json
import os
import pandas as pd
from token_counter import count_tokens
from termcolor import colored
import codeSearch
from codeSearch import search_codebase
from bingSearch import bing_search_save

openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 1, send model the user query and what functions it has access to
def run_conversation():
    while True:
        user_input = input(colored("\nFenix: Enter a query or type 'exit' to quit: ", 'yellow'))
        if user_input.lower() in ["exit", "quit"]:
            break
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[{"role": "user", "content": user_input}],
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
                }
            ],
            function_call="auto", 
        )

        message = response["choices"][0]["message"]
        print(colored("Function Call:" + str(message.get("function_call")), 'blue'))
        if message.get("function_call"):
            function_name = message["function_call"]["name"]
            args = json.loads(message["function_call"]["arguments"])
            if function_name in ["search_codebase","bing_search_save"]:
                print(colored("Function Name: " + function_name, 'green'))
                print(colored("Function Args: " + str(args), 'green'))
                # Execute Function?
                user_input = input(colored("Execute Function? (y/n): ", 'yellow'))
                if user_input.lower() in ["y", "yes"]:
                    function_response = eval(function_name)(**args)
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
                        "content": function_response,
                    },
                ],
                stream=True,
            )
            # 
            responses = ''

            # Process each chunk
            for chunk in second_response:
                if "role" in chunk["choices"][0]["delta"]:
                    continue
                elif "content" in chunk["choices"][0]["delta"]:
                    r_text = chunk["choices"][0]["delta"]["content"]
                    responses += r_text
                    print(r_text, end='', flush=True)

run_conversation()
