function_descriptions = [


    {
        "name": "write_to_file",
        "description": "Use this function to write code to appropiate full file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The full file path to write the provided content to",
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
        "name": "read_from_file",
        "description": "Use this function to read the content of files",
        "parameters": {
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
        "name": "delete_file",
        "description": "Use this function to delete files",
        "parameters": {
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
    }

]
