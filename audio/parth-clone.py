import os
from dotenv import load_dotenv
import openai
from elevenlabs import voices, generate, set_api_key
import simpleaudio as sa
import soundfile
import wave
import time

def play_audio(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.environ['xi-api-key'])


# Fetch all available voices
all_voices = voices()
#print(all_voices)



if __name__ == "__main__":
    # Find the voice
    voice_id = next(
    (voice.voice_id for voice in all_voices
    if voice.name == 'Parth TTS'), None)
    print(voice_id)
    # Generate audio
    audio = generate(
                text = "I am Fenix, student of the Room of Spirit and Time.",
                voice=voice_id,
                model="eleven_monolingual_v1"
            )

    # Write audio data to .wav file
    with open('audio.wav', 'wb') as f:
        f.write(audio)
      
    file_path = "audio.wav"

    # Read and rewrite the file with soundfile
    data, samplerate = soundfile.read(file_path)
    soundfile.write(file_path, data, samplerate)
    
    # Play audio file
    play_audio(file_path)
    
    # Save audio to a file
    file_path = 'audio.wav'
    soundfile.write(file_path, audio, 22050, 'PCM_24')
    
    # Play audio
    play_audio(file_path)