print("Loading octave...")
import numpy
import oct2py

octave = oct2py.Oct2Py()

print("Loading sound file...")
y, f_s = octave.audioread("C:/Users/User/Documents/university/Capstone Project/output.wav")
# y, f_s = octave.audioread("C:/Users/User/Desktop/file.wav")
# y, f_s = octave.audioread("C:/Users/User/Desktop/c-minor-chord.wav")
# y, f_s = octave.audioread("C:/Users/User/Desktop/single-piano-note.wav")
# y, f_s = octave.audioread("C:/Users/User/Desktop/single-notes.wav")
# y, f_s = octave.audioread("C:/Users/User/Desktop/octave-on-piano.wav")
# y, f_s = octave.audioread("C:/Users/User/Desktop/chromatic.wav")
# y, f_s = octave.audioread("C:/Users/User/Desktop/winterwind.wav")

def fft(vals):
    print("Taking FFT...")
    result = octave.abs(octave.fft(vals))
    return result[:, 0] # + result[:, 1]

def no_filter(vals):
    return vals

def filter_first_overtone(vals):
    print("Filtering overtones...")
    ret = vals[:]
    for i, v in enumerate(ret):
        try:
            ret[i*2] = ret[i*2] - v # max(ret[i*2] - 2*v, 0)
        except IndexError:
            pass
    return ret

def note_number_to_freq(num):
    return 440 * 2**((num - 49) / 12)

def freq_to_note_numbers(vals):
    print("Converting frequencies to note numbers...")
    """
    440Hz = "A"
    12 semitones per octave
    A440 is key number 49 on the piano
    """
    ret = octave.log2(vals / 440) * 12 + 49
    try:
        return ret[0]
    except IndexError:
        return ret

def plot_frequency_spectrum(wav_data, f_s=44100, numbered_notes=True, overtone_filter=no_filter):
    # Filter overtones
    y_vals = overtone_filter(fft(wav_data))

    # Convert abstract FFT indexes to Hz
    # Source: https://dsp.stackexchange.com/questions/46167/getting-frequencies-corresponding-to-peaks-in-fft-plot-matlab  # pylint: disable=line-too-long
    scaling_factor = f_s / len(wav_data)
    x_vals = (octave.linspace(1, len(wav_data), len(wav_data)) * scaling_factor)[0]
    assert len(y_vals) == len(x_vals)

    r_min = int(26 / scaling_factor)    # Frequency of lowest note on piano
    r_max = int(4200 / scaling_factor)  # Frequency of highest note on piano

    if numbered_notes:
        x_vals = freq_to_note_numbers(x_vals)

    print("Plotting...")

    x_plottable, y_plottable = x_vals[r_min:r_max], y_vals[r_min:r_max]

    octave.plot(x_plottable, y_plottable)
    return x_plottable, y_plottable

a, b = plot_frequency_spectrum(y, numbered_notes=True) #, overtone_filter=filter_first_overtone)
b_sorted = sorted(enumerate(b), key=lambda x: x[1])
