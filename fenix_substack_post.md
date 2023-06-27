# Title: Streamlining Research and Assisting with FenixAGI Mk1

## Introduction

FenixAGI Mk1 is an advanced AI assistant designed to revolutionize research and assistance tasks. Built on OpenAI's GPT-16k 3.5-turbo language model, FenixAGI Mk1 offers a range of functions that can aid researchers and help streamline their workflows. This Substack post provides a detailed overview of the `fenix.py` file, showcasing its structure, functionality, and usage instructions.

## File Structure

The `fenix.py` file acts as the core component of FenixAGI Mk1, powering its research-oriented functions and assistance capabilities. Here's a breakdown of its components:

### Libraries and Global Variables

The `fenix.py` file imports essential libraries such as `openai`, `json`, `os`, `pandas`, and `termcolor`. Additionally, it initializes critical global variables including the approved functions list, colors dictionary, and FenixState class, laying the foundation for FenixAGI Mk1's operations.

### FenixState Class

The `FenixState` class assumes the responsibility of capturing and retaining the state of the FenixAGI assistant. This includes preserving the conversation history, instructions, executed function calls, display response settings, operational mode, and approved functions, all of which allow for seamless interactions and personalized experiences.

### Helper Functions

To enhance its research capabilities and provide effective assistance, FenixAGI Mk1 incorporates several helper functions. These include `fenix_help()` for providing guidance, `save_fenix()` for saving the current state, `derezz_fnix()` for resetting the assistant, `ask_user()` for collecting user input, and `tell_user()` for delivering informative messages. These functions contribute to the efficiency of the assistant and enhance the overall user experience.

### Main Conversation Loop

The `run_conversation()` function serves as the entry point for FenixAGI Mk1's research and assistance capabilities. This function processes user input and utilizes the GPT-3.5-turbo language model to generate responses. If a function call is detected in the response, FenixAGI Mk1 executes the corresponding function based on the mode (manual or automatic) and user approval. The conversation history is updated with both user input and assistant responses, ensuring a continuous and interactive experience.

## Utilization Instructions

To utilize FenixAGI Mk1 for research and assistance tasks, follow these instructions:

1. **Setting up API Keys**: Obtain the necessary API keys before using FenixAGI Mk1:
   - BING_SEARCH_KEY: Access this key from the Bing Search API portal ([https://portal.azure.com/](https://portal.azure.com/#))
   - OPENAI_API_KEY: Obtain this key for the GPT-3.5-turbo-16k model by signing up at [https://platform.openai.com/signup](https://platform.openai.com/signup)

2. **Running FenixAGI Mk1**: Execute the `run_conversation()` function within the `fenix.py` file to initiate FenixAGI Mk1 and start the conversation loop.

3. **Interacting with FenixAGI Mk1**: Utilize the command line interface to communicate with FenixAGI Mk1. Input your messages after the `> ` prompt, and FenixAGI Mk1 will respond accordingly.
   - Special commands: FenixAGI Mk1 recognizes commands such as 'exit', 'quit', '~', '1', and '2' for various operations. Utilize these commands to control FenixAGI Mk1's behavior and settings during the conversation.

4. **Expanding Functionality**: FenixAGI Mk1 supports extensibility. Expand its capabilities by adding new functions to the `approved_functions` list and corresponding entries to the `function_descriptions` list. This enables customization and the incorporation of additional research and assistance functionalities.

5. **Saving and Restoring State**: FenixAGI Mk1 automatically saves its state to the `fenix_state.json` file. Upon relaunch, FenixAGI Mk1 checks for this file and restores the previous state if available. You can manually reset FenixAGI Mk1 and the state by entering '0' as your user input.

## Conclusion

FenixAGI Mk1, powered by OpenAI's GPT-3.5-turbo language model, is a powerful AI assistant designed to streamline research and provide assistance. With its research-oriented functions, personalization capabilities, and extensibility, FenixAGI Mk1 empowers researchers and enhances their workflow. Fork the FenixAGI Mk1 repository on Replit and experience the transformative potential it holds.

You can fork and run Fenix locally or on Replit at [https://replit.com/@p4r7h/FenixAGI-Mk-1-Function-Caller?v=1](https://replit.com/@p4r7h/FenixAGI-Mk-1-Function-Caller?v=1)

For any inquiries, feedback, or collaboration opportunities, feel free to reach out to Parth Patil, the creator of FenixAGI Mk1, on LinkedIn at [https://www.linkedin.com/in/parthspatil/](https://www.linkedin.com/in/parthspatil/).

