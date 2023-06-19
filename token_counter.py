import tiktoken

def count_tokens(text, model_name="gpt-4-0613"):
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(text))
