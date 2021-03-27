import pychord
import musicalbeeps

NOTE_TO_NUMBER = {
    ord("A"): 1,
    ord("B"): 3,
    ord("C"): 4,
    ord("D"): 6,
    ord("E"): 8,
    ord("F"): 9,
    ord("G"): 11
}
NUMBER_TO_NOTE = {
    1: "A",
    2: "A#",
    3: "B",
    4: "C",
    5: "C#",
    6: "D",
    7: "D#",
    8: "E",
    9: "F",
    10: "F#",
    11: "G",
    12: "G#",
}

CHORD_MAX_NOTES = 4

def main():
    while True:
        base_str = input("Enter base note: ")
        chord_str1 = input("Enter chord 1: ")
        chord_str2 = input("Enter chord 2: ")

        try:
            chord1 = pychord.Chord(chord_str1)
            chord2 = pychord.Chord(chord_str2)

            notes1 = chordToList(chord1, base_str)
            notes2 = chordToList(chord2, base_str)
            print("Chord 1:", notes1, notesToStrings(notes1, base_str))
            print("Chord 2:", notes2, notesToStrings(notes2, base_str))

            notes_mult = multiplyChords(notes1, notes2)
            notes_mult_str = notesToStrings(notes_mult, base_str)
            notes_mult_chord = pychord.note_to_chord(notes_mult_str)

            if notes_mult_chord == []:
                notes_mult_chord = "Unknown chord"

            print("Chords multiplied:", notes_mult_chord, notes_mult, notes_mult_str)

            playChord(notes_mult_str)
        except ValueError as e:
            print(e)

def multiplyChords(A: list, B: list):
    result = [1]*CHORD_MAX_NOTES

    # 2x2 for now
    result[0] = A[0] * B[0] + A[1] * B[2]
    result[1] = A[0] * B[1] + A[1] * B[3]
    result[2] = A[2] * B[0] + A[3] * B[2]
    result[3] = A[2] * B[1] + A[3] * B[3]

    return result

def chordToList(chord: pychord.Chord, base: str):
    notes = []

    for note in chord.components():
        notes.append(noteToNumber(base, note))

    if len(notes) > CHORD_MAX_NOTES:
        notes = notes[0:CHORD_MAX_NOTES]
    elif len(notes) < CHORD_MAX_NOTES:
        notes += [1] * (CHORD_MAX_NOTES-len(notes))

    return notes

def notesToStrings(notes: list, base: str):
    strings = []

    offset = noteToNumber("A", base)-1

    for note in notes:
        # Offset
        strings.append(NUMBER_TO_NOTE[(note+offset-1)%12+1])

    return strings

def noteToNumber(base: str, note: str):
    base_offset = 0
    note_offset = 0

    # Handle flat and sharp. _n are ints
    base_n, base_offset = handleAccidental(base)
    note_n, note_offset = handleAccidental(note)

    # Check that notes are capital letter or convert if possible
    testAndConvertNote(base_n)
    testAndConvertNote(note_n)

    # Map to range 1-12
    base_n = (NOTE_TO_NUMBER[base_n] + base_offset) % 12
    note_n = (NOTE_TO_NUMBER[note_n] + note_offset) % 12

    return (note_n-base_n+13-1) % 12 + 1

def testAndConvertNote(note: int):
    if ord('A') <= note <= ord('G'):
        pass
    elif ord('a') <= note <= ord('g'):
        note -= 32
    else:
        raise ValueError("Invalid note value", note)
    return note

def handleAccidental(note: str):
    offset = 0

    if len(note) == 2:
        if note[1] == '#':
            offset = 1
        elif note[1] == 'b':
            offset = -1
        else:
            raise ValueError("Invalid accidental")

    return ord(note[0]), offset

def playChord(notes: list):
    players = []

    for i in range(len(notes)):
        players.append(musicalbeeps.Player(volume=0.3, mute_output=False))

    for i in range(len(notes)):
        players[i].play_note(notes[i], 2)

main()