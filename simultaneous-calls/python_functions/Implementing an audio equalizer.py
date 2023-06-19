from pydub import AudioSegment
import numpy as np

def equalize_audio(filename, eq_freqs=None, eq_gains=None, output_filename=None):
    # Default equalizer frequency bands and gains
    if eq_freqs is None:
        eq_freqs = [64, 125, 250, 500, 1_000, 2_000, 4_000, 8_000, 16_000]
    if eq_gains is None:
        eq_gains = [0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Load audio file
    audio = AudioSegment.from_file(filename)

    # Make sure there are equal number of DataFrame points and gains
    assert len(eq_freqs) == len(eq_gains), "Equalizer freqs and gains must be the same length."

    # Create a blank array to store the equalized audio
    equalized_audio = np.array([])

    for i, freq in enumerate(eq_freqs):
        # Get the specific frequency band
        band = audio.low_pass_filter(freq * 2).high_pass_filter(freq / 2)
        
        # Adjust the gain for the current frequency band
        band = band + eq_gains[i]

        # Add the equalized band to the array
        if len(equalized_audio) == 0:
            equalized_audio = np.array(band.get_array_of_samples(), dtype=np.int16)
        else:
            equalized_audio = equalized_audio + np.array(band.get_array_of_samples(), dtype=np.int16)

    # Convert the numpy array back to an AudioSegment
    equalized_audio = AudioSegment(
        equalized_audio.tobytes(),
        frame_rate=audio.frame_rate,
        sample_width=audio.sample_width,
        channels=audio.channels
    )

    # Save the equalized audio
    if output_filename:
        equalized_audio.export(output_filename, format="wav")

    return equalized_audio