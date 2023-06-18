import soundfile
import wave

file_path = "audio.wav"

# Read and rewrite the file with soundfile
data, samplerate = soundfile.read(file_path)
soundfile.write(file_path, data, samplerate)

# Now try to open the file with wave
with wave.open(file_path) as file:
    print('File opened!')