import os
import json
import sys
import shutil
from termcolor import colored
from auto_coder_tools.instruction_gen import generate_instructions
from auto_coder_tools.pseudo_gen_concurrent import generate_concurrently
from auto_coder_tools.write_competitors_to_files  import write_competitors_to_files
from auto_coder_tools.pseudo_eval_eliminate import eliminate
from auto_coder_tools.final_code import final_code_responses

from concurrent.futures import ThreadPoolExecutor
import argparse



def parse_args():
    parser = argparse.ArgumentParser(description='Auto Coder')
    parser.add_argument('--auto', action='store_true', help='run in automatic mode without user input')
    parser.add_argument('--model', type=str, default="gpt-3.5-turbo-16k-0613", help='choose the model to use')
    parser.add_argument('--num', type=int, default=3, help='number of pseudo code to generate')
    parser.add_argument('--pause', action='store_true', help='pause after instructions are generated')
    return parser.parse_args()

args = parse_args()

def clear_terminal():
    if os.name == 'nt':
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Linux and macOS

def print_welcome_screen():
    clear_terminal()
    welcome_message = """
   _____          __           _________            .___             ____   ____    _____  
  /  _  \  __ ___/  |_  ____   \_   ___ \  ____   __| _/___________  \   \ /   /   /  |  | 
 /  /_\  \|  |  \   __\/  _ \  /    \  \/ /  _ \ / __ |/ __ \_  __ \  \   Y   /   /   |  |_
/    |    \  |  /|  | (  <_> ) \     \___(  <_> ) /_/ \  ___/|  | \/   \     /   /    ^   /
\____|__  /____/ |__|  \____/   \______  /\____/\____ |\___  >__|       \___/ /\ \____   | 
        \/                             \/            \/    \/                 \/      |__|                           
    """
    version = "Auto Coder V.4"
    print(colored(welcome_message, 'green'))
    print(f"\nWelcome to {version}")

print_welcome_screen()
print(colored("\n\nNOTICE: This program can consume a lot of tokens especially with more pseudo generations!!! GPT-4 can cost 30 cents to 1 dollar OR MORE for each run with 3 pseudo generations", "magenta"))

if not args.auto:

    model = ""

    # ask user which model to use
    while model == "":
            # tell user that GPT-4 is recommended for pseudo code elimination
            print(colored("\nWhich model do you want to use for Instruction generation?", "yellow"))
            print(colored("1. GPT-4", "green"))
            print(colored("2. GPT-3.5-turbo", "green"))
            model = input(colored("Enter your choice (1 or 2): ", "yellow")).strip()
            if model in ["1", "2"]:
                model =  "gpt-3.5-turbo-16k-0613" if model == "2" else "gpt-4"
            else:
                print(colored("Invalid input. Please enter either 1 or 2.", "red"))



    generate_instructions(model=model)

    # tell the user that they can review and change the instructions in the instructions.json file
    print(colored("\n\nINSTRUCTIONS GENERATED! YOU CAN REVIEW AND CHANGE THE INSTRUCTIONS IN THE 'user_instructions.txt' FILE BEFORE CONTINUING", "magenta"))

    # ask users how many pseudo code they want to generate
    num_pseudo_code = input(colored("\nHow many pseudo code do you want to generate? (type a number): ", "yellow"))

    model = ""
    while model == "":
            # tell user that GPT-4 is recommended for pseudo code elimination
            print(colored("\nGPT-4 is recommended for Pseudo Code generation", "green"))
            print(colored("\nWhich model do you want to use for Pseudo Code generation?", "yellow"))
            print(colored("1. GPT-4", "green"))
            print(colored("2. GPT-3.5-turbo", "green"))
            model = input(colored("Enter your choice (1 or 2): ", "yellow")).strip()
            if model in ["1", "2"]:
                model =  "gpt-3.5-turbo-16k-0613" if model == "2" else "gpt-4"
            else:
                print(colored("Invalid input. Please enter either 1 or 2.", "red"))

    generate_concurrently(num_runs=num_pseudo_code, model=model)

    print(colored("\n\nPSEUDO CODE FILES GENERATED! YOU CAN REVIEW AND CHANGE THE PSEUDO CODE IN THE 'pseudo_competitors' FOLDER", "magenta"))

    write_competitors_to_files(file_path="pseudo_competitors.json", folder_name="pseudo_competitors", older_folder_name="older_pseudo_competitors")


    # eliminating pseudo code
    model = ""
    while model == "":
            # tell user that GPT-4 is recommended for pseudo code elimination
            print(colored("\nGPT-4 is recomented for pseudo code elimination", "green"))
            print(colored("\nWhich model do you want to use for pseudo code elimination?", "yellow"))
            print(colored("1. GPT-4", "green"))
            print(colored("2. GPT-3.5-turbo", "green"))
            model = input(colored("Enter your choice (1 or 2): ", "yellow")).strip()
            if model in ["1", "2"]:
                model =  "gpt-3.5-turbo-16k-0613" if model == "2" else "gpt-4"
            else:
                print(colored("Invalid input. Please enter either 1 or 2.", "red"))

    print(colored("\nEliminating pseudo code...", "green"))
    eliminate(model=model)

    print(colored("\n\nPSEUDO CODE ELIMINATiON COMPLETE! YOU CAN REVIEW THE APPROVED PSEUDO CODE FILES THE 'winning_pseudo_competitors' FOLDER", "magenta"))

    def get_pseudo_code_numbers():
        numbers_to_generate = input(colored("\nWhich pseudo code do you want to generate Final Code for? (type a number or numbers seperated by commas): ", "yellow"))
        pseudo_code_numbers_to_generate = [int(number.strip()) for number in numbers_to_generate.split(",")]
        return pseudo_code_numbers_to_generate

    def process_pseudo_code_files(pseudo_code_numbers_to_generate, folder_name, model):
        with ThreadPoolExecutor() as executor:
            tasks = []
            for file_number in pseudo_code_numbers_to_generate:
                with open(os.path.join(folder_name, f"{file_number}.py"), "r") as f:
                    pseudo_code = f.read()
                tasks.append(executor.submit(final_code_responses, pseudo_code=pseudo_code, file_number=file_number, model=model))
            for task in tasks:
                task.result()

    def check_and_process_files(folder_name):
        print(colored("\nHere are the available pseudo code numbers: ", "green"))
        # tell the user where they can examine the pseudo code files
        print(colored(f"\nYou can examine the pseudo code files in the {folder_name} folder", "green"))
        file_numbers = [int(file_name[:-3]) for file_name in os.listdir(folder_name) if file_name.endswith('.py')]
        print(colored(f"{file_numbers}", "green"))
        pseudo_code_numbers_to_generate = get_pseudo_code_numbers()
        if any(number not in file_numbers for number in pseudo_code_numbers_to_generate):
            print(colored("Invalid input. Please choose a number or numbers seperated by commas from the list", "red"))
            return
        process_pseudo_code_files(pseudo_code_numbers_to_generate, folder_name, model)

    def reorganize_old_files(source_dir, target_dir):
        # Check if the source directory exists
        if not os.path.isdir(source_dir):
            print(f"Source directory {source_dir} does not exist. Please check the directory path.")
            return

        # Create the target directory if it doesn't already exist
        os.makedirs(target_dir, exist_ok=True)

        # Get a list of all existing folders in the target directory
        existing_folders = [name for name in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, name))]

        # Find the highest numbered folder that already exists
        if existing_folders:
            highest_number = max(int(folder) for folder in existing_folders if folder.isdigit())
        else:
            highest_number = 0

        # The new folder number will be one higher than the current highest
        new_folder_number = highest_number + 1

        # Create new target directory
        new_target_dir = os.path.join(target_dir, str(new_folder_number))
        os.makedirs(new_target_dir, exist_ok=True)

        # Move the existing files to the new folder
        for file_name in os.listdir(source_dir):
            shutil.move(os.path.join(source_dir, file_name), new_target_dir)

        # Recreate the source directory
        os.makedirs(source_dir, exist_ok=True)


    def ask_user_model():
        while True:
            # tell user that GPT-4 is recommended for pseudo code elimination
            print(colored("\nGPT-4 is recommended for Final Code generation", "green"))
            print(colored("\nWhich model do you want to use for Final Code generation?", "yellow"))
            print(colored("1. GPT-4", "green"))
            print(colored("2. GPT-3.5-turbo", "green"))
            model = input(colored("Enter your choice (1 or 2): ", "yellow")).strip()
            if model in ["1", "2"]:
                return "gpt-3.5-turbo-16k-0613" if model == "2" else "gpt-4"
            else:
                print(colored("Invalid input. Please enter either 1 or 2.", "red"))


    if os.stat("winning_pseudo_competitors.json").st_size != 0:
        write_competitors_to_files(file_path="winning_pseudo_competitors.json", folder_name="winning_pseudo_competitors", older_folder_name="older_winning_pseudo_competitors")
        open("winning_pseudo_competitors.json", "w").close()

        model = ask_user_model()
        print(colored(f"\n{model} is selected for Final Code generation", "green"))

        reorganize_old_files('final_code', 'older_final_code')
        check_and_process_files("winning_pseudo_competitors")
        print(colored("\n\n FINAL CODE FILES GENERATED! YOU CAN REVIEW THE FINAL CODE FILES IN THE 'Final_Code' FOLDER", "magenta"))

    elif os.stat("winning_pseudo_competitors.json").st_size == 0:
        print(colored("\nNo winning pseudo code to generate Final Code for", "red"))
        which_pseudo = input(colored("\nDo you wish to generate Final Code for any of the non-winning pseudo code? (y/n): ", "yellow"))
        if which_pseudo == "y":
            model = ask_user_model()
            print(colored(f"\n{model} is selected for Final Code generation", "green"))

            reorganize_old_files('final_code', 'older_final_code')
            check_and_process_files("pseudo_competitors")
        elif which_pseudo == "n":
            print(colored("\nNo Final Code generated", "red"))
            sys.exit()


elif args.auto:
    model = args.model
    num_pseudo_code = args.num
    print(colored(f"\n{model} is selected for generation. Will be generating {num_pseudo_code} pseudo code alternatives", "green"))
    
    generate_instructions(model=model)
    
    print(colored("\n\nINSTRUCTIONS GENERATED! YOU CAN REVIEW THE INSTRUCTIONS IN THE 'user_instructions.txt' FILE", "magenta"))
    if args.pause:
        input(colored("\nPress Enter to continue...", "yellow"))

    generate_concurrently(num_runs=num_pseudo_code, model=model)
    print(colored("\n\nPSEUDO CODE GENERATED! YOU CAN REVIEW THE PSEUDO CODE IN THE 'pseudo_competitors' FOLDER", "magenta"))

    eliminate(model=model)
    print(colored("\n\nPSEUDO CODE ELIMINATED! YOU CAN REVIEW THE ELIMINATED PSEUDO CODE IN THE 'winning_pseudo_competitors' FOLDER", "magenta"))



    def process_pseudo_code_files(pseudo_code_numbers_to_generate, folder_name, model):
        with ThreadPoolExecutor() as executor:
            tasks = []
            for file_number in pseudo_code_numbers_to_generate:
                with open(os.path.join(folder_name, f"{file_number}.py"), "r") as f:
                    pseudo_code = f.read()
                tasks.append(executor.submit(final_code_responses, pseudo_code=pseudo_code, file_number=file_number, model=model))
            for task in tasks:
                task.result()

    def check_and_process_files(folder_name):
        file_numbers = [int(file_name[:-3]) for file_name in os.listdir(folder_name) if file_name.endswith('.py')]
        print(colored(f"{file_numbers}", "green"))

        process_pseudo_code_files(file_numbers, folder_name, model)

    def reorganize_old_files(source_dir, target_dir):
        # Check if the source directory exists
        if not os.path.isdir(source_dir):
            print(f"Source directory {source_dir} does not exist. Please check the directory path.")
            return

        # Create the target directory if it doesn't already exist
        os.makedirs(target_dir, exist_ok=True)

        # Get a list of all existing folders in the target directory
        existing_folders = [name for name in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, name))]

        # Find the highest numbered folder that already exists
        if existing_folders:
            highest_number = max(int(folder) for folder in existing_folders if folder.isdigit())
        else:
            highest_number = 0

        # The new folder number will be one higher than the current highest
        new_folder_number = highest_number + 1

        # Create new target directory
        new_target_dir = os.path.join(target_dir, str(new_folder_number))
        os.makedirs(new_target_dir, exist_ok=True)

        # Move the existing files to the new folder
        for file_name in os.listdir(source_dir):
            shutil.move(os.path.join(source_dir, file_name), new_target_dir)

        # Recreate the source directory
        os.makedirs(source_dir, exist_ok=True)


    if os.stat("winning_pseudo_competitors.json").st_size != 0:
        write_competitors_to_files(file_path="winning_pseudo_competitors.json", folder_name="winning_pseudo_competitors", older_folder_name="older_winning_pseudo_competitors")
        open("winning_pseudo_competitors.json", "w").close()
        reorganize_old_files('final_code', 'older_final_code')
        check_and_process_files("winning_pseudo_competitors")
        print(colored("\n\n FINAL CODE FILES GENERATED! YOU CAN REVIEW THE FINAL CODE FILES IN THE 'Final_Code' FOLDER", "magenta"))

    elif os.stat("winning_pseudo_competitors.json").st_size == 0:
        print(colored("\nNo winning pseudo code to generate Final Code for", "red"))
        which_pseudo = input(colored("\nDo you wish to generate Final Code for any of the non-winning pseudo code? (y/n): ", "yellow"))
        if which_pseudo == "y":
            print(colored(f"\n{model} is selected for Final Code generation", "green"))

            reorganize_old_files('final_code', 'older_final_code')
            check_and_process_files("pseudo_competitors")
        elif which_pseudo == "n":
            print(colored("\nNo Final Code generated", "red"))
            sys.exit()




    