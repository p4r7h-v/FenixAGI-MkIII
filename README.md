# FenixAGI MkII: Advanced AI Assistant

Fenix A.G.I. Mark-III is an advanced AI assistant designed to revolutionize project management. Built by Parth and powered by OpenAI's GPT-16k 3.5-turbo language model, FenixAGI can assist users in a wide array of tasks including file operations, web scraping, data visualization, and more.

## Features

- **Interactive Voice Assistant**: FenixAGI supports voice interaction, with the ability to switch between different voices.
- **Customizable**: You can easily extend FenixAGI's functionality by adding new functions to the `approved_functions` list and corresponding entries to the `function_descriptions` list.
- **Learning Capabilities**: FenixAGI can learn from user feedback and revise its instructions to improve performance over time.
- **Powered by OpenAI**: FenixAGI utilizes the powerful GPT-16k 3.5-turbo language model by OpenAI.

## Getting Started

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/p4r7h-v/FenixAGI-MkII
   ```
2. Navigate to the project directory:
   ```
   cd FenixAGI-MkII
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### API Key Setup

Fenix uses three API keys for its functionality. Follow the instructions below to set up the required API keys:

- **Bing API Key**:
  - Obtain a Bing API Key from the [Microsoft Azure portal](https://www.microsoft.com/en-us/bing/apis/bing-web-search-api).
  - Set the obtained API Key as the `BING_API_KEY` environment variable.

- **OpenAI API Key**:
  - Sign up for an account on the [OpenAI website](https://platform.openai.com).
  - Generate an API Key from the API section of your OpenAI account.
  - Set the generated API Key as the `OPENAI_API_KEY` environment variable.

- **ElevenLabs API Key (optional)**:
  - Visit the [ElevenLabs website](https://elevenlabs.orbit-experiments.com/) and create an account.
  - Generate an API Key from your ElevenLabs account.
  - Set the generated API Key as the `xi-api-key` environment variable.

### Usage

1. Run Fenix:
   ```
   python fenix.py
   ```
2. Follow the prompts and interact with Fenix by typing your queries or commands.

While running, FenixAGI accepts a variety of commands to guide its behavior:

- 'v': Toggle voice modes.
- 'a': Toggle between automatic and manual mode for function execution.
- 'd': Toggle display of the assistant's responses.
- 'e' or ' ' (spacebar): Records the user's voice for 5 seconds and transcribes it. The transcription is then used as the user's input.
- 'r': Reset FenixAGI to a default state, clearing the conversation history and meta instructions.
- 'exit' or 'quit': Terminate the session and save the current state of FenixAGI.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
