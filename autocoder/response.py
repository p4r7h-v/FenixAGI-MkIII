import os
import openai
from termcolor import colored

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_user_input(prompt_text):
    while True:
        user_input = input(colored(prompt_text, "cyan"))
        if user_input.strip():
            return user_input
        print(colored("Input can't be empty, try again.", "red"))

def get_user_feedback():
    feedback = ""
    print(colored("Enter user feedback below. When finished, enter 'done'.", "cyan"))
    while True:
        line = input(colored("> ", "cyan"))
        if line.lower() == "done":
            break
        feedback += line + "\n"
    return feedback.strip()

def interactive_chat(user_task, max_iters=3, max_meta_iters=5):
    SUCCESS_PHRASE = 'task succeeded'
    FAIL_PHRASE = 'task failed'
    KEY_PHRASES = [SUCCESS_PHRASE, FAIL_PHRASE]

    instructions = 'None'
    for iteration in range(max_meta_iters):
        print(f'\n[Iteration {iteration+1}/{max_meta_iters}]\n')
        conversation = [{"role": "system", "content": instructions}, {"role": "user", "content": user_task}]

        for step in range(max_iters):
            print(f'Step {step+1}/{max_iters}')

            response = openai.ChatCompletion.create(model="gpt-4-0613", messages=conversation)
            assistant_message = response['choices'][0]['message']['content']
            print(colored("Assistant: ", "green"), assistant_message)

            conversation.append({"role": "assistant", "content": assistant_message})

            user_feedback = get_user_feedback()
            conversation.append({"role": "user", "content": user_feedback})
            
            if user_feedback.lower() in KEY_PHRASES:
                print('Success!' if user_feedback.lower() == SUCCESS_PHRASE else 'Failure. Thanks for participating!')
                return

        instructions = critique_and_revise_instructions(conversation)

    print('Task failed after maximum iterations. Thanks for participating!')

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

if __name__ == '__main__':
    user_task = get_user_input("Enter User Instructions for a task. When finished, enter 'done': ")
    while user_task.lower() != 'done':
        interactive_chat(user_task)
        user_task = get_user_input("\nYou can enter a new task or 'done' to exit: ")
    print('Thanks for participating!')