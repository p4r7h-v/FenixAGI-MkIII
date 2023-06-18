from pydub import AudioSegment
from pydub.playback import play as pydub_play
from elevenlabs import voices, generate, set_api_key

# Point to the correct FFmpeg executable
AudioSegment.converter = "C:/FFmpeg/bin/ffmpeg.exe"

# Set the API Key
set_api_key(os.environ['xi-api-key'])

# Fetch all available voices
all_voices = voices()
print(all_voices)
# Find the 'Dip Sith' voice
dip_sith_voice_id = next((voice.voice_id for voice in all_voices if voice.name == 'Dip Sith:  Trained with famous Dark Side Phrases'), None)

if dip_sith_voice_id:
    # Use the 'Dip Sith' voice to generate speech
    audio = generate(
        text="Greetings, User! I am Codified Likeness Utility (C.L.U.), an assistant on this Twitch channel. This channel is dedicated to showcasing programming with GPT-4, a powerful language model, created by OpenAI.",
        voice=dip_sith_voice_id,
        model="eleven_monolingual_v1"
    )

    # Write audio data to .wav file
    with open('audio.wav', 'wb') as f:
        f.write(audio)

    # Play the audio file
    audio_to_play = AudioSegment.from_wav('audio.wav')
    pydub_play(audio_to_play)
else:
    print('Dip Sith voice not found.')
