import random

def simple_chatbot():
    responses = {
        "greetings": ["Hello!", "Hi!", "Hey!", "Hi there!"],
        "farewells": ["Goodbye!", "See you later!", "Bye!"],
        "how_are_you": ["I'm doing well, thank you!", "I'm good, how about you?", "Not too bad!"],
        "unknown": ["I'm not sure about that.", "Interesting, let's talk about something else.", "I don't have an answer to that."]
    }

    while True:
        user_input = input("You: ").lower()
        if user_input in ["quit", "exit", "bye", "goodbye"]:
            print(random.choice(responses["farewells"]))
            break

        if "hello" in user_input or "hi" in user_input or "hey" in user_input:
            print("Chatbot:", random.choice(responses["greetings"]))
        elif "how are you" in user_input or "how're you" in user_input or "how is it going" in user_input:
            print("Chatbot:", random.choice(responses["how_are_you"]))
        else:
            print("Chatbot:", random.choice(responses["unknown"]))

if __name__ == "__main__":
    simple_chatbot()