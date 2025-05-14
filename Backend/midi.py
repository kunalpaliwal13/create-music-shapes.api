from mido import Message, MidiFile, MidiTrack, MetaMessage
from midi2audio import FluidSynth


NOTE_MAP = {
    'C': 0, 'C#': 1, 'D': 2, 'D#': 3,
    'E': 4, 'F': 5, 'F#': 6, 'G': 7,
    'G#': 8, 'A': 9, 'A#': 10, 'B': 11
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
def create_midi(melody, output_path="output.mid", tempo=500000):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    # Set tempo (500000 microseconds per beat = 120 bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo))
    notes = melody.split()
    for note_str in notes:
        midi_num = note_to_midi(note_str)
        track.append(Message('note_on', note=midi_num, velocity=64, time=0))
        track.append(Message('note_off', note=midi_num, velocity=64, time=480))  # quarter note
    mid.save(output_path)
    return output_path

def midi_to_wav(midi_file, output_audio="output.wav", soundfont="/usr/share/sounds/sf2/FluidR3_GM.sf2"):
    fs = FluidSynth(soundfont)
    fs.midi_to_audio(midi_file, output_audio)
    return output_audio

if __name__ == "__main__":
    melody = "C4 E4 G4 F4 D4 B4 A4 C5 E4 G4 F4 E4 D4 C4 G4 A4"
    midi_path = create_midi(melody, "melody.mid")
    midi_to_wav(midi_path, "melody.wav")
