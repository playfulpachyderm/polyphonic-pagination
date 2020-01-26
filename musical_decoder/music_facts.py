"""
Some functions and constants describing musical reality.
"""

import math

LOWEST_PIANO_FREQ = 27.5   # Note number 1 (A0)
HIGHEST_PIANO_FREQ = 4186  # Note number 88 (C8)

KEY_COUNT = 88

def freq_to_note(freq):
    """
    Convert a frequency in Hz to a note number on the piano.

    440Hz = "A"
    12 semitones per octave
    A440 is key number 49 on the piano
    """
    return math.log2(freq / 440) * 12 + 49


def note_to_freq(note):
    """
    Convert a note number to a frequency in Hz.

    Same scheme as above.
    """
    return 440 * 2**((note - 49) / 12)
