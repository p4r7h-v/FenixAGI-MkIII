import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 125)  # Adjust the speaking rate (default is 200)
    engine.say(text)
    engine.runAndWait()

# Example usage:
text_to_speech("Hello, I am a Python text-to-speech converter.")