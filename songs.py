# MIDI to notes + min/max stats + loadSong
from dataclasses import dataclass
from pathlib import Path

import pretty_midi

MUSIC_DIR = Path(__file__).resolve().parent / "music"

PLAYLIST = [
    "Rivers In The Desert (Persona 5).mid",
    "It's Going Down Now (Persona 3 Reload).mid",
    "Last Surprise (Persona 5).mid",
    "Beneath The Mask (Persona 5) (1).mid",
    "A Way Of Life (Persona 3 Portable).mid",
    "Color Your Night (Persona 3 Reload).mid",
    "Full Moon Full Life (Persona 3 Reload).mid",
    "Heaven (Persona 4) (1).mid",
    "Persona 3 Reload - When the Moon's Reaching Out Stars.mid",
    "Pull The Trigger (Persona Q2_ New Cinema Labyrinth).mid",
    "Take Over (Persona 5 Royal).mid",
    "Wake Up, Get Up, Get Out There (Persona 5).mid",
]

@dataclass
class Note:
    number: int
    start: float
    duration: float
    velocity: float


@dataclass
class Song:
    name: str
    notes: list
    bpm: float
    min_midi: int
    max_midi: int
    min_vel: float
    max_vel: float
    min_time: float
    max_time: float


def load_song(path):
    midi = pretty_midi.PrettyMIDI(str(path))
    notes = []
    for inst in midi.instruments:
        for n in sorted(inst.notes, key=lambda n: n.start):
            notes.append(Note(int(n.pitch), float(n.start),
                              float(n.end - n.start), n.velocity / 127))

    if not notes:
        raise ValueError("no notes")

    _, tempos = midi.get_tempo_changes()
    bpm = float(tempos[0]) if len(tempos) else 120.0

    num = [n.number for n in notes]
    vel = [n.velocity for n in notes]
    dur = [n.duration for n in notes]
    return Song(Path(path).name, notes, bpm,
                min(num), max(num), min(vel), max(vel), min(dur), max(dur))


def load_playlist(names=PLAYLIST):
    songs = []
    for name in names:
        try:
            songs.append(load_song(MUSIC_DIR / name))
            print("loaded", name)
        except Exception as e:
            print("skipped", name, "-", e)
    print(f"{len(songs)}/{len(names)} songs ready")
    return songs


if __name__ == "__main__":
    # `python songs.py` to check files load
    for s in load_playlist():
        print(f"  {s.name}: {len(s.notes)} notes, {s.bpm:.0f} bpm, "
              f"pitch {s.min_midi}-{s.max_midi}")