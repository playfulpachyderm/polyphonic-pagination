import numpy as np
import collections


# TODO: Swap out the lists for static arrays.
# It will improve efficiency and run time
class MEDBuffer:
    def __init__(self, page_buffer, note_buffer_length=0):
        self.page_buffer = page_buffer
        # self.recent_note_buffer = collections.deque(maxlen=note_buffer_length)
        self.recent_note_buffer = []
        self.MED_buffer = [[i for i in range(0, len(page_buffer)+1)]]
        # self.MED_head = 0
        # self.MED_tail = 0

    def add_note(self, note):
        self.recent_note_buffer.append(note)
        self.MED_buffer.append([0 for i in range(0, len(self.page_buffer)+1)])
        self.update_med_table()
        return self.get_end_alignment()

    def update_med_table(self):
        self.MED_buffer[-1][0] = self.MED_buffer[-2][0] + 1

        for i in range(1, len(self.page_buffer) + 1):
            # Gap penalty of 1
            value1 = self.MED_buffer[-2][i] + 1
            value2 = self.MED_buffer[-1][i-1] + 1
            value3 = self.MED_buffer[-2][i-1]

            # This is where we'd do a lookup for a mismatch penalty
            if self.recent_note_buffer[-1] != self.page_buffer[i-1]:
                value3 += 2

            self.MED_buffer[-1][i] = min(value1, value2, value3)

    def get_end_alignment(self):
        l = min(self.MED_buffer[-1])
        i = self.MED_buffer[-1].index(l)
        return i

    def purge_buffer(self):
        self.MED_buffer = [[i for i in range(1, len(self.page_buffer)+1)]]
