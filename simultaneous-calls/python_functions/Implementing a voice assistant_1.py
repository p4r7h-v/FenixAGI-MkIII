import speech_recognition as sr

def voice_assistant():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    print("Please speak something...")

    with microphone as source:
        try:
            # Adjust the noise level
            recognizer.adjust_for_ambient_noise(source)
            # Record the audio
            audio = recognizer.listen(source)
        except Exception as e:
            print("Error while recording audio:", e)
            return None

    try:
        # Convert the speech to text using Google Speech Recognition API
        speech_text = recognizer.recognize_google(audio)
        print(f"You said: {speech_text}")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand your speech")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    return speech_text


if __name__ == "__main__":
    voice_assistant()