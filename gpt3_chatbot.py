from fastapi import FastAPI
from pydantic import BaseModel
import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

app = FastAPI()


class ChatRequest(BaseModel):
    conversation: list


class ChatResponse(BaseModel):
    message: str


@app.post("/chat/")
def chat(request: ChatRequest):
    # Get the conversation from the request
    conversation = request.conversation

    # Convert conversation to OpenAI format
    messages = [{"role": msg["role"], "content": msg["content"]} for msg in conversation]

    # Generate response using GPT-3
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=messages,
        max_tokens=100,
        temperature=0.7,
        n = 1
    )

    # Extract the generated reply from the response
    reply = response.choices[0].text.strip()

    # Construct the response object
    chat_response = ChatResponse(
        message=reply
    )

    return chat_response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
