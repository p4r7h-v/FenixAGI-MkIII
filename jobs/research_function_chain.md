# Research Function Chain

## Companies to Explore:

- OpenAI
- Google DeepMind
- HuggingFace
- Anthropic
- Poe/Perplexity
- Langchain
- Streamlit
- Snowflake
- Databricks
- Midjourney
- Microsoft

## Function Chain:

1. `bing_search_save`: Perform web searches using Bing to gather information about the specific companies.
2. `scrape_website`: Scrape the websites of the companies to extract relevant information.
3. `create_code_search_csv`: Create a CSV file to track search results and save any code snippets or open-source projects related to the companies.
4. `search_codebase`: Use the `search_codebase` function to search for specific keywords related to the companies' research projects, tools, or libraries.
5. `read_file`: Read the contents of the CSV file and any code files obtained from the code search to access the collected information.
6. `create_markdown_file`: Create a Markdown file to document the findings and key details about the companies and their research endeavors.
7. `convert_markdown_to_html`: Convert the Markdown file to HTML for easy sharing or publishing.