import tiktoken

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
def count_tokens(text):
    return len(encoding.encode(text))

to_be_counted = """


"""

print("token count is: " , count_tokens(to_be_counted))