import speech_recognition as sr
import pyttsx3

def voice_assistant():
    recognizer = sr.Recognizer()
    engine = pyttsx3.init()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language="en-US")
        print(f"User said: {command}")
        
        # Process the command and generate a response
        response = process_command(command)
        print(f"Assistant said: {response}")
        
        # Speak the response
        engine.say(response)
        engine.runAndWait()

    except Exception as e:
        print("Failed to recognize the command.")
        print(e)

def process_command(command):
    response = ""

    # Example for processing a command
    if "hello" in command.lower():
        response = "Hello! How can I help you?"

    else:
        response = "I'm sorry, I didn't understand that."

    return response

if __name__ == "__main__":
    voice_assistant()