from music21 import *
from array import *
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

# Convert xml file into Music21 objects
score = converter.parse(r'C:\Users\Joyce Yu\Documents\Audiveris\Remembering Serenity\Remembering Serenity.xml')
#score = converter.parse(r'C:\Users\Joyce Yu\Documents\Audiveris\Pi\Pi.xml')

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

#BUT WHAT ABOUT THE START OF A NEW PAGE???

for i in range(len(pagesArray.pages)):
    newPage = True
    pageOffset = 0
    pageElements = pagesArray.pages[i].semiFlat.elements
    #print(pageElements)
    
    noteArray = []
    previousOffsets = []
    
    for x in pageElements:
        xClasses = x.classes
        if 'TimeSignature' in xClasses:
            timeSignature = x   # music21.meter.TimeSignature object
            # timeSignature.beatDuration.quarterLength is a thing!!
        
        if 'Note' in xClasses:
            if not previousOffsets:
                elapsedBeats = 0
            elif newPage:
                pageOffset = previousOffsets[-1] + something # Whatever was left in the previous page
            else:
                # Calculate elapsed beats since previous note
                elapsedBeats = pageOffset + x.activeSite.offset + x.offset - previousOffsets[-1]

            previousOffsets.append(pageOffset + x.activeSite.offset + x.offset)
            
            # List of notes to append to noteArray
            currentNotes = []
            
            # Decrement remaining beats of all notes in notesHeldDownArray
            print("notesHeldDownArray:")
            print(notesHeldDownArray)
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
                    elapsedBeats = x.activeSite.offset + x.offset - previousOffsets[-1]

                previousOffsets.append(x.activeSite.offset + x.offset)

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
                elapsedBeats = x.activeSite.offset + x.offset - previousOffsets[-1]
            
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
                
        # Set newPage flag to False
        newPage = False
        
    #print(noteArray)
    arrayThatGoesOnTheOutside.append(noteArray)

pp.pprint(arrayThatGoesOnTheOutside)

#Outer array: 
    # Each entry represents a page
#Inner array: 
    # First index is array of piano key number(s) of note(s) held through the specified beat
    # Second index is measure number
    # Third index is beat within measure