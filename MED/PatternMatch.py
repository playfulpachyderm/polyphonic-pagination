import numpy as np
import collections
from matplotlib import pyplot as plt

first_row_bias = 0.1
gap = 1
penalty = 2


# TODO: Swap out the lists for static arrays.
# It will improve efficiency and run time
class MEDBuffer:
    def __init__(self, page_buffer, note_buffer_length=0):
        first_row_bias
        self.page_buffer = page_buffer
        self.recent_note_buffer = []

        # Original method - initialize first row sequentially
        # self.MED_buffer = [[i for i in range(0, len(page_buffer)+1)]]

        #initialize first row to zeros to avoid biasing to start of page
        # self.MED_buffer = [[0 for i in range(0, len(page_buffer)+1)]]

        #use global gap value to init first row
        self.MED_buffer = [[i*first_row_bias for i in range(0, len(page_buffer)+1)]]


        # self.MED_head = 0
        # self.MED_tail = 0

    def note_penalty_lookup(self, played_note, page_note):
        misses = 0
        # one octave error should have low penalty

        for subnote in played_note:
            if subnote not in page_note:
                misses += penalty
        return misses


    def add_note(self, note):
        gap
        self.recent_note_buffer.append(note)
        self.MED_buffer.append([0 for i in range(0, len(self.page_buffer)+1)])
        self.update_med_table()
        return self.get_end_alignment()

    def update_med_table(self):
        self.MED_buffer[-1][0] = self.MED_buffer[-2][0] + 1

        for i in range(1, len(self.page_buffer) + 1):
            # Gap/deletion penalty of 1
            value1 = self.MED_buffer[-2][i] + gap
            value2 = self.MED_buffer[-1][i-1] + gap
            value3 = self.MED_buffer[-2][i-1]

            # This is where we'd do a lookup for a mismatch penalty
            if self.recent_note_buffer[-1] != self.page_buffer[i-1]:
                value3 += self.note_penalty_lookup(self.recent_note_buffer[-1], self.page_buffer[i-1])

            self.MED_buffer[-1][i] = min(value1, value2, value3)

    def get_end_alignment(self):
        min_value = min(self.MED_buffer[-1])
        min_index = self.MED_buffer[-1].index(min_value)
        return min_index

    def purge_buffer(self):
        self.MED_buffer = [[i for i in range(1, len(self.page_buffer)+1)]]

    def view_table(self):
        plt.ioff()
        plt.imshow(self.MED_buffer, origin="lower")
        plt.xlabel("Given Score Count")
        plt.ylabel("Interpreted Note Count")
        plt.show()

