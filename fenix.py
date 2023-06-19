import openai
import json
import os
import codeSearch
from codeSearch import search_codebase
import pandas as pd
from token_counter import count_tokens

#Function df
df = None
root_folder = os.path.join(os.getcwd(), ".")
code_search_file = os.path.join(root_folder, "code_search.csv")
df = pd.read_csv(code_search_file)

openai.api_key = os.getenv("OPENAI_API_KEY")
 
# Step 1, send model the user query and what functions it has access to
def run_conversation():
    user_input = input("Enter a query: ")
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
            }
        ],
        function_call="auto", 
    )

    message = response["choices"][0]["message"]
    print("Function Call:" + str(message.get("function_call")))
    if message.get("function_call"):
        function_name = message["function_call"]["name"]
        args = json.loads(message["function_call"]["arguments"])
        if function_name == "search_codebase":
            print("Function Name: " + function_name)
            print("Function Args: " + str(args))
            function_response = eval(function_name)(**args)
        else:
            print("Unexpected function name: " + function_name)
            return
        #print("Function Response: " + str(function_response))
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
        )
        print(second_response["choices"][0]["message"]["content"])
        return second_response

run_conversation()