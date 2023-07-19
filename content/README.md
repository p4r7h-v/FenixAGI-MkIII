# Fenix

Fenix A.G.I. Mark-II is an advanced AI assistant built by Parth. Fenix is designed to assist users in various tasks using OpenAI's GPT-3.5-turbo language model.

## Getting Started

To get started with Fenix, follow the steps below:

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/fenix.git
   ```
2. Navigate to the project directory:
   ```
   cd fenix
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

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
