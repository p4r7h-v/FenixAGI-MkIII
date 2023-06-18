import irc.bot
import irc.strings
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


class TwitchBot(irc.bot.SingleServerIRCBot):

  def __init__(self):
    self.server = "irc.chat.twitch.tv"
    self.port = 6667
    self.username = os.getenv("TWITCH_USERNAME")
    self.token = os.getenv("TWITCH_TOKEN")
    self.channel = f"#{self.username}"
    self.rules = "Be respectful. No spamming. No self-promotion. No spoilers."
    self.twitter_link = "twitter.com/htrapvader"
    self.replit_link = "replit.com/@p4r7h"
    self.start_time = time.time()

    print(f"Connecting to {self.server}:{self.port} as {self.username}...")

    irc.bot.SingleServerIRCBot.__init__(self,
                                        [(self.server, self.port, self.token)],
                                        self.username, self.username)

  def on_welcome(self, connection, event):
    connection.join(self.channel)
    print(f"Successfully connected to {self.channel} on {self.server}.")

  def on_pubmsg(self, connection, event):
    command = event.arguments[0]
    print(f"Received command: {command}")

    if command == "!hello":
      self.connection.privmsg(self.channel, "Hello, Twitch chat!")

    elif command.startswith("!shoutout"):
      user = command.split()[1]
      self.connection.privmsg(self.channel, f"Shout out to @{user}!")

    elif command == "!uptime":
      uptime_seconds = time.time() - self.start_time
      uptime_minutes, uptime_seconds = divmod(uptime_seconds, 60)
      uptime_hours, uptime_minutes = divmod(uptime_minutes, 60)
      uptime_string = f"{int(uptime_hours)} hours, {int(uptime_minutes)} minutes, {int(uptime_seconds)} seconds"
      self.connection.privmsg(self.channel, "The agent has been live for: " + uptime_string)


    elif command.startswith("!clu"):
      prompt = command.replace("!clu", "")
      system_message = "Your role is to act as a helpful assistant on a live stream. This stream, run by Parth, showcases programming with GPT-4. The stream features generative code and autonomous agents built in python. Your task is to assist viewers by answering their questions and providing context around the stream. You only respond on topics relevant to the programming. Keep your answers short and to the point."
      response = openai.ChatCompletion.create(model="gpt-3.5-turbo-0613",
                                              messages=[{
                                                "role":
                                                "system",
                                                "content":
                                                system_message
                                              }, {
                                                "role": "user",
                                                "content": prompt
                                              }],
                                              max_tokens=200)

      assistant_message = response['choices'][0]['message'][
        'content']
      print(assistant_message)
      self.speak_and_send_message(assistant_message)
      self.connection.privmsg(self.channel, "C.L.U.: " + assistant_message)

    elif command == "!rules":
      self.connection.privmsg(self.channel, "Chat Rules: " + self.rules)

    elif command == "!socials":
      self.connection.privmsg(self.channel, "Follow me on Twitter: " + self.twitter_link)
      self.connection.privmsg(self.channel, "Follow me on Clubhouse: " + self.clubhouse_link)
      self.connection.privmsg(self.channel, "Try my projects on Replit: " + self.replit_link)

    elif command == "!commands" or command == "!help":
      commands = ["!hello", "!shoutout", "!uptime", "!clu", "!rules", "!socials", "!replit"]
      self.connection.privmsg(self.channel, "Available commands: " + ', '.join(commands))


  def speak_and_send_message(self, message):
    if dip_sith_voice_id:
      # Use the 'Dip Sith' voice to generate speech
      audio = generate(
                text=message,
                voice=dip_sith_voice_id,
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

# Fetch all available voices
all_voices = voices()
#print(all_voices)

# Find the 'Dip Sith' voice
dip_sith_voice_id = next(
  (voice.voice_id for voice in all_voices
   if voice.name == 'Dip Sith:  Trained with famous Dark Side Phrases'), None)

if __name__ == "__main__":
  bot = TwitchBot()
  bot.start()
