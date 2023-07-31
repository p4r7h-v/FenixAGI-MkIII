# FileOperations.py

import os
import json
from FenixState import FenixState


class FileOperations:
    @staticmethod
    def save_fenix(fenix_state):  # Add fenix_state as a parameter
        with open("fenix_state.json", "w") as f:
            json.dump(fenix_state.__dict__, f)
            return "Fenix State Saved."

    @staticmethod
    def rez_fenix(filename="fenix_state.json"):
        global fenix_state  # Declare the variable as global
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


    @staticmethod
    def derez_fenix(filename="fenix_state.json"):
        # Delete the fenix_state.json file
        if os.path.exists("fenix_state.json"):
            os.remove("fenix_state.json")
            return "Fenix State Derezzed."