# songs -> pen -> display
import math
import time

from pen import Pen, STRIKE_HOLD, LINE_HOLD
from songs import load_playlist
from preview import show  # swap for the real board

NUM_ROWS = 28
NUM_COLS = 28
DISC_BUDGET = 120

MIN_DISCS = 6
MAX_ROWS = 5
LINE_MIN_DUR = 0.1
BOARD_FPS = 15
BARS_PER_LAP = 3
PAUSE_MAX = 1.0
SWOOSH_TIME = 1.5
SWOOSH_HOLD = 0.15
SONG_GAP = 4

pen = Pen(NUM_ROWS, NUM_COLS, DISC_BUDGET)

songs = []
song = None
song_index = 0
next_note = 0
active_notes = []
last_note = None
song_ended_at = None
start_time = 0.0


def map_range(x, a, b, c, d):
    if a == b: 
        return (c + d) / 2
    return c + (x - a) * (d - c) / (b - a)


def js_round(x):
    return math.floor(x + 0.5)


def start_song(i):
    global song, song_index, next_note, active_notes, last_note, song_ended_at, start_time
    song_index = i
    song = songs[i]

    lap_seconds = BARS_PER_LAP * 4 * 60 / song.bpm
    pen.reset()
    pen.speed = min(NUM_COLS / lap_seconds, BOARD_FPS)

    next_note = 0
    active_notes = []
    last_note = None
    song_ended_at = None
    start_time = time.monotonic() - song.notes[0].start


def tick():
    global next_note, active_notes, last_note, song_ended_at, start_time

    elapsed = time.monotonic() - start_time
    pen.begin_frame(elapsed)
    p = pen.col(elapsed)

    active_notes = [n for n in active_notes if n["end_time"] > elapsed]

    # skip long silences
    if not active_notes and next_note < len(song.notes):
        gap = song.notes[next_note].start - elapsed
        if gap > PAUSE_MAX:
            start_time -= gap - PAUSE_MAX

    # NOTE-ON
    new_notes = []
    while next_note < len(song.notes) and song.notes[next_note].start <= elapsed:
        nd = song.notes[next_note]
        row = math.floor(map_range(nd.number, song.min_midi, song.max_midi, NUM_ROWS - 1, 0))
        lowness = row / (NUM_ROWS - 1)
        note = {
            "row": row,
            "velocity": nd.velocity,
            "end_time": elapsed + nd.duration,
            "thick": 1 + js_round((MAX_ROWS - 1) * lowness * lowness),
        }
        active_notes.append(note)
        new_notes.append(note)
        # TODO sound: play nd here
        next_note += 1

    # STRIKE + CONNECTOR for new notes
    new_notes.sort(key=lambda n: n["velocity"], reverse=True)
    for n in new_notes:
        for k in range(MIN_DISCS):
            pen.mark_thick(n["row"], p - k, max(n["end_time"], elapsed + STRIKE_HOLD), n["thick"])

        prev = last_note
        if prev and prev["dur"] >= LINE_MIN_DUR and elapsed - prev["end_time"] < 0.5:
            c0 = pen.col(min(prev["end_time"], elapsed))
            for r, c in pen.line(c0, prev["row"], p, n["row"]):
                pen.mark(r, c, elapsed + LINE_HOLD)
        last_note = {"row": n["row"], "end_time": n["end_time"], "dur": n["end_time"] - elapsed}

    # GROW sounding notes at the pen
    for n in sorted(active_notes, key=lambda n: n["velocity"], reverse=True):
        pen.mark_thick(n["row"], p, n["end_time"], n["thick"])

    # END OF SONG: rest, then swoosh, then next song
    if next_note >= len(song.notes) and not active_notes:
        if song_ended_at is None:
            song_ended_at = elapsed
        t = elapsed - song_ended_at

        swoosh_start = SONG_GAP - SWOOSH_TIME
        if t >= swoosh_start:
            col = math.floor((t - swoosh_start) / SWOOSH_TIME * NUM_COLS)
            if col < NUM_COLS:
                for r in range(NUM_ROWS):
                    pen.mark(r, col, elapsed + SWOOSH_HOLD)

        if t > SONG_GAP:
            start_song((song_index + 1) % len(songs))

    show(pen)


def main():
    global songs
    songs = load_playlist()
    if not songs:
        raise SystemExit("no songs loaded - check the music/ folder")

    start_song(0)
    frame = 1 / BOARD_FPS
    try:
        while True:
            frame_start = time.monotonic()
            tick()
            time.sleep(max(0, frame - (time.monotonic() - frame_start)))
    except KeyboardInterrupt:      # Ctrl+C to stop
        print("stopped")


if __name__ == "__main__":
    main()