function_descriptions = [

    {
        "name": "create_code_search_csv",
        "description": "Use this function to create a csv of all python functions in a directory",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_name": {
                    "type": "string",
                    "description": "The directory path to search for python functions, defaults to current directory:'.'",
                },
            },
            "required": ["folder_name"],
        },
    },

    {
        "name" : "write_file",
        "description" : "writes the provided content to the provided file path",
        "parameters" : {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The full file path to write the provided content to. Use this only once per file",
                },
                "content": {
                    "type": "string",
                    "description": "The code to write to the provided file path",
                },
            },
            "required": ["file_path", "content"],
        },
    },

    {
        "name" : "read_file",
        "description" : "reads the content from the provided file path",
        "parameters" : {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to read the content from",
                },
            },
            "required": ["file_path"],
        },
    },

    {
        "name" : "delete_file",
        "description" : "deletes the file at the provided file path",
        "parameters" : {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to delete",
                },
            },
            "required": ["file_path"],
        },
    },

    {
        "name": "create_directory",
        "description": "Use this function to create directories",
        "parameters": {
            "type": "object",
            "properties": {
                "directory_path": {
                    "type": "string",
                    "description": "The directory path to create",
                },
            },
            "required": ["directory_path"],
        },
    },

    {
        "name": "ask_user_for_additional_information",
        "description": "Use this function to ask the user for additional information when needed",
        "parameters": {
            "type": "object",
            "properties": {
                "question_for_additional_information": {
                    "type": "string",
                    "description": "The question to ask the user for additional information",
                },
            },
            "required": ["question_for_additional_information"],
        },
    },

    {
        "name": "search_codebase",
        "description": "Search the codebase dataframe of python functions for the function with the most similar results",
        "parameters": {
            "type": "object",
            "properties": {
                "code_query": {
                    "type": "string",
                    "description": "The code_query to search for",
                },
                "n": {
                    "type": "integer",
                    "description": "The number of results to return",
                },
            },
            "required": ["code_query", "n"],
        },
    },
    {
        "name": "bing_search_save",
        "description": "Search bing and save the results to a csv",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search for",
                }
            },
            "required": ["query"],
        }
    },
    {
        "name": "scrape_website",
        "description": "Scrape or read a website and save the results to a txt file",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The url to scrape or read",
                }
            },
            "required": ["url"],
        }
    },
    {
        "name": "save_fenix",
        "description": "Save the current state of Fenix",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "",
                }
            },
        },
    },

    {
        "name": "count_tokens_in_string",
        "description": "Count the number of tokens in a string",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to count the number of tokens in",
                },
            },
            "required": ["text"],
        },
    },

    {
        "name": "count_tokens_in_file",
        "description": "Count the number of tokens in a file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to count the number of tokens in",
                },
            },
            "required": ["file_path"],
        },
    },

    {
        "name": "bing_search_save",
        "description": "Search bing and save the results to a csv",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to search for",
                }
            },
            "required": ["query"],
        }
    },

    {
        "name": "create_markdown_file",
        "description": "Create a markdown file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The file path to create the markdown file",
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the markdown file",
                },
            },
            "required": ["file_path", "content"],
        },
    },

    {
        "name": "fenix_help",
        "description": "Get help on Fenix",
        "parameters": {
            "type": "object",
            "properties": {
                "help_query": {
                    "type": "string",
                    "description": "'how to use fenix' or 'what can fenix do' or 'what is fenix' or 'what is fenix used for' or 'who created fenix' or 'who is the creator",
                },
            },
            "required": ["help_query"],  
        },
    },
    
      
]
