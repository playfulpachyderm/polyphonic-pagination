from musical_decoder.single_note_extractor import *
from musical_decoder.plot import set_scale
from page_import.Monophonic_Pagination import *
from MED.PatternMatch import *
import numpy as np
import matplotlib.pyplot as plt
import time
import winsound

page = monophonic_pageinator("./page_import/Pi.xml")
# print(page[0][0][0])

f_s, y = scipy_load_wav("pi_mono.wav")
# plt.figure(1)

# for notes_on_page in [ [page[0][i][0] for i in range(0, len(page[0]))] ,
#                        [page[1][i][0] for i in range(0, len(page[1]))] ] :

pno = 0
notes_on_page = [page[pno][i][0] for i in range(0, len(page[pno]))]

matcher = MEDBuffer(notes_on_page, 5)
fig1, ax1 = plt.subplots()
image = ax1.imshow(matcher.MED_buffer, origin='upper', vmin=0, vmax=1e2)
ax1.set_xlabel("Page Buffer")
ax1.set_ylabel("Played Note Buffer")
fig1.canvas.draw()
plt.pause(0.01)

notes = []
alignment_call = []
fig2, ax2 = plt.subplots()
plot, = ax2.plot(notes, '*')
plt.pause(0.01)

winsound.PlaySound('page_import/Pi.wav', winsound.SND_ASYNC)

for i in np.arange(0, len(y), f_s / 10):

    # print(i)
    ts = time.time()
    # print("%d:%d"%(i,i+f_s/10))
    sample = y[int(i):int(i+f_s/10)]
    set_scale(sample, f_s)
    # print(len(sample))
    # sample = sample - np.mean(sample)
    # print(sample)
    # plt.plot(FFT(sample))
    # print(single_note_from(FFT(sample)))

    fft_value = FFT(sample)
    n = single_note_from(fft_value)

    notes.append(n)

    plot.set_ydata(notes)
    plot.set_xdata(range(0, len(notes)))
    ax2.set_xlim(len(notes) - 10, len(notes))
    ax2.set_ylim(20, 80)
    fig2.canvas.draw()

    if len(notes) == 1 or n != notes[-2]:


        matcher.add_note(n)
        best_alignment = matcher.get_end_alignment()
        alignment_call.append(best_alignment)

        image.set_data(matcher.MED_buffer)
        image.set_extent((0, len(matcher.page_buffer), len(matcher.recent_note_buffer), 0))
        ax2.annotate(alignment_call[-1],(len(notes),notes[-1]), fontsize=20)
        fig1.canvas.draw()
        fig2.canvas.draw()
        plt.pause(0.01)
        if best_alignment == len(notes_on_page):
            print("Reached end of the page")
            pno += 1
            if pno >= len(page):
                break
            notes_on_page = [page[pno][i][0] for i in range(0, len(page[pno]))]
            matcher = MEDBuffer(notes_on_page, 5)
            # break
    gap = 0.095 - (time.time() - ts)
    if gap > 0:
        plt.pause(gap)



    # for xpos, ypos in enumerate(notes):
    #     ax.annotate(alignment_call[xpos],(xpos,ypos))
    # # plt.show()
