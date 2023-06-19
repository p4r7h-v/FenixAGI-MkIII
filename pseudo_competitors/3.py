import os
import openai
from termcolor import colored

def get_user_input(prompt_text):
    # Validate and return user input

def get_user_feedback():
    # Collect user feedback and return as string

def interactive_chat(user_task, max_iters=3, max_meta_iters=5):
    instructions = None
    for _ in range(max_meta_iters):
        conversation = [{'role': 'system', 'content': instructions},
                        {'role': 'user', 'content': user_task}]
        for _ in range(max_iters):
            # Call OpenAI API with conversation
            # Extract and print assistant's message
            # Append assistant's message to conversation
            # Collect and append user feedback to conversation
            # Check for success or failure phrases and return if found
        instructions = critique_and_revise_instructions(conversation)

def critique_and_revise_instructions(conversation_history):
    # Convert conversation_history to chat log string
    # Create meta prompt using chat log string
    # Call OpenAI API with meta prompt
    # Extract, print, and return new instructions

if __name__ == "__main__":
    user_task = get_user_input("Enter your task:")
    while user_task != 'done':
        interactive_chat(user_task)
        user_task = get_user_input("Enter your next task:")
    print("Thank you for using the interactive chat!")