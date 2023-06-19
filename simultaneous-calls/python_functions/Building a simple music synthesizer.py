import numpy as np
import simpleaudio as sa

# Simple music synthesizer function
def play_sine_wave(frequency, duration):
    # Sampling rate (sample/second) - CD Quality
    sample_rate = 44100
    
    # Generate an array of samples for the sine wave of desired frequency and duration
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

    # Convert the sine wave to PCM format (16-bit data)
    audio_data = (sine_wave * 32767).astype(np.int16)

    # Play the sine wave using simpleaudio
    play_obj = sa.play_buffer(audio_data, 1, 2, sample_rate)
    play_obj.wait_done()

# Example usage:
# Play a sine wave of 440 Hz (A4) for 2 seconds
play_sine_wave(frequency=440, duration=2)