from musical_decoder.single_note_extractor import *
from page_import.Monophonic_Pagination import *
from MED.PatternMatch import *
import numpy as np

f_s, y = scipy_load_wav("pi_mono.wav")

for i in np.arange(0,len(y), f_s//10):

    print("%d:%d"%(i,i+f_s/10))
    sample = y[int(i):int(i+f_s/10)].copy()
    print(len(sample))
    sample = sample - np.mean(sample)
    print(sample)
    print(single_note_from(FFT(y[int(i):int(i+f_s/10)])))