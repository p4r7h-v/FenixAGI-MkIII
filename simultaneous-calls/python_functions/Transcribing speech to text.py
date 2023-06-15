from google.cloud import speech_v1p1beta1 as speech
import io

def transcribe_speech_to_text(file_path, api_key_file):
    """
    Transcribe speech to text from an audio file using Google Speech-to-Text API.

    Args:
        file_path (str): Path to the audio file to transcribe.
        api_key_file (str): Path to the API key JSON file.

    Returns:
        str: Transcribed text.
    """

    # Set Google Application credentials
    import os
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = api_key_file

    # Create a speech client
    client = speech.SpeechClient()

    # Read the binary data of the audio file
    with io.open(file_path, 'rb') as audio_file:
        content = audio_file.read()

    # Define an audio object with the binary data
    audio = speech.RecognitionAudio(content=content)

    # Configure the API request parameters
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Make the API request
    response = client.recognize(config=config, audio=audio)

    # Extract the transcribed text from the response
    transcript = ''
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return transcript