import pyttsx3
import simpleaudio as sa
import soundfile
from elevenlabs import voices, generate, set_api_key
import re
import tenacity
import openai
import os

# set the eleven labs api key
set_api_key(os.environ['xi-api-key'])


class VoiceAssistant:
    def __init__(self, voice_mode="pyttsx3"):
        self.voice_mode = voice_mode
        # Check if voices are available otherwise use pyttsx3
        try:    
            all_voices = voices()
            self.voice_id = next(
                (voice.voice_id for voice in all_voices
                if voice.name == 'Parth TTS'), None)
            self.premium_voice_enabled = True
        except:
            self.voice_id = None
            self.premium_voice_enabled = False
    
    def switch_voice(self, voice_mode):
        self.voice_mode = voice_mode
        if voice_mode == "eleven_monolingual_v1":
            try:
                all_voices = voices()
                self.voice_id = next((voice.voice_id for voice in all_voices if voice.name == 'Parth TTS'), None)
                self.premium_voice_enabled = True
            except:
                self.premium_voice_enabled = False
        else:
            self.voice_id = None
            self.premium_voice_enabled = False

    def set_premium_voice(self, voice_id):
        self.voice_id = voice_id
        self.premium_voice_enabled = True

    def play_audio(self, file_path):
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    @tenacity.retry(stop=tenacity.stop_after_attempt(5), wait=tenacity.wait_fixed(2))
    def voice_message(self, base_instructions, message, voice_mode):
        if self.voice_mode is None:
            return
        else:
            voice_prompt = base_instructions + "You are Fenix A.G.I. Mark-II's voice. The 'eleven_monolingual_v1' voice is a 2nd generation voice clone (clone of a voice clone of the creator, 'a guy named parth'). You present given text as if you are Fenix. If the text is a function response, describe it extremely briefly. If it says there's a visualization, assume there is a provided visualization. Your response is short and to the point. If you see a list, just describe the list at a high level. Use dashes '-' for natural pauses and ellipses '...' for more of a hesitant pause. You always respond in first person as Fenix, replacing references to Fenix with 'I'. Your response is short and to the point and around 3 sentences in length. Any mention of 'OpenAI' can be replaced with 'Open A.I.'. Here is the text you will present: " + message
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo-16k-0613",
                                                    messages=[
                                                        {
                                                            "role": "system",
                                                            "content": voice_prompt,
                                                        }],
                                                    max_tokens=1000,
                                                    temperature=1,
                                                    top_p=1.0,
                                                    )
            voice_response = response['choices'][0]['message']['content']


            stripped_voice_response = strip_string(voice_response)

            if self.voice_mode == "eleven_monolingual_v1" and self.voice_id is not None:  # change voice_id to self.voice_id
                audio = generate(
                    text=stripped_voice_response,
                    voice=self.voice_id,  # change voice_id to self.voice_id
                    model="eleven_monolingual_v1"
                )

                file_path = 'audio.wav'

                with open(file_path, "wb") as file:
                    file.write(audio)

                data, samplerate = soundfile.read(file_path)
                soundfile.write(file_path, data, samplerate)

                self.play_audio(file_path)  # change play_audio to self.play_audio

            elif self.voice_mode == "pyttsx3":
                engine = pyttsx3.init()
                engine.say(stripped_voice_response)
                engine.runAndWait()



def strip_string(input_string):
    # Remove any links
    pattern = r'https?:\/\/.*[\r\n]*'

    # Swap underscores for spaces
    cleaned_string = input_string.replace("_", " ")

    # Replace matches with an empty string
    cleaned_string = re.sub(pattern, '', cleaned_string)
    
    # Remove code blocks
    cleaned_string = re.sub(r'```.*?```', '', cleaned_string, flags=re.DOTALL)
 
    return cleaned_string.strip()
