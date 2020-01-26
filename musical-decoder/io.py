"""
Small module with functions to do with reading WAV data, either from a file or the microphone.
"""

import os
import wave

# from scipy.io import wavfile
import pyaudio

from .WavData import WavData


AUDIO_DIR = os.path.dirname(__file__) + "/../audio-samples"
SAMPLE_RATE = 44100
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16

p = pyaudio.PyAudio()
# mic = p.open(format=FORMAT, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

def read_sample_wav(filename):
    """
    Read a file from the `audio-samples` directory as a wav file.

    Params:
        - `filename`: name of the file to read

    Returns: f_s, data
        - `f_s`: sampling rate
        - `data`: the samples
    """
    fullpath = AUDIO_DIR + "/" + filename
    assert os.path.exists(fullpath), "No such file: " + fullpath

    # Using Python builtin `wave` library because scipy.io.wavfile can't read
    # file metadata (channels, rate, etc)
    x = wave.open(fullpath, "rb")
    data = x.readframes(x.getnframes())

    return WavData.from_bytes(data,
        sample_rate=x.getframerate(),
        sample_size=x.getsampwidth(),
        n_channels=x.getnchannels()
    )


def read_from_mic_blocking(frames):
    """
    Read audio from mic using 1 channel, 2 bytes per frame, and 44100 samples / s.

    Params:
        - `frames`: number of frames to read
        - `seconds`: time in seconds to record for
    """
    mic = p.open(format=FORMAT, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)
    data = mic.read(frames)
    return WavData.from_bytes(data)


def play_file(filename):
    """
    Test function.  Play an audio file from `audio-samples` by filename.
    """
    w = read_sample_wav(filename)
    w.play()

__all__ = ["read_sample_wav", "read_from_mic_blocking", "play_file"]
