import pyttsx3

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.say(text)
    engine.runAndWait()

# Example usage:
text_to_speech("Hello, I am your text-to-speech converter.")