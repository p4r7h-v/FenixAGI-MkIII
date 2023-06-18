import speech_recognition as sr

def transcribe_speech_to_text():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Please say something...")
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio)
        print("You said: ", text)
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Error with speech recognition; {e}")

speech_to_text = transcribe_speech_to_text()