import os
import openai
from termcolor import colored
from token_counter import count_tokens
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def load_instructions_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return "You are a helpful assistant."

def save_instructions_to_file(file_path, instructions):
    with open(file_path, 'w') as file:
        print(colored(f"Saving Instructions to {file_path}", "yellow"))
        file.write(instructions)

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
    print(colored("Meta Prompt: " + meta_prompt, "cyan"))
    print("Token count is:", count_tokens(meta_prompt))
    meta_text = meta_response['choices'][0]['message']['content']
    count_tokens(meta_text)
    print(colored("Meta Critique: " + meta_text.split("Critique: ")[1].split("Instructions: ")[0].strip(),"yellow"))
    new_instructions = meta_text.split("Instructions: ")[1].strip()
    
    print(colored(
        f'\nNew Instructions: {new_instructions}\n' + '#' * 80 + '\n', 'magenta'))

    return new_instructions

def interactive_chat(user_task, instructions_file_path, approved_functions):
    instructions = load_instructions_from_file(instructions_file_path)
    print(colored(f"Opening Task: {user_task}", "yellow"))

    conversation = [{"role": "system", "content": instructions}, {
            "role": "user", "content": user_task}]
    while True:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=conversation,
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
        print("Token count is:", count_tokens(assistant_message))

        conversation.append(
            {"role": "assistant", "content": assistant_message})

        # Collect multiline user feedback
        user_feedback = ""
        print(colored("Type your message. When finished, type 'done')", "cyan"))
        print(colored("Type '~' to update Meta Instructions)", "cyan"))
        print(colored("Type '.' to end the session)", "cyan"))
        while True:
            line = input(colored("> ", "cyan"))
            if line.lower() == 'done':
                break
            elif line.lower() == '~':
                instructions = critique_and_revise_instructions(conversation, approved_functions)
                save_instructions_to_file(instructions_file_path, instructions)
                print(colored('Meta Instructions saved.', 'green'))
                return
            elif line.lower() == '.':
                print(colored('Session ended. Thanks for participating!', 'green'))
                return
            user_feedback += line + "\n"

        conversation.append({"role": "user", "content": user_feedback.strip()})

if __name__ == '__main__':
    instructions_file_path = "metaPrompter/instructions.txt"
    while True:  # create an outer loop for multiple tasks
        user_task = ''
        print(colored('\n[New Task]\n', "yellow"))
        user_task = input(colored("Type your task. When finished, type 'done')\n> ", "cyan"))
        if user_task.lower() == 'done':
            break
        interactive_chat(user_task, instructions_file_path)
    print(colored('Thanks for participating!', 'green'))

