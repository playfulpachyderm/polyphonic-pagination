"""
Plot frequency spectrum of wav files
"""

import math
import os
import numpy
from scipy.fftpack import fft as FFT
from scipy.io import wavfile

print("Loading sound file...")

AUDIO_DIR = os.path.abspath(__file__ + "/../../audio-samples")

def scipy_load_wav(filename):
    fullpath = AUDIO_DIR + "/" + filename
    assert os.path.exists(fullpath), "No such file: " + fullpath
    y, f_s = wavfile.read(fullpath)
    return y, f_s

f_s, y = scipy_load_wav("single-note-me.wav")


def freq_to_note(freq):
    """
    440Hz = "A"
    12 semitones per octave
    A440 is key number 49 on the piano
    """
    return math.log2(freq / 440) * 12 + 49

def note_to_freq(note):
    return 440 * 2**((note - 49) / 12)


# def filter_first_overtone(vals):
#     print("Filtering overtones...")
#     ret = vals[:]
#     for i, v in enumerate(ret):
#         try:
#             ret[i*2] = ret[i*2] - v # max(ret[i*2] - 2*v, 0)
#         except IndexError:
#             pass
#     return ret

def get_scaling_factor(fft, f_s=44100):
    return f_s / len(fft)

scaling_factor = get_scaling_factor(y, f_s)

def fft_to_hz(fft):
    """
    Convert abstract FFT x-values to Hz.
    Source: https://dsp.stackexchange.com/questions/46167/getting-frequencies-corresponding-to-peaks-in-fft-plot-matlab  # pylint: disable=line-too-long
    """
    x_vals = numpy.linspace(1, len(fft), len(fft)) * scaling_factor

    assert len(x_vals) == len(fft)
    return x_vals


def displayable_range():
    """
    Returns: slice representing lowest to highest notes on piano
    A0 => 27.5 Hz
    C8 => 4186 Hz
    """
    lowest_note = int(26 / scaling_factor)
    highest_note = int(4200 / scaling_factor)

    return slice(lowest_note, highest_note)


def plot_frequency_spectrum(wav_data, f_s=44100, numbered_notes=True, overtone_filter=None):
    # Filter overtones
    y_vals = numpy.abs(FFT(wav_data))
    if overtone_filter:
        y_vals = overtone_filter(y_vals)

    x_vals = fft_to_hz(y_vals)
    slc = displayable_range()

    print("Plotting...")

    if numbered_notes:
        x_vals = [freq_to_note(x) for x in x_vals]
        xlabel = "Note numbers (A440 = 49)"
    else:
        xlabel = "Frequency (Hz)"

    x_plottable, y_plottable = x_vals[slc], y_vals[slc]

    return x_vals, y_vals


def tuning(fft, note_numbers):
    peak = note_numbers[fft.argmax()] % 1

    if peak > 0.5:
        return peak - 1
    else:
        return peak


def to_buckets(fft):
    num_buckets = 88

    buckets = []
    for note in range(num_buckets):
        i = int(note_to_freq(note) / scaling_factor)
        j = int(note_to_freq(note + 1) / scaling_factor)
        print(i, j)
        buckets.append(fft[i:j])

    return buckets


def single_note_from(fft):
    peak = freq_to_note(fft.argmax() * scaling_factor)
    tuning = (peak % 1)
    if tuning < 0.5:
        return int(peak)
    else:
        return int(peak+1)

if __name__ == "__main__":
    x, y = plot_frequency_spectrum(y, numbered_notes=True) #, overtone_filter=filter_first_overtone)

    from matplotlib import pyplot
    pyplot.xlim(0, 88)
    pyplot.plot(x, y, linewidth=0.5)
    pyplot.show()

    # b_sorted = sorted(enumerate(b), key=lambda x: x[1])

    # import time
    # def tryit(x):
    #     start = time.time()
    #     for i in range(x):
    #         a = fft(y[:(4400 + x)])
    #     print(time.time() - start)
