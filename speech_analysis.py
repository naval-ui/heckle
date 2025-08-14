import numpy as np
import wave

def is_silent(wav_file, silence_threshold=80):
    """
    Determines if the audio file is mostly silent by measuring RMS amplitude.

    Args:
        wav_file (str): Path to WAV audio file.
        silence_threshold (int): RMS value below which audio is considered silent.

    Returns:
        bool: True if audio is considered silent, False otherwise.
    """
    with wave.open(wav_file, 'rb') as wf:
        n_frames = wf.getnframes()
        audio_data = wf.readframes(n_frames)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        rms = np.sqrt(np.mean(audio_array**2))
        return rms < silence_threshold
