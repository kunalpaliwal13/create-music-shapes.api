from mido import Message, MidiFile, MidiTrack, MetaMessage
import pretty_midi


NOTE_MAP = {
    'C': 0,  'C#': 1,  'Db': 1,
    'D': 2,  'D#': 3,  'Eb': 3,
    'E': 4,
    'F': 5,  'F#': 6,  'Gb': 6,
    'G': 7,  'G#': 8,  'Ab': 8,
    'A': 9,  'A#': 10, 'Bb': 10,
    'B': 11,
}


def note_to_midi(note):
    if len(note) == 2:
        pitch, octave = note[0], int(note[1])
        accidental = ''
    else:
        pitch, accidental, octave = note[0], note[1], int(note[2])

    key = pitch + accidental
    midi_number = 12 + (octave * 12) + NOTE_MAP[key]
    return midi_number

def create_midi(melody: str, output_path="output.mid", tempo=120):
    """
    Create a MIDI file from a space-separated string of notes (e.g., "C4 D4 E4").
    Each note will be a quarter note.
    """
    midi = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(program=0) 
    beat_duration = 60.0 / tempo

    current_time = 0.0
    for note_str in melody.split():
        midi_number = note_to_midi(note_str)
        note = pretty_midi.Note(
            velocity=100, 
            pitch=midi_number, 
            start=current_time, 
            end=current_time + beat_duration
        )
        instrument.notes.append(note)
        current_time += beat_duration  # Move to next beat

    midi.instruments.append(instrument)
    midi.write(output_path)
    return output_path

def midi_to_wav(midi_file, output_audio="output.wav", soundfont="/usr/share/sounds/sf2/FluidR3_GM.sf2"):
    fs = FluidSynth(soundfont)
    fs.midi_to_audio(midi_file, output_audio)
    return output_audio

if __name__ == "__main__":
    melody = "C4 E4 G4 F4 D4 B4 A4 C5 E4 G4 F4 E4 D4 C4 G4 A4"
    midi_path = create_midi(melody, "melody.mid")
    midi_to_wav(midi_path, "melody.wav")
