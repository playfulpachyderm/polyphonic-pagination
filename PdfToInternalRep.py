# To run:
    # Download Audiveris
    # Navigate to wherever Audiveris is downloaded, it may be 'C:\Program Files\Audiveris'
    # Navigate into 'Audiveris/bin' and copy 'Pi.pdf' (should be under 'pdf-samples' folder in git repo) into this directory
    # Change the hardcoded file path 'C:\Users\Joyce Yu\Documents\Audiveris\Pi\Pi.mxl' in two places to your directory of where Audiveris stores outputted files 
    # This hardcode will be removed once UI is integrated

# What you want out of this is to call the function pdfToInternalRep

from music21 import *
from array import *
import zipfile
import subprocess
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

# Helper function translates from music21 note to keyboard key number (1 to 88)
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
    return (note.octave-1)*12 + 3 + number

# TODO: accept parameter with pdf file path (dependent on UI) 
def pdfToInternalRep():
    working_dir = r'C:\Program Files\Audiveris\bin' # You may need to change this depending on where your Audiveris program is stored
    #print(working_dir)

    print("Starting conversion from PDF to .mxl")
    process = subprocess.check_call(["Audiveris", "-batch", "-export", f"Pi.pdf"], shell=True, cwd=working_dir)
    print("Done converting from PDF to .mxl")


    # Extract XML file from .mxl
    # CHANGE THIS FILE PATH TO WHEREVER AUDIVERIS STORES OUTPUTTED FILES
    with zipfile.ZipFile(r'C:\Users\Joyce Yu\Documents\Audiveris\Pi\Pi.mxl') as zip_ref:
        zip_ref.extractall('./')

    # Convert xml file into Music21 objects
    # CHANGE THIS FILE PATH TO WHEREVER AUDIVERIS STORES OUTPUTTED FILES
    score = converter.parse(r'C:\Users\Joyce Yu\Documents\Audiveris\Pi\Pi.xml')

    # Divides score into its pages
    # pagesArray is a music21 LayoutScore object, not a python array
    pagesArray = layout.divideByPages(score, fastMeasures=True)

    # Array where each entry represents the contents of a page
    arrayThatGoesOnTheOutside = []

    # DURATION IS ALWAYS MEASURED IN QUARTER NOTES
    # BUT BEATS IS NOT MEASURED IN QUARTER NOTES

    # Dynamic array of currently held down notes
    # Each entry is a tuple [<note number>, <beats remaining>]
    notesHeldDownArray = []

    # To help calculate elapsed time between notes (Why is it all stored in a list? I'm going to say for debugging purposes...)
    previousOffsets = []    

    for i in range(len(pagesArray.pages)):
        pageOffset = pagesArray.pages[i].offset
        pageElements = pagesArray.pages[i].semiFlat.elements

        # Array to append to output array
        noteArray = []

        for x in pageElements:
            xClasses = x.classes
            if 'TimeSignature' in xClasses:
                timeSignature = x   # music21.meter.TimeSignature object
                # timeSignature.beatDuration.quarterLength is a thing

            if 'Note' in xClasses:
                if not previousOffsets:
                    elapsedBeats = 0
                else:
                    # Calculate elapsed beats since previous note
                    elapsedBeats = pageOffset + x.activeSite.offset + x.offset - previousOffsets[-1]

                previousOffsets.append(pageOffset + x.activeSite.offset + x.offset)

                # List of notes to append to noteArray
                currentNotes = []

                # Decrement remaining beats of all notes in notesHeldDownArray
                for n in notesHeldDownArray:
                    n[1] = n[1] - elapsedBeats

                # Remove all expired notes from notesHeldDownArray
                newList = [n for n in notesHeldDownArray if n[1] > 0]
                notesHeldDownArray = newList

                # Add new note to notesHeldDownArray
                notesHeldDownArray.append([noteToNumber(x), x.duration.quarterLength])

                # Append all notes in notesHeldDownArray to currentNotes
                for n in notesHeldDownArray:
                    currentNotes.append(n[0])

                # Remove previous noteArray if redundant because left hand comes in a separate entry in pageElements
                if noteArray:
                    previousNoteArrayEntry = noteArray[-1]
                    if previousNoteArrayEntry[1] == x.measureNumber and previousNoteArrayEntry[2] == x.beat:
                        noteArray.pop()

                # Append the note
                noteArray.append([ currentNotes, x.measureNumber, x.beat])

            if 'Chord' in xClasses:
                # Do what 'Note' does, but for chords

                # Append all notes of the chord
                noteNumbers = []
                for note in x.notes:
                    if not previousOffsets:
                        elapsedBeats = 0
                    else:
                        # Calculate elapsed beats since previous note
                        elapsedBeats = pageOffset + x.activeSite.offset + x.offset - previousOffsets[-1]

                    previousOffsets.append(pageOffset + x.activeSite.offset + x.offset)

                    # List of notes to append to noteArray
                    currentNotes = []

                    # Decrement remaining beats of all notes in notesHeldDownArray
                    for n in notesHeldDownArray:
                        n[1] = n[1] - elapsedBeats

                    # Remove all expired notes from notesHeldDownArray
                    newList = [n for n in notesHeldDownArray if n[1] > 0]
                    notesHeldDownArray = newList

                    # Add new note to notesHeldDownArray
                    notesHeldDownArray.append([noteToNumber(note), note.duration.quarterLength])

                    # Append all notes in notesHeldDownArray to currentNotes
                    for n in notesHeldDownArray:
                        currentNotes.append(n[0])

                # Remove previous noteArray if redundant because left hand comes in a separate entry in pageElements
                if noteArray:
                    previousNoteArrayEntry = noteArray[-1]
                    if previousNoteArrayEntry[1] == x.measureNumber and previousNoteArrayEntry[2] == x.beat:
                        noteArray.pop()

                noteArray.append([currentNotes, x.measureNumber, x.beat])
            if 'Rest' in xClasses:

                if not previousOffsets:
                    elapsedBeats = 0
                else:
                    # Calculate elapsed beats since previous note
                    elapsedBeats = pageOffset + x.activeSite.offset + x.offset - previousOffsets[-1]

                for n in notesHeldDownArray:
                    n[1] = n[1] - elapsedBeats

                # Remove all expired notes from notesHeldDownArray
                newList = [n for n in notesHeldDownArray if n[1] > 0]
                notesHeldDownArray = newList

                # Append the rest only if notesHeldDownArray is empty
                if not notesHeldDownArray:
                    if noteArray:
                        previousNoteArrayEntry = noteArray[-1]
                        if previousNoteArrayEntry[1] == x.measureNumber and previousNoteArrayEntry[2] == x.beat:
                            noteArray.pop()
                    noteArray.append([ [0], x.measureNumber, x.beat])  

        #print(noteArray)
        arrayThatGoesOnTheOutside.append(noteArray)

    pp.pprint(arrayThatGoesOnTheOutside)
    return arrayThatGoesOnTheOutside

# Understanding arrayThatGoesOnTheOutside
    # Outermost array:
        # Object that contains everything
    # First nested array: 
        # Each array represents a page
    # Second nested array: 
        # First index is array of piano key number(s) of note(s) held through the specified beat
        # Second index is measure number
        # Third index is beat within measure
        # The second and third indices are to be replaced with graphical coordinate values