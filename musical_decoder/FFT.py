"""
THe FFT class and associated helpers.
"""

import numpy

from scipy.fftpack import fft
from matplotlib import pyplot

from . import music_facts


class FFT(numpy.ndarray):
    """
    Represents the Fast Fourier Transform corresponding to a WavData object.
    """
    def __new__(cls, wav_data):
        ret = numpy.abs(fft(wav_data.normalize()))
        ret = ret.view(cls)

        ret.wav_data = wav_data
        ret.scaling_factor = ret.wav_data.sample_rate / len(ret)
        return ret

    def x_val_in_hz(self, x_val):
        """
        Convert abstract FFT indexes to Hz, using the `scaling_factor`.

        Source: https://dsp.stackexchange.com/questions/46167/getting-frequencies-corresponding-to-peaks-in-fft-plot-matlab  # pylint: disable=line-too-long
        """
        return x_val * self.scaling_factor  # pylint: disable=no-member

    def hz_to_x_val(self, hz):
        """
        Opposite of the above; same logic.
        """
        return hz / self.scaling_factor  # pylint: disable=no-member

    def single_note(self):
        """
        Pick a single note to represent this audio snippet
        """
        loudest = self.argmax()
        freq = self.x_val_in_hz(loudest)
        return music_facts.freq_to_note(freq)

    def plot(self, numbered_notes=True):
        """
        Plot this frequency spectrum
        """
        plot = FFTPlot(self)
        plot.plot()



class FFTPlot(object):
    """
    Plots an FFT.
    """
    def __init__(self, _fft):
        self.fft = _fft

        self.plottable_start = int(self.fft.hz_to_x_val(music_facts.LOWEST_PIANO_FREQ))
        assert self.plottable_start >= 1, self.plottable_start
        assert isinstance(self.plottable_start, int), type(self.plottable_start)

        self.plottable_end = int(self.fft.hz_to_x_val(music_facts.HIGHEST_PIANO_FREQ))
        assert self.plottable_end <= len(self.fft), self.plottable_end
        assert isinstance(self.plottable_end, int)

        self.x_vals = [
            self.fft.x_val_in_hz(i) for i in range(self.plottable_start, self.plottable_end)
        ]

        self.y_vals = [
            self.fft[i] for i in range(self.plottable_start, self.plottable_end)
        ]

        assert len(self.x_vals) == len(self.y_vals), "len(x_vals): {}, len(y_vals): {}".format(
            len(self.x_vals), len(self.y_vals)
        )

    def plot(self, numbered_notes=True):
        if numbered_notes:
            x_vals = [music_facts.freq_to_note(x) for x in self.x_vals]
        else:
            x_vals = self.x_vals

        pyplot.plot(x_vals, self.y_vals, linewidth=0.5)
        pyplot.show()


if __name__ == "__main__":
    from musical_decoder import *  # pylint: disable=wildcard-import,unused-wildcard-import
    # data = read_sample_wav("waltz2.wav")
    data = read_sample_wav("single-note-me2.wav")
    data = read_sample_wav("single-piano-note.wav")
    fft = FFT(data)
    fft.plot()
