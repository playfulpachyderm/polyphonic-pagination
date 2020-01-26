"""
The WavData class and associated helpers.
"""

from matplotlib import pyplot
import numpy
import pyaudio


FORMAT        = pyaudio.paInt16
CHUNK_SIZE    = 1024

p = pyaudio.PyAudio()


class WavData(numpy.ndarray):
    """
    Represents a snippet of audio data in WAV format.

    See the following for info on the weird __new__ method instead of __init__:
    - https://stackoverflow.com/questions/27557029/how-should-a-class-that-inherits-from-numpy-ndarray-and-has-a-default-value-be-c    # pylint: disable=line-too-long
    - https://docs.scipy.org/doc/numpy/user/basics.subclassing.html#slightly-more-realistic-example-attribute-added-to-existing-array  # pylint: disable=line-too-long
    """

    def __new__(cls, data, sample_rate=44100, sample_size=2, n_channels=1):
        """
        Params:
            - `data`: a numpy array
            - `sample_rate`: samples per second
            - `sample_size`: size of each sample, in bytes
            - `n_channels`: mono or stereo
        """

        if isinstance(data, list):
            data = numpy.array(data)

        ret = data.view(cls)
        ret.sample_rate = sample_rate
        ret.sample_size = sample_size
        ret.n_channels = n_channels

        return ret

    def __array_finalize__(self, other):
        if other is None:
            return

        # pylint: disable=attribute-defined-outside-init
        self.sample_rate = getattr(other, "sample_rate", 44100)
        self.sample_size = getattr(other, "sample_size", 2)
        self.n_channels = getattr(other, "n_channels", 1)

    @classmethod
    def from_bytes(cls, data, dtype=numpy.int16, **kwargs):
        """
        Initialize a WavData object from a bytes object (convenience method).
        """
        np_array = numpy.frombuffer(data, dtype=dtype)

        if "n_channels" in kwargs:
            n_channels = kwargs["n_channels"]
            assert len(np_array) % n_channels == 0, "len(np_array): {}, n_channels: {}".format(
                len(np_array), n_channels
            )
            length = len(np_array // n_channels)
            shape = (length, ) if n_channels is 1 else (length, n_channels)
            np_array = numpy.reshape(np_array, shape)
            # np_array = numpy.reshape(np_array, (len(np_array) // n_channels, n_channels))
        return cls.__new__(cls, np_array, **kwargs)

    def play(self):
        """
        Play this wav data over the speakers.
        """
        o_stream = p.open(format=FORMAT, channels=self.n_channels, rate=self.sample_rate, output=True)  # pylint: disable=no-member,line-too-long

        start = 0
        while start < len(self):
            chunk = self[start : start + CHUNK_SIZE].tobytes()
            o_stream.write(chunk)

            start += CHUNK_SIZE

        o_stream.stop_stream()
        o_stream.close()

    def normalize(self):
        """
        Averages 2-tuples to merge 2 channels into 1.

        data = [
            [a1, a2],
            [b1, b2],
            [c1, c2],
            ...
        ]

        Returns: 1d array
        """

        if len(self.shape) == 2:
            data = [sum(x) / 2 for x in self]
            # pylint: disable=no-member
            return WavData(data,
                sample_rate=self.sample_rate,
                sample_size=self.sample_size,
                n_channels=1)
        return self

    def plot(self):
        pyplot.plot(self)
        pyplot.show()
