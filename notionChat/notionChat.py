import openai
import guidance
from termcolor import colored
import json
import os
import re
import time
import requests
from notion_client import Client

#Agent Name
agent_name = "Fenix"

# Load your notion API key from an environment variable
notion_api_key = os.getenv('notion_api_key')
notion_database_id = os.getenv('notion_database_id')
notion = Client(auth=notion_api_key)

# Load your OpenAI API key from an environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# we use GPT-4 here, but you could use gpt-3.5-turbo as well
guidance.llm = guidance.llms.OpenAI("gpt-4")


# a custom function we will call in the guidance program
def parse_best(prosandcons, options):
  best = int(re.findall(r'Best=(\d+)', prosandcons)[0])
  return options[best]


# define the guidance program using role tags (like `{{#system}}...{{/system}}`)
create_project = guidance('''
{{#system~}}
You are a helpful assistant.
{{~/system}}

{{! generate five unique ways to accomplish a goal }}
{{#block hidden=True}}
{{#user~}}
I want to {{goal}}.
{{~! generate potential options ~}}
Can you please generate one option for how to accomplish this?
Please make the option very short, at most one line.
{{~/user}}

{{#assistant~}}
{{gen 'options' n=5 temperature=1.0 max_tokens=500}}
{{~/assistant}}
{{/block}}

{{! generate pros and cons for each option and select the best option }}
{{#block hidden=True}}
{{#user~}}
I want to {{goal}}.

Can you please comment on the pros and cons of each of the following options, and then pick the best option?
---{{#each options}}
Option {{@index}}: {{this}}{{/each}}
---
Please discuss each option very briefly (one line for pros, one for cons), and end by saying Best=X, where X is the best option.
{{~/user}}

{{#assistant~}}
{{gen 'prosandcons' temperature=0.0 max_tokens=500}}
{{~/assistant}}
{{/block}}

{{! generate a project to accomplish the chosen option }}
{{#user~}}
I want to {{goal}}.
{{~! Create a project }}
Here is my project:
{{parse_best prosandcons options}}
Please elaborate on this project, and tell me how to best accomplish it. Format the response as a comma-separated list of blocks in Notion API's block object format. Use only the following block types: ("paragraph"","to_do","heading_1","heading_2","heading_3").
{{~/user}}

Here is your project:
{{#assistant~}}
{{gen 'project' max_tokens=4000}}
{{~/assistant}}

{{! generate a name for the project }}
{{#user~}}
Give the project a name. Don't use JSON syntax.
{{~/user}}

Here is your project's name:
{{#assistant~}}
{{gen 'project_name' max_tokens=100}}
{{~/assistant}}

{{! generate 3 different tags for the project }}
{{#user~}}
Give the project a descriptive tag.
{{~/user}}
 
Here is your project's descriptive tag:
{{#assistant~}}
{{gen 'project_tags' n=3 max_tokens=100}}
{{~/assistant}}
''')


# Create a new Notion page with a content parameter
def create_notion_page(database_id, page_title):
  url = "https://api.notion.com/v1/pages"
  headers = {
    "Authorization":
    "Bearer " + notion_api_key,  # Add your Notion API key here
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
  }

  # add the body to the data
  data = {
    "parent": {
      "database_id": database_id
    },
    "created_time": time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.localtime()),
    "properties": {
      "Name": {
        "title": [{
          "text": {
            "content": page_title
          }
        }]
      },
      "Tags": {
        "type": "multi_select",
        "multi_select": [{
          "name": "OpenAI"
        }, {
          "name": "Notion"
        }]
      }
    }
  }

  try:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
  except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
    print(f"Response content: {response.content}")
    return None

  print(
    colored(f"Page {page_title} created in Notion database {database_id}",
            "green"))
  json_response = response.json()
  return json_response.get("id")


# Get Notion page
def get_notion_page(page_id):
  url = f"https://api.notion.com/v1/pages/{page_id}"
  headers = {
    "Authorization": f"Bearer {notion_api_key}",
    "Notion-Version": "2022-06-28"
  }
  print(f"Request URL: {url}")

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status(
    )  # This will raise an exception if the response contains an error status code
    page = response.json()
    #print(json.dumps(page, indent=4))  # Pretty-print the JSON response
    #print the url of the page
    print(colored(f"Page URL: {page['url']}", "green"))
    return page_id
  except Exception as e:
    print(f"Error retrieving Notion page: {e}")


def append_to_notion_page(plan, page_id):
  # Create a list to store the JSON objects
  json_objects = []

  # Iterate through each object in plan
  for obj in plan:
    # Append each object as a JSON dictionary
    json_objects.append(obj)
    print(type(obj))
    print(obj)

   # Iterate over each JSON object
  for obj in json_objects:
      try:
          block_type = obj.get('type', None)
          if isinstance(block_type, dict):
              block_type = block_type.get('type', None)
          print(block_type)
  
          if block_type == 'to_do':
              response = notion.blocks.children.append(
                  block_id=page_id,
                  children=[{
                      "object": "block",
                      "type": "to_do",
                      "to_do": {
                          "rich_text": [{
                              "type": "text",
                              "text": {
                                  "content": obj['to_do']['text'][0]['text']['content']
                              }
                          }],
                          "checked": obj['to_do'].get('checked', False)
                      }
                  }])
          elif block_type == 'paragraph':
              response = notion.blocks.children.append(
                  block_id=page_id,
                  children=[{
                      "object": "block",
                      "type": "paragraph",
                      "paragraph": {
                          "rich_text": [{
                              "type": "text",
                              "text": {
                                  "content": obj['paragraph']['text'][0]['text']['content']
                              }
                          }]
                      }
                  }])
          # Add more conditions for other block types here
  
          print(f"Block {obj} added to Notion page {page_id}")
      except Exception as e:
          print(f"Error adding block to Notion page: {e}")


def main(user_task):
  # Execute the program for a specific goal
  out = create_project(
    goal=user_task,
    parse_best=parse_best  # a custom python function we call in the program
  )
  print(colored("Goal: " + str(out['goal']), "yellow"))
  print(colored("Options: " + str(out['options']), "green"))
  print(colored("Pros and Cons: " + str(out['prosandcons']), "cyan"))
  #print(colored("Project: " + str(out['project']), "blue"))
  print(colored("Project Name: " + str(out['project_name']), "magenta"))
  print(colored("Project Tags: " + str(out['project_tags'])))

  # Create a new Notion page
  page_title = str(out['project_name'])
  page_id = create_notion_page(notion_database_id, page_title)
  print(colored(f"Project Tags: {out['project_tags']}", "magenta"))

  if page_id:
    print("Page ID: " + page_id)
    project = out['project']
    # Enclose the JSON array in square brackets
    project_json = f"[{project}]"

    # Parse the JSON array
    json_list = json.loads(project_json)

    # Append each block to the page
    append_to_notion_page(json_list, page_id)
    get_notion_page(page_id)
  else:
    print("Failed to create Notion page")


if __name__ == '__main__':
  user_task = ""
  print(
    colored("User Instructions for a task. When finished, enter 'done'.",
            "cyan"))
  while True:
    line = input(colored("> ", "cyan"))
    if line == "done":
      break
    user_task += line + "\n"
  main(user_task)
