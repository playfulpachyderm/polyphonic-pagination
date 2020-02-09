from unittest import TestCase
from PatternMatch import MEDBuffer
import numpy as np


class TestMEDBuffer(TestCase):
    def test_add_note(self):
        testobj = MEDBuffer(["A", "B", "C"])
        testobj.add_note("A")
        testobj.add_note("B")
        testobj.add_note("C")
        print(np.asarray(testobj.MED_buffer))

    def test_get_end_alignment(self):
        testobj = MEDBuffer(["A", "B", "C"])
        testobj.add_note("A")
        testobj.add_note("B")
        testobj.add_note("C")
        self.assertEqual(testobj.get_end_alignment(), 3)


    def test_purge_buffer(self):
        self.fail()

    def test_longstring(self):
        testobj = MEDBuffer(["ACD", "JJE", "TPD"])
        testobj.add_note("A")
        testobj.add_note((""))