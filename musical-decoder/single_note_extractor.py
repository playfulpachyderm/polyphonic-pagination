import math
import os
import numpy
print("Loading octave...")

import oct2py

octave = oct2py.Oct2Py()

print("Loading sound file...")

AUDIO_DIR = os.path.abspath(__file__ + "/../../audio-samples")

def octave_load_wav(filename):
    """Read a wav file and return list of samples"""
    fullpath = AUDIO_DIR + "/" + filename
    assert os.path.exists(fullpath), "No such file: " + fullpath
    y, f_s = octave.audioread(fullpath)
    return y, f_s

y, f_s = octave_load_wav("single-piano-note.wav")


def freq_to_note(freq):
    """
    440Hz = "A"
    12 semitones per octave
    A440 is key number 49 on the piano
    """
    return math.log2(freq / 440) * 12 + 49


def fft(vals):
    """Return an FFT"""
    print("Taking FFT...")
    result = octave.abs(octave.fft(vals))
    return result[:, 0] # + result[:, 1]


def get_scaling_factor(fft, f_s=44100):
    return f_s / len(fft)

scaling_factor = get_scaling_factor(y, f_s)


def tuning(fft, note_numbers):
    peak = note_numbers[fft.argmax()] % 1

    if peak > 0.5:
        return peak - 1
    else:
        return peak

def single_note_from(fft):
    peak = freq_to_note(fft.argmax() * scaling_factor)
    tuning = (peak % 1)
    if tuning < 0.5:
        return int(peak)
    else:
        return int(peak+1)

print(single_note_from(fft(y)))
