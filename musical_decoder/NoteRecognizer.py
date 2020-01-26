"""
"""

import numpy
from matplotlib import pyplot

from .FFT import FFT
from . import music_facts

class NoteRecognizer(numpy.ndarray):
    """
    Recognizes notes
    """
    def __new__(cls, fft):
        ret = numpy.array([])

        for note in range(music_facts.KEY_COUNT):
            note_range_start_freq = music_facts.note_to_freq(note - 0.5)
            note_range_end_freq = music_facts.note_to_freq(note + 0.5)

            note_range_start_index = int(fft.hz_to_x_val(note_range_start_freq))
            note_range_end_index = int(fft.hz_to_x_val(note_range_end_freq))

            fft_slice = fft[note_range_start_index : note_range_end_index]

            ret = numpy.append(ret, numpy.average(fft_slice))

        return ret.view(cls)

    def single_note(self):
        return numpy.nan_to_num(self).argmax()

    def plot(self):
        pyplot.bar(*zip(*enumerate(self)))
        pyplot.show()

def extract(wav_data):
    fft = FFT(wav_data)
    recognizer = NoteRecognizer(fft)
    return recognizer.single_note()

if __name__ == "__main__":
    from musical_decoder import *  # pylint: disable=wildcard-import,unused-wildcard-import
    data = read_sample_wav("single-piano-note.wav")
    fft = FFT(data)
    recognizer = NoteRecognizer(fft)
    pyplot.bar(*zip(*enumerate(recognizer)))
    pyplot.show()

    print(recognizer.single_note())
