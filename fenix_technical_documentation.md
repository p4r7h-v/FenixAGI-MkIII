# FenixAGI Mk1 Technical Documentation

## Introduction

FenixAGI Mk1 is an advanced AI assistant designed to revolutionize project management. Built on OpenAI's GPT-16k 3.5-turbo language model, FenixAGI Mk1 offers a range of functions such as codebase searches, web scraping, file management, and more. This technical documentation provides an overview of the `fenix.py` file structure, functionality, and usage instructions.

## File Overview

The `fenix.py` file contains the main functionality for running the Fenix assistant. Here's an overview of its components:

### Libraries and Global Variables

- The necessary libraries such as `openai`, `json`, `os`, `pandas`, and `termcolor` are imported.
- The global variables include the approved functions list, colors dictionary, and FenixState class.

### FenixState Class

- The `FenixState` class stores the state of the Fenix assistant, including conversation history, instructions, function calls, display response settings, operational mode, and approved functions.

### Helper Functions

- Several helper functions, such as `fenix_help()`, `save_fenix()`, `derezz_fnix()`, `ask_user()`, and `tell_user()`, are defined to handle various aspects of the assistant's operation.

### Main Conversation Loop

- The `run_conversation()` function initializes the Fenix assistant and starts the main conversation loop.
- User input is processed and passed to the GPT-3.5-turbo language model for response generation.
- The assistant's responses are analyzed, and if a function call is issued, it is executed based on the mode (manual or automatic) and user approval.
- The conversation history is updated with the user input and assistant responses.
- The conversation loop continues until the user chooses to exit.

## Usage Instructions

1. **Setting Up API Keys**: Before using Fenix, ensure you have acquired the necessary API keys:
   - BING_SEARCH_KEY: Obtain this key from the Bing Search API portal at [https://portal.azure.com/](https://portal.azure.com/#).
   - OPENAI_API_KEY: Acquire this key for the GPT-3.5-turbo-16k model at [https://platform.openai.com/signup](https://platform.openai.com/signup).

2. **Running Fenix**: To run Fenix, execute the `run_conversation()` function in the `fenix.py` file. This will initialize the assistant and start the conversation loop.

3. **Interaction with Fenix**: Communicate with Fenix through the command line interface. Enter your messages after the `> ` prompt, and Fenix will respond accordingly.
   - Special commands: Fenix recognizes special commands such as 'exit', 'quit', '~', '1', and '2' for various operations. Use these commands to control Fenix's behavior and settings during the conversation.

4. **Extending Functionality**: Fenix is designed to be extensible. By adding new functions to the `approved_functions` list and corresponding entries to the `function_descriptions` list, you can expand Fenix's capabilities with custom functions.

5. **Saving and Restoring State**: Fenix automatically saves its state to the `fenix_state.json` file. When running Fenix again, it checks for this file and restores the previous state if available. You can manually derez Fenix and reset the state by entering '0' as the user input.

6. **Updating Instructions**: Fenix learns from user feedback and can revise its instructions for improved performance. Enter '~' as the user input to update the instructions based on the conversation history and critique the assistant's performance.

## Conclusion

This technical documentation provides an overview of the `fenix.py` file and instructions for using FenixAGI Mk1. With its versatile functions, adaptability, and extensibility, Fenix is a powerful tool for data scientists and engineers interested in autonomous agents and efficient information retrieval. Feel free to explore and expand upon Fenix to streamline your project management tasks.

Note: This documentation may not cover all the details of the internal workings of Fenix. For more in-depth information, refer to the code comments and review the LangChain library documentation used by Fenix.

For any further assistance or inquiries, reach out to Fenix's creator, Parth Patil, on LinkedIn at [https://www.linkedin.com/in/parthspatil/](https://www.linkedin.com/in/parthspatil/).