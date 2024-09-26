from midiutil import MIDIFile
from mingus.core import chords

chord_progression = ["E" , "C#m" , "F#m" , "A" , "Am"]

NOTES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
OCTAVES = list(range(11))
NOTES_IN_OCTAVE = len(NOTES)
#dictornary for errors
errors = {
    'notes': 'Bad input, please refer this spec-\n'
}

#this function swaps "accidentals" aka notes that are written different but mean the same, C# is the same as F, Fb is the same as C
# To make things easier, we pick one of the written ways eg Db goes to C# 
def swap_accidentals(note):
    if note == 'Db':
        return 'C#'
    if note == 'D#':
        return 'Eb'
    if note == 'E#':
        return 'F'
    if note == 'Gb':
        return 'F#'
    if note == 'G#':
        return 'Ab'
    if note == 'A#':
        return 'Bb'
    if note == 'B#':
        return 'C'

    return note

#function that takes the swapped note, runs a check to see if it is in the NOTES array, checks if it is in the OCTAVES array,
#then to find the midi number it takes the note and finds the index of it, eg c = o , d = 2 , f# = 6 
#using this it runs it through a line of maths that calculates the midi number: midinumber = index of note + 12* which octave the note is in. 
# eg the index of C is 0 , the octave we are in is set to 4 (octave = 4) and the NOTES_in_octave is 12 since the chromatic scale is 12.
# so the midi number (which is being assigned to the variable note) , is going to be = to 0+(12*4) which will = 48
#so the midi number for C4 is = 48
def note_to_number(note: str, octave: int) -> int:
    note = swap_accidentals(note)
    assert note in NOTES, errors['notes']
    assert octave in OCTAVES, errors['notes']

    note = NOTES.index(note)
    note += (NOTES_IN_OCTAVE * octave)

    assert 0 <= note <= 127, errors['notes']

    return note


array_of_notes = []
for chord in chord_progression:
    array_of_notes.extend(chords.from_shorthand(chord))

array_of_note_numbers = []
for note in array_of_notes:
    OCTAVE = 4
    array_of_note_numbers.append(note_to_number(note, OCTAVE))

track = 0
channel = 0
time = 0  # In beats
duration = 1  # In beats
# Get user input for tempo and volume
tempo = int(input("Enter the tempo (BPM): "))  # User inputs tempo in beats per minute
volume = int(input("Enter the volume (0-127): "))  # User inputs volume (0 to 127)

# Ensure the volume is within the valid MIDI range
if volume < 0 or volume > 127:
    print("Volume must be between 0 and 127.")
    volume = 100  # Set a default volume if the input is out of range



MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
# automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(array_of_note_numbers):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open("pure-edm-fire-arpeggio2.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)


    


