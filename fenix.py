'''
Introducing FenixAGI Mk1, an advanced AI assistant designed to revolutionize project management. Powered by OpenAI's GPT-16k 3.5-turbo language model, Fenix is a versatile companion that assists users in various tasks. From codebase searches to web scraping and file management, Fenix can complete tasks efficiently. Fenix's extensibility ensures adaptability to evolving project needs. With its ability to learn from user feedback, Fenix continually improves its performance, making it an invaluable asset in streamlining project workflows. Experience the future of AI assistance with FenixAGI Mk1.

To use the functions in the functions.py file, a person needs the following API keys:

1. BING_SEARCH_KEY: Fenix uses Bing Search API for performing web searches using the `bing_search_save()` function. Get yours here:https://portal.azure.com/#
2. OPENAI_API_KEY: GPT-3.5-Turbo-16k is required to run  the main chat loop and call functions. here: https://platform.openai.com/signup

Fenix is an advanced AI assistant made by Parth: https://www.linkedin.com/in/parthspatil/ 
For more wacky LLM projects: https://replit.com/@p4r7h.
'''

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

  def __init__(self,
               conversation=[],
               instructions="",
               function_calls=[],
               display_response=False,
               mode="manual",
               approved_functions=approved_functions):
    self.conversation = conversation
    self.instructions = instructions
    self.function_calls = function_calls
    self.display_response = display_response
    self.mode = mode
    self.approved_functions = approved_functions


def fenix_help(help_query):
  help_text = '''
  Restoring Fenix State
  At the start of a session, the function checks if a saved state of the Fenix AI assistant exists. If it does, the state is loaded and the session continues from where it left off last time. If not, a new state is initialized.
  User Input
  The function continuously prompts the user for input and processes it accordingly.
  Special Commands
  There are several special commands the user can input to control the behavior of Fenix:
  'exit' or 'quit': Terminates the session and saves the current state of Fenix.
  '~': Updates the meta instructions used by the assistant.
  '1': Toggles between manual and automatic mode. In manual mode, Fenix will ask for approval before executing a function. In automatic mode, approved functions are executed automatically.
  '2': Toggles whether the assistant's responses should be displayed or not.
  '0': Resets Fenix to a default state, clearing the conversation history and meta instructions.
  AI Response Generation
  The user's input (and the entire conversation history) is fed into an instance of the GPT-3.5-turbo model, which generates the assistant's response. If the response includes a function call, the function is executed if it is approved and the mode is either manual and approved by user, or automatic. The result of the function call can optionally be displayed to the user, depending on the current settings.
  Extending Functionality
  New functionality can be added to Fenix by adding new functions to the approved_functions list and corresponding entries to the function_descriptions list.
  Error Handling
  Errors during the execution of a function are handled by returning an error message to the user and not executing the function. Unrecognized user inputs in response to a function call prompt are treated as 'no' responses.
  Future Development
  Currently, the conversation history used to generate responses is limited by the maximum context length of the GPT-3.5-turbo model. Future versions of the run_conversation() function may implement more sophisticated methods for managing long conversation histories.'''
  help_text += "\n\nFenix is also capable of executing a wide range of functions, these don't have explicit keystrokes. Here are the available functions for Fenix: "
  help_text += "\n".join(
    [f"\n {function}" for i, function in enumerate(approved_functions)])
  return help_text




def critique_and_revise_instructions(conversation_history, approved_functions):
  chat_log = '\n'.join([
    f"{msg['role'].capitalize()}: {msg['content']}"
    for msg in conversation_history
  ])

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

  meta_response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k-0613",
                                               messages=[{
                                                 "role": "user",
                                                 "content": meta_prompt
                                               }])
  tell_user(
    "Analyzing conversation history and learning from your feedback...",
    "yellow")
  #print(colored("Meta Prompt: " + meta_prompt, "cyan"))
  print("Token count is:", count_tokens_in_string(meta_prompt))
  meta_text = meta_response['choices'][0]['message']['content']
  #count_tokens_in_string(meta_text)
  print(
    colored(
      "Meta Critique: " +
      meta_text.split("Critique: ")[1].split("Instructions: ")[0].strip(),
      "yellow"))
  new_instructions = meta_text.split("Instructions: ")[0].strip()

  print(
    colored(f'\nNew Instructions: {new_instructions}\n' + '#' * 80 + '\n',
            'magenta'))

  return new_instructions

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
    conversation.append({"role": "system", "content": "Fenix State Rezzed."})
  else:
    fenix_state = FenixState(display_response=True,
                             mode="manual",
                             approved_functions=approved_functions)
    conversation = fenix_state.conversation
    conversation.append({"role": "system", "content": "Fenix State Created."})

  fenix_state.instructions = "FenixAGI Mk1 is an advanced AI assistant made by Parth Patil, built on top of OpenAI's GPT-16k 3.5-turbo language model. Fenix assists the user with their projects. Fenix can execute functions, such as searching the codebase, scraping a website, or saving a file. Fenix can also learn from the user's feedback and revise its instructions to improve its performance in the future. Designed to be extensible. Fenix is the beginning of a new era of AI assistants."
  tell_user(fenix_state.instructions, COLORS['launch'])
  tell_user("Type 'help' for more information.", COLORS['launch'])
  conversation.append({"role": "system", "content": fenix_state.instructions})
  while True:
    user_input = ask_user("> ", COLORS['query'])
    if user_input.lower() in ["exit", "quit"]:
      tell_user("Exiting Fenix.", COLORS['important'])
      conversation.append({"role": "system", "content": "Exiting Fenix."})
      save_fenix()
      conversation.append({"role": "system", "content": "State saved."})
      break

    elif user_input.lower() in ["~"]:
      # Update the meta instructions
      user_input = "Update the meta instructions."
      conversation.append({"role": "user", "content": user_input})
      fenix_state.instructions = critique_and_revise_instructions(
        conversation, approved_functions)
      conversation.append({
        "role": "system",
        "content": "Meta instructions updated."
      })
      save_fenix()
      conversation.append({"role": "system", "content": "State saved."})

    elif user_input.lower() == "1":
      # Toggle automatic function calling mode
      user_input = "Toggle automatic function calling mode."
      conversation.append({"role": "user", "content": user_input})
      if (fenix_state.mode == "manual"):
        fenix_state.mode = "auto"
        tell_user("Fenix is now in automatic mode.", COLORS['important'])
        tell_user("Fenix will now execute approved functions automatically.",
                  COLORS['important'])
        tell_user("Press '1' to toggle back to manual mode.",
                  COLORS['important'])
        conversation.append({
          "role": "system",
          "content": "Fenix is now in automatic mode."
        })
        conversation.append({
          "role":
          "system",
          "content":
          "Fenix will now execute approved functions automatically."
        })
      elif (fenix_state.mode == "auto"):
        fenix_state.mode = "manual"
        tell_user("Fenix is now in manual mode.", COLORS['important'])
        tell_user(
          "Fenix will now ask for approval before executing a function.",
          COLORS['important'])
        tell_user("Press '1' to toggle back to automatic mode.",
                  COLORS['important'])
        conversation.append({
          "role": "system",
          "content": "Fenix is now in manual mode."
        })
        conversation.append({
          "role":
          "system",
          "content":
          "Fenix will now ask for approval before executing a function."
        })
    elif user_input == "2":
      # Toggle display response
      user_input = "Toggle display response."
      conversation.append({"role": "user", "content": user_input})
      fenix_state.display_response = not fenix_state.display_response
      tell_user(
        f"Display Function Response is now set to {fenix_state.display_response}.",
        COLORS['important'])

      conversation.append({
        "role":
        "system",
        "content":
        f"Display Function Response is now set to {fenix_state.display_response}."
      })

    elif user_input.lower() == "0":
      #update meta instructions and derez fenix
      temp_instructions = critique_and_revise_instructions(
        conversation, approved_functions)
      # Derez Fenix
      user_input = "Derez Fenix."
      conversation.clear()  # Clear the conversation list
      fenix_state.conversation.clear()  # Clear the conversation in FenixState
      conversation.append({"role": "user", "content": user_input})
      tell_user("Derezzing Fenix.", COLORS['important'])
      conversation.append({"role": "system", "content": "Derezzing Fenix."})
      derez_fenix()
      fenix_state = FenixState(display_response=False,instructions=temp_instructions,
                               mode="manual",
                               approved_functions=approved_functions)
      tell_user("Meta Instructions updated and conversation history reset.",
                COLORS['important'])
      conversation = fenix_state.conversation
      conversation.append({
        "role": "system",
        "content": "New Fenix State Created."
      })
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
        tell_user(f"Function Call: {message.get('function_call')}",
                  COLORS['function_call'])
        function_name = message["function_call"]["name"]
        args = json.loads(message["function_call"]["arguments"])
        current_function_call = (function_name, args)
        if function_name in approved_functions:
          tell_user("Function Calling Mode: " + str(fenix_state.mode),
                    COLORS['important'])
          tell_user("Press '1' to toggle automatic function calling mode.",
                    COLORS['important'])
          if fenix_state.mode == "manual":
            user_input = ask_user("Do you want to run the function? (y/n)",
                                  COLORS['query'])
            if user_input.lower() in ["y", "yes"]:
              function_response = eval(function_name)(**args)
              if fenix_state.display_response:
                tell_user(f"Function Response: {function_response}",
                          COLORS['response'])

            elif user_input.lower() in ["n", "no", "exit", "quit"]:
              tell_user("Not executing function", COLORS['important'])
              assistant_message = "Function execution skipped by user."
              conversation.append({
                "role": "assistant",
                "content": assistant_message
              })
              function_response = None
            else:
              tell_user(
                "Unrecognized input. Default action is not to execute the function.",
                COLORS['important'])
              assistant_message = "Function execution skipped due to unrecognized input."
              conversation.append({
                "role": "assistant",
                "content": assistant_message
              })
              function_response = None
          elif fenix_state.mode == "auto":
            function_response = eval(function_name)(**args)

          if function_response is not None:
            second_response = openai.ChatCompletion.create(
              model="gpt-3.5-turbo-16k-0613",
              messages=conversation + [
                {
                  "role": "user",
                  "content": user_input
                },
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
            conversation.append({
              "role": "assistant",
              "content": assistant_message
            })

        else:
          tell_user("Sorry, I don't have access to that function.",
                    COLORS['important'])
          assistant_message = "Function execution skipped by assistant."
          conversation.append({
            "role": "assistant",
            "content": assistant_message
          })

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
        conversation.append({
          "role": "assistant",
          "content": assistant_message
        })

    print("\nConversation length (tokens): " +
          str(count_tokens_in_string(stringify_conversation(conversation))))


run_conversation()
