from music21 import *
from array import *
from pprint import pprint

# helper function
def noteToNumber(note):
    key = note.name
    if key == 'C':
        number = 1
    if key == 'C+' or key == 'D-':
        number = 2
    if key == 'D':
        number = 3
    if key == 'D+' or key == 'E-':
        number = 4
    if key == 'E':
        number = 5
    if key == 'F':
        number = 6
    if key == 'F+' or key == 'G-':
        number = 7
    if key == 'G':
        number = 8
    if key == 'G+' or key == 'A-':
        number = 9
    if key == 'A':
        number = 10
    if key == 'A+' or key == 'B-':
        number = 11
    if key == 'B':
        number = 12
    return (note.octave - 1) * 12 + 3 + number


def monophonic_pageinator(path=r'.\Pi.xml'):
    # Outer array:
    # each entry represents a page
    # Inner array:
    # first index is piano key number(s) of note(s)
    # second index is measure number
    # third index is beat within measure
    # convert xml file into Music21 objects
    score = converter.parse(path)
    # divides score into its pages!!
    pagesArray = layout.divideByPages(score, fastMeasures=True)
    arrayThatGoesOnTheOutside = []

    for i in range(len(pagesArray.pages)):
        pageElements = pagesArray.pages[i].semiFlat.elements

        noteArray = []

        for x in pageElements:
            xClasses = x.classes
            if 'Note' in xClasses:
                # append the note
                noteName = str(x.pitch)
                noteArray.append([noteToNumber(x), x.measureNumber, x.beat])
            if 'Chord' in xClasses:
                # append the chord
                chordNotes = []
                noteNumbers = []
                for n in x.notes:
                    noteName = str(n.pitch)
                    chordNotes.append(noteName)
                    noteNumbers.append(noteToNumber(n))
                noteArray.append([noteNumbers, x.measureNumber, x.beat])
            if 'Rest' in xClasses:
                # append the rest if only in RH
                if x.duration != duration.Duration(4.0):
                    noteArray.append([0, 0, x.measureNumber, x.beat])
                    # print(noteArray)
        arrayThatGoesOnTheOutside.append(noteArray)

    # pprint(arrayThatGoesOnTheOutside)
    return arrayThatGoesOnTheOutside


if __name__ == "__main__":
    pprint(monophonic_pageinator())