import os
import openai
from termcolor import colored

def get_user_input(prompt_text):
    user_input = input(prompt_text)
    while not user_input.strip():
        print(colored("Input cannot be empty. Please try again.", "red"))
        user_input = input(prompt_text)
    return user_input

def get_user_choice(choices):
    for i, choice in enumerate(choices, 1):
        print(f"{i}. {choice}")
    print("Or type your own response.")

    user_input = input()
    while not user_input.strip() or (not user_input.isnumeric() and len(user_input.split()) == 1):
        print(colored("Invalid input. Please try again.", "red"))
        user_input = input()

    if user_input.isnumeric() and 1 <= int(user_input) <= len(choices):
        return choices[int(user_input) - 1]
    else:
        return user_input
    
def call_openai_api(conversation):
    response = openai.ChatCompletion.create(model="gpt-4-0613", messages=conversation)
    assistant_message = response['choices'][0]['message']['content']
    print(colored("Assistant: ", "green"), assistant_message)
    return response

def critique_and_revise_instructions(conversation_history):
    chat_log = '\n'.join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_history])

    meta_prompt = f"""The Assistant has just had the following interactions with a User. Please critique the Assistant's performance and revise the Instructions based on the interactions.

    ####

    {chat_log}

    ####

    First, critique the Assistant's performance: What could have been done better? 
    Then, revise the Instructions to improve the Assistant's responses in the future. 
    The new Instructions should help the Assistant satisfy the user's request in fewer interactions. 
    Remember, the Assistant will only see the new Instructions, not the previous interactions.

    Start your critique with "Critique: ..." and your revised instructions with "Instructions: ...".
    """

    meta_response = openai.ChatCompletion.create(model="gpt-4-0613", messages=[{"role": "user", "content": meta_prompt}])
    meta_text = meta_response['choices'][0]['message']['content']

    new_instructions = meta_text.split("Instructions: ")[1].strip()

    print(f'\nNew Instructions: {new_instructions}\n' + '#' * 80 + '\n')

    return new_instructions

def interactive_chat(user_task, max_iters=3, max_meta_iters=5):
    instructions = None
    for _ in range(max_meta_iters):
        conversation = [{'role': 'system', 'content': instructions}, {'role': 'user', 'content': user_task}]
        for _ in range(max_iters):
            response = call_openai_api(conversation)
            print("Response: ", response)
            assistant_message = extract_message(response)
            print(colored(assistant_message, "cyan"))
            conversation.append({'role': 'assistant', 'content': assistant_message})
            user_choice = get_user_choice(["Option 1", "Option 2", "Option 3", "Option 4", "Display meta conversation"])
            if user_choice == "Display meta conversation":
                for message in conversation:
                    print(f"{message['role']}: {message['content']}")
            else:
                conversation.append({'role': 'user', 'content': user_choice})
        instructions = critique_and_revise_instructions(conversation)


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    user_task = get_user_input("Enter your task: ")
    while user_task != "done":
        interactive_chat(user_task)
        user_task = get_user_input("Enter your task: ")
    print(colored("Thank you for using the AI assistant!", "green"))
