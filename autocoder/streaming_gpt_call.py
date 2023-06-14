
import openai

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    stream=True,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"""{user_input}"""}
    ]
)

responses = ''

# Process each chunk
for chunk in response:
    if "role" in chunk["choices"][0]["delta"]:
        continue
    elif "content" in chunk["choices"][0]["delta"]:
        r_text = chunk["choices"][0]["delta"]["content"]
        responses += r_text
        print(r_text, end='', flush=True)