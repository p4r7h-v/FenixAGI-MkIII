import guidance
import re
from termcolor import colored
import openai
import os
import diskcache
import pathlib
import requests
import html
from urllib.parse import urlparse
import urllib.parse
import io
import html
import html.parser

# Load your OpenAI API key from an environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

# we use GPT-4 here, but you could use gpt-3.5-turbo as well
guidance.llm = guidance.llms.OpenAI("gpt-4")


# a custom function we will call in the guidance program
def parse_best(prosandcons, strategies):
  best = int(re.findall(r'Best=(\d+)', prosandcons)[0])
  best -= 1
  return strategies[best]


# define the guidance program using role tags (like `{{#system}}...{{/system}}`)
generate_strategies = guidance('''
{{#system~}}
You are a helpful assistant.
{{~/system}}

{{! generate 3 potential ways to accomplish a goal }}
{{#block hidden=True}}
{{#user~}}
I want to {{goal}}.
{{~! generate potential strategies ~}}
Can you please generate one strategy for how to accomplish this?
Please make the strategy very short, at most one line.
{{~/user}}

{{#assistant~}}
{{gen 'strategies' n=3 temperature=1.0 max_tokens=500}}
{{~/assistant}}
{{/block}}
''')

generate_pros_and_cons = guidance('''
{{#system~}}
You are a helpful assistant.
{{~/system}}

{{! generate pros and cons for each approach and select the best strategy }}
{{#block hidden=True}}
{{#user~}}
I want to {{goal}}.

Can you please comment on the pros and cons of each of the following strategies, and then pick the best strategy? Make sure you index at 1 not 0.
---{{#each strategies}}
Generated strategies {{@index}}: {{this}}{{/each}}
---
Please discuss each strategy very briefly (one line for pros, one for cons) and end by saying Best=X, where X is the best strategy.
{{~/user}}

{{#assistant~}}
{{gen 'prosandcons' temperature=0.0 max_tokens=500}}
{{~/assistant}}
{{/block}}
''')

generate_strategy = guidance('''
{{#system~}}
You are a helpful assistant.
{{~/system}}

{{! generate a strategy to accomplish the given goal }}
{{#user~}}
I want to {{goal}}.
{{~! Create a strategy }}
Here is my strategy:
{{parse_best prosandcons strategies}}
Please elaborate on this strategy, and tell me how to best accomplish it. Be concise and actionable.
{{~/user}}

Here is your strategy:
{{#assistant~}}
{{gen 'strategy' max_tokens=1000}}
{{~/assistant}}
''')


def main():
  while True:
    user_task = input("Enter a task or goal: ")
    # Execute the program for a specific goal
    print("Generating strategies...")
    generated_strategies = generate_strategies(goal=user_task, )
    print(colored("Goal: " + str(generated_strategies['goal']), "light_green"))
    print(colored("Strategies: ", "light_magenta"))
    for i, strategy in enumerate(generated_strategies['strategies'], 1):
      print(colored("Strategy {}: {}".format(i, strategy), "light_magenta"))
    print("Generating pros and cons...")
    generated_pros_and_cons = generate_pros_and_cons(
      goal=user_task, strategies=generated_strategies['strategies'])
    print(
      colored("Pros and Cons: " + str(generated_pros_and_cons['prosandcons']),
              "light_magenta"))
    print("Generating strategy...")
    generated_strategy = generate_strategy(
      goal=user_task,
      strategies=generated_strategies['strategies'],
      prosandcons=generated_pros_and_cons['prosandcons'],
      parse_best=parse_best  # a custom python function we call in the program
    )
    print(
      colored("Strategy: " + str(generated_strategy['strategy']),
              "light_cyan"))


if __name__ == "__main__":
  main()

import urllib.parse
import io
import html
import html.parser

# Load your OpenAI API key from an environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

# we use GPT-4 here, but you could use gpt-3.5-turbo as well
guidance.llm = guidance.llms.OpenAI("gpt-4")


# a custom function we will call in the guidance program
def parse_best(prosandcons, strategies):
  best = int(re.findall(r'Best=(\d+)', prosandcons)[0])
  best -= 1
  return strategies[best]


# define the guidance program using role tags (like `{{#system}}...{{/system}}`)
generate_strategies = guidance('''
{{#system~}}
You are a helpful assistant.
{{~/system}}

{{! generate 3 potential ways to accomplish a goal }}
{{#block hidden=True}}
{{#user~}}
I want to {{goal}}.
{{~! generate potential strategies ~}}
Can you please generate one strategy for how to accomplish this?
Please make the strategy very short, at most one line.
{{~/user}}

{{#assistant~}}
{{gen 'strategies' n=3 temperature=1.0 max_tokens=500}}
{{~/assistant}}
{{/block}}
''')

generate_pros_and_cons = guidance('''
{{#system~}}
You are a helpful assistant.
{{~/system}}

{{! generate pros and cons for each approach and select the best strategy }}
{{#block hidden=True}}
{{#user~}}
I want to {{goal}}.

Can you please comment on the pros and cons of each of the following strategies, and then pick the best strategy? Make sure you index at 1 not 0.
---{{#each strategies}}
Generated strategies {{@index}}: {{this}}{{/each}}
---
Please discuss each strategy very briefly (one line for pros, one for cons) and end by saying Best=X, where X is the best strategy.
{{~/user}}

{{#assistant~}}
{{gen 'prosandcons' temperature=0.0 max_tokens=500}}
{{~/assistant}}
{{/block}}
''')

generate_strategy = guidance('''
{{#system~}}
You are a helpful assistant.
{{~/system}}

{{! generate a strategy to accomplish the given goal }}
{{#user~}}
I want to {{goal}}.
{{~! Create a strategy }}
Here is my strategy:
{{parse_best prosandcons strategies}}
Please elaborate on this strategy, and tell me how to best accomplish it. Be concise and actionable. Focus on the atomic unit of the strategy's success.
{{~/user}}

Here is your strategy:
{{#assistant~}}
{{gen 'strategy' max_tokens=1000}}
{{~/assistant}}
''')


def main():
  while True:
    user_task = input("Enter a task or goal: ")
    # Execute the program for a specific goal
    print("Generating strategies...")
    generated_strategies = generate_strategies(goal=user_task, )
    print(colored("Goal: " + str(generated_strategies['goal']), "light_green"))
    print(colored("Strategies: ", "light_magenta"))
    for i, strategy in enumerate(generated_strategies['strategies'], 1):
      print(colored("Strategy {}: {}".format(i, strategy), "light_magenta"))
    print("Generating pros and cons...")
    generated_pros_and_cons = generate_pros_and_cons(
      goal=user_task, strategies=generated_strategies['strategies'])
    print(
      colored("Pros and Cons: " + str(generated_pros_and_cons['prosandcons']),
              "light_magenta"))
    print("Generating strategy...")
    generated_strategy = generate_strategy(
      goal=user_task,
      strategies=generated_strategies['strategies'],
      prosandcons=generated_pros_and_cons['prosandcons'],
      parse_best=parse_best  # a custom python function we call in the program
    )
    print(
      colored("Strategy: " + str(generated_strategy['strategy']),
              "light_cyan"))


if __name__ == "__main__":
  main()
