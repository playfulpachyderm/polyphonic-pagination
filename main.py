from musical_decoder.single_note_extractor import *
from musical_decoder.plot import set_scale
from page_import.Monophonic_Pagination import *
from MED.PatternMatch import *
import numpy as np
import matplotlib.pyplot as plt
import pyaudio
import time

page = monophonic_pageinator("./page_import/Pi.xml")
# print(page[0][0][0])



f_s, y = scipy_load_wav("pi_mono.wav")
# plt.figure(1)

# for notes_on_page in [ [page[0][i][0] for i in range(0, len(page[0]))] ,
#                        [page[1][i][0] for i in range(0, len(page[1]))] ] :

pno = 0
notes_on_page = [page[pno][i][0] for i in range(0, len(page[pno]))]

matcher = MEDBuffer(notes_on_page, 5)
image = plt.imshow(matcher.MED_buffer, origin='upper')
plt.xlabel("Page Buffer")
plt.ylabel("Played Note Buffer")
plt.draw()
plt.pause(0.01)

notes = []
alignment_call = []
for i in np.arange(0, len(y), f_s / 10):

    # print("%d:%d"%(i,i+f_s/10))
    sample = y[int(i):int(i+f_s/10)].copy()
    set_scale(sample, f_s)
    # print(len(sample))
    # sample = sample - np.mean(sample)
    # print(sample)
    # plt.plot(FFT(sample))
    # print(single_note_from(FFT(sample)))

    fft_value = FFT(sample)
    n = single_note_from(fft_value)
    if len(notes) == 0 or n != notes[-1]:
        notes.append(n)
        matcher.add_note(n)
        best_alignment = matcher.get_end_alignment()
        alignment_call.append(best_alignment)

        image.set_data(matcher.MED_buffer)
        image.set_extent((0, len(matcher.page_buffer), len(matcher.recent_note_buffer), 0))
        plt.draw()
        plt.pause(0.1)
        if best_alignment == len(notes_on_page):
            print("Reached end of the page")
            pno += 1
            if pno >= len(page):
                break
            notes_on_page = [page[pno][i][0] for i in range(0, len(page[pno]))]
            matcher = MEDBuffer(notes_on_page, 5)
            # break

    # fig, ax = plt.subplots()
    # ax.plot(notes, '*')
    # for xpos, ypos in enumerate(notes):
    #     ax.annotate(alignment_call[xpos],(xpos,ypos))
    # # plt.show()
