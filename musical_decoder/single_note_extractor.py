import math
import os
from scipy.fftpack import fft as FFT
import numpy
from scipy.io import wavfile

from .plot import scipy_load_wav, freq_to_note, get_scaling_factor, tuning, single_note_from

# print("Loading sound file...")

AUDIO_DIR = os.path.abspath(__file__ + "/../../audio-samples")

f_s, y = scipy_load_wav("pi_mono.wav")
# f_s, y = scipy_load_wav("single-piano-note.wav")


# scaling_factor = get_scaling_factor(y, f_s)

# print(single_note_from(FFT(y)))
