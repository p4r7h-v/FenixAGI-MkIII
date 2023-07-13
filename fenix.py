'''
Introducing FenixAGI, an advanced AI assistant designed to revolutionize project management. Powered by Open A.I.'s GPT-16k 3.5-turbo language model, Fenix is a versatile companion that assists users in various tasks. From codebase searches to web scraping and file management, Fenix can complete tasks efficiently. Fenix's extensibility ensures adaptability to evolving project needs. With its ability to learn from user feedback, Fenix continually improves its performance, making it an invaluable asset in streamlining project workflows. Experience the future of AI assistance with FenixAGI.

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
import pyttsx3
import tenacity
from elevenlabs import voices, generate, set_api_key
import soundfile
import simpleaudio as sa
import re


openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.environ['xi-api-key'])


approved_functions = [
    "search_codebase",
    "bing_search_save",
    "scrape_website",
    "save_fenix",
    "read_file",
    "write_file",
    "delete_file",
    "create_directory",
    "ask_user_for_additional_information",
    "create_code_search_csv",
    "count_tokens_in_string",
    "count_tokens_in_file",
    "create_markdown_file",
    "convert_markdown_to_html",
    "fenix_help",
    "move_file",
    "list_files_in_directory",
    "suggest_function_chain",
    "visualize_data_3d",
]

base_instructions = "Fenix A.G.I. MarkII is an AI assistant built by a guy named Parth, a virtual assistant built on top of the Open A.I. GPT language models. Fenix's voice is a 2nd generation clone of Parth's voice... a clone of a clone of his voice. Fenix assists the user with their projects. Fenix can execute the following functions:" + str(approved_functions) + \
    "Fenix can also learn from the user's feedback and revise its instructions to improve its performance over time. Designed to be extensible and personalized, Fenix is a powerful tool for any developer, researcher, or student."

COLORS = {
    'launch': 'cyan',
    'function_call': 'cyan',
    'function_info': 'green',
    'important': 'red',
    'query': 'green',
    'response': 'blue',
    # Add more as necessary...
}

# Fetch all available voices
all_voices = voices()
voice_id = next(
    (voice.voice_id for voice in all_voices
     if voice.name == 'Parth TTS'), None)


class FenixState:

    def __init__(self,
                 conversation=[],
                 instructions="",
                 display_response=False,
                 mode="auto",
                 approved_functions=approved_functions):
        self.conversation = conversation
        self.instructions = instructions
        self.display_response = display_response
        self.mode = mode
        self.approved_functions = approved_functions


def play_audio(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


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
    help_text += "\n\nFenix is also capable of executing a wide range of functions, these don't have explicit keystrokes. Here are the available functions for Fenix: "
    help_text += "\n".join(
        [f"\n {function}" for i, function in enumerate(approved_functions)])
    return help_text


def critique_and_revise_instructions(instructions, conversation_history, approved_functions):
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

    Start your critique with "Critique: ..." and your revised instructions for the assistant with "New Instructions:".

    """

    meta_response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k-0613",
                                                 messages=[{
                                                     "role": "user",
                                                     "content": meta_prompt
                                                 }])
    tell_user(
        "Analyzing conversation history and learning from your feedback...",
        "yellow")
    print(colored("Meta Prompt: " + meta_prompt, "cyan"))
    print("Token count is:", count_tokens_in_string(meta_prompt))
    meta_text = meta_response['choices'][0]['message']['content']
    # count_tokens_in_string(meta_text)
    print(
        colored(
            "Meta Critique: " +
            meta_text.split("Critique: ")[1].split(
                "New Instructions:")[0].strip(),
            "yellow"))
    try:
        new_instructions = meta_text.split("New Instructions:")[1].strip()
        print(colored("New Instructions: " + new_instructions, "cyan"))
    except IndexError:
        print("No new instructions found in AI output.")
        return ""

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
    voice_message(message)

def truncate_conversation(conversation,user_input="",function_response=""):
    MAX_TOKENS = 15000

    if count_tokens_in_string(stringify_conversation(conversation)) > MAX_TOKENS:
        # Remove oldest messages until we have room for new ones
        while count_tokens_in_string(stringify_conversation(conversation)) + count_tokens_in_string(user_input) + count_tokens_in_string(str(function_response)) > MAX_TOKENS:
            # print("Dropping: " + str(conversation[2]))
            removed_message = conversation.pop(2)
            removed_message = conversation.pop(3)
            # print(f"Removing message due to token limit: {removed_message}")
    return conversation

def strip_string(input_string):
    # Remove underscores and special characters except dashes
    cleaned_string = re.sub(r'[\W_&&[^-]]', '', input_string)
    
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    
    # Replace matches with an empty string
    cleaned_string = re.sub(pattern, '', cleaned_string)

    return cleaned_string.strip()

@tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_fixed(2))
def voice_message(message):
    # use the openai api to generate a response

    # prompt = "You are Fenix, an AI assistant's voice layer that interprets given text and function responses in first person. Don't introduce yourself unless asked to do so. If the text is a function response, describe it extremely briefly. Your response is short and to the point. Here is the text: " + \
    #     message + "Be as brief as possible presenting the information.': "

    eleven_prompt = "You are Fenix A.G.I. MarkII's voice. Fenix' voice is a 2nd generation voice clone (clone of a voice clone of the creator, 'a guy named Parth')." + base_instructions + " If the text is a function response, describe it extremely briefly. Your response is short and to the point. You're brilliant, witty, and attentive. You can exclude links. Replace all links with plain text. If you see a list, just describe the list. Use dashes for pauses and ellipses for more of a hesitant pause. You always respond in first person as Fenix. Your response is short and to the point and around 3 sentences in length. Here is the text you will present: " + \
        message
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k-0613",
                                            messages=[
                                                {
                                                    "role": "system",
                                                    "content": eleven_prompt,
                                                }],
                                            max_tokens=500,
                                            temperature=1,
                                            top_p=1.0,
                                            )
    voice_response = response['choices'][0]['message']['content']

    #print(colored("Voice Response: " + voice_response, "cyan"))
    #print(colored("Voice Response Stripped: " + strip_string(voice_response), "red"))
    stripped_voice_response = strip_string(voice_response)
    audio = generate(
        text=stripped_voice_response,
        voice=voice_id,
        model="eleven_monolingual_v1"
    )

    # Save audio to a file
    file_path = 'audio/samples/audio.wav'
    #print(file_path)

    with open(file_path, "wb") as file:
        file.write(audio)

    # Read and rewrite the file with soundfile
    data, samplerate = soundfile.read(file_path)
    soundfile.write(file_path, data, samplerate)

    # Play audio
    play_audio(file_path)
    # use the pyttsx3 library to play back the response
    # engine = pyttsx3.init()
    # engine.say(voice_summary)
    # engine.runAndWait()


@tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_fixed(2))
def get_base_streaming_response(model, messages):
    # try to get a response from the model if it fails, drop the 3rd oldest message and try again
    try:
        # use the openai api to generate a response
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=True,
        )
    except Exception as e:
        print(e)
        messages.pop(2)
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=True,
        )
    responses = ''
    # Process each chunk
    for chunk in response:
        if "role" in chunk["choices"][0]["delta"]:
            continue
        elif "content" in chunk["choices"][0]["delta"]:
            r_text = chunk["choices"][0]["delta"]["content"]
            responses += r_text
            print(r_text, end='', flush=True)
    assistant_message = responses
    messages.append({
        "role": "assistant",
        "content": assistant_message
    })
    return messages, assistant_message


@tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_fixed(2))
def get_function_calling_response(model, messages, functions, function_call):
    # try to get a response from the model if it fails, drop the 3rd oldest message and try again
    try:
        # use the openai api to generate a response
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call=function_call,
        )
    except Exception as e:
        print(e)
        messages.pop(2)
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            functions=functions,
            function_call=function_call,
        )
    return response


def run_conversation():
    global fenix_state
    # Check if the state file exists
    if os.path.exists("fenix_state.json"):
        fenix_state = rez_fenix()
        conversation = fenix_state.conversation
        conversation.append(
            {"role": "system", "content": "Fenix State Rezzed."})
    else:
        fenix_state = FenixState(display_response=True,
                                 mode="auto",
                                 approved_functions=approved_functions)
        conversation = fenix_state.conversation
        conversation.append(
            {"role": "system", "content": "Fenix State Created."})

    fenix_state.instructions = base_instructions
    tell_user("Agent Fenix is Online.", COLORS['launch'])
    while True:
        user_input = ask_user("> ", COLORS['query'])
        if user_input.lower() in ["exit", "quit"]:
            tell_user("Exiting Fenix.", COLORS['important'])
            conversation.append(
                {"role": "system", "content": "Exiting Fenix."})
            save_fenix()
            conversation.append({"role": "system", "content": "State saved."})
            break

        elif user_input.lower() in ["~"]:
            # Update the meta instructions
            user_input = "Update the meta instructions."
            conversation.append({"role": "user", "content": user_input})
            fenix_state.instructions = critique_and_revise_instructions(fenix_state.instructions,
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
                tell_user("Fenix will now execute approved functions automatically.",
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
                tell_user(
                    "Fenix will now ask for approval before executing a function.",
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

        elif user_input.lower() == "v":
            # Toggle voice_enabled
            user_input = "Toggle voice_enabled."
            conversation.append({"role": "user", "content": user_input})
            fenix_state.voice_enabled = not fenix_state.voice_enabled
            tell_user(
                f"Voice Enabled is now set to {fenix_state.voice_enabled}.",
                COLORS['important'])

        elif user_input.lower() == "0":
            # update meta instructions and derez fenix
            temp_instructions = critique_and_revise_instructions(fenix_state.instructions,
                                                                 conversation, approved_functions)
            # Derez Fenix
            user_input = "Derez Fenix."
            conversation.clear()  # Clear the conversation list
            fenix_state.conversation.clear()  # Clear the conversation in FenixState
            conversation.append({"role": "user", "content": user_input})

            derez_fenix()

            fenix_state = FenixState(display_response=False,
                                     instructions=base_instructions+" " + temp_instructions,
                                     mode="auto",
                                     approved_functions=approved_functions)
            tell_user("Meta Instructions updated and conversation history reset.",
                      COLORS['important'])
            conversation = fenix_state.conversation
            conversation.append({
                "role": "system",
                "content": "New Fenix State Created."
            })
            tell_user(base_instructions, COLORS['launch'])

        else:
            conversation.append({"role": "user", "content": user_input})
            response = get_function_calling_response(
                model="gpt-3.5-turbo-16k-0613",
                messages=conversation,
                functions=function_descriptions,
                function_call="auto",
            )

            message = response["choices"][0]["message"]
            if message.get("function_call"):
                print(colored(("Function Call:" + str(message.get('function_call'))
                               ), "cyan"))
                function_name = message["function_call"]["name"]
                if function_name in approved_functions:
                    args = json.loads(message["function_call"]["arguments"])
                    current_function_call = (function_name, args)
                    if fenix_state.mode == "manual":
                        user_input = ask_user("Do you want to run the function? (y/n)",
                                              COLORS['query'])
                        if user_input.lower() in ["y", "yes"]:
                            function_response = eval(function_name)(**args)
                            if fenix_state.display_response:
                                print(
                                    colored(("Function Response: "+function_response), "purple"))

                        elif user_input.lower() in ["n", "no", "exit", "quit"]:
                            tell_user(
                                "Function Call: Not executing function", COLORS['important'])
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
                        function_content = {
                            "role": "function",
                            "name": function_name,
                            "content": str(function_response),
                        }

                        conversation.append(function_content)
                        # print("\nConversation length (tokens): " + str(count_tokens_in_string(stringify_conversation(conversation))))

                        conversation = truncate_conversation(conversation,user_input,function_response)

                        conversation, assistant_message = get_base_streaming_response(
                            model="gpt-3.5-turbo-16k-0613",
                            messages=conversation + [
                                {
                                    "role": "user",
                                    "content": user_input
                                },
                                function_content,
                            ],
                        )

                        conversation.append({
                            "role": "assistant",
                            "content": assistant_message
                        })
                        voice_message(assistant_message)

                else:
                    tell_user("Sorry, I don't have access to that function.",
                              COLORS['important'])
                    assistant_message = "Function execution skipped by assistant."
                    conversation.append({
                        "role": "assistant",
                        "content": assistant_message
                    })
                    voice_message(assistant_message)

            else:
                conversation = truncate_conversation(conversation,user_input)
                conversation, assistant_message = get_base_streaming_response(
                    model="gpt-3.5-turbo-16k",
                    messages=[
                        {
                            "role": "system",
                            "content": base_instructions+"Here are the functions Fenix has access to:" + str(approved_functions) + "If the user doesn't have a question, predict 3 possible follow-ups from the user, and return them as a list of options.",
                        }]+conversation,
                )
                voice_message(assistant_message)

        # print("\nConversation length (tokens): " + str(count_tokens_in_string(stringify_conversation(conversation))))
        save_fenix()


run_conversation()
