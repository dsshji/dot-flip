# the actual loop to send commands
# setup and draw loop
import math
import time

from pen import STRIKE_HOLD, LINE_HOLD, Pen
from songs import load_playlist
from preview import show

MIN_DISCS = 6
MAX_DISCS = 28

MIN_ROWS = 1
MAX_ROWS = 5

LINE_MIN_DUR = 0.1
BOARD_FPS = 15
BARS_PER_LAP = 3

PAUSE_MAX = 1.0

SWOOSH_TIME = 1.5
SWOOSH_HOLD = 0.15

SONG_GAP = 4

global songs
global songIndex
global songEndedAt
global nextNote
global activeNotes
global songEndedAt
global songIndex
global song
global lastNote

songs = []
songIndex = 0
songEndedAt = None
nextNote = 0
activeNotes = []
songEndedAt = None
songIndex = 0
song = songs[songIndex]
lastNote = None

# startMillis = millis() - notes_data[0].start * 1000

num_cols = 28
num_rows = 28

pen = Pen(num_rows, num_cols, 120)

def start_song(i):
    songIndex = i
    song = songs[i]

    lapSeconds = BARS_PER_LAP * 4 * 60 / song.bpm
    pen.reset()
    pen.speed(min(num_cols / lapSeconds, BOARD_FPS))

    nextNote = 0
    activeNotes = []
    songEndedAt = None
    lastNote = None

    start_time = time.monotonic() - song.notes[0].start

def tick():
    elapsed = (millis() - startMillis) / 1000
    pen.begin_frame(elapsed)
    p = pen.col(elapsed)
    used = 0

    activeNotes = activeNotes.filter(n => n.endTime > elapsed)

    #   // skip long silences
    #   if (activeNotes.length === 0 && nextNote < notes_data.length) {
    #     gap = notes_data[nextNote].start - elapsed;
    #     if (gap > PAUSE_MAX) startMillis -= (gap - PAUSE_MAX) * 1000;
    #   }



#   // NOTE-ON
#   newNotes = [];
#   while (nextNote < notes_data.length && notes_data[nextNote].start <= elapsed) {
#     thick = newNotes.length >= 4 ? 3 : 1;
#     nd = notes_data[nextNote];
#     row = floor(map(nd.number, minMidi, maxMidi, num_rows - 1, 0));
#     vn = maxVel > minVel ? (nd.velocity - minVel) / (maxVel - minVel) : 0.5;
#     lowness = row / (num_rows - 1);
# note = { row, velocity: nd.velocity, endTime: elapsed + nd.duration,
#                thick: 1 + round((MAX_ROWS - 1) * lowness * lowness) };
#     activeNotes.push(note);
#     newNotes.push(note);
#     nd.play_note();   
#     nextNote++;
#   }

#   // STRIKE + CONNECTOR for new notes
#   newNotes.sort((a, b) => b.velocity - a.velocity);
#   for (n of newNotes) {
#     for (let k = 0; k < MIN_DISCS; k++) markThick(n.row, p - k, max(n.endTime, now + STRIKE_HOLD), n.thick);

#     prev = lastNote;
#     if (prev && prev.dur >= LINE_MIN_DUR && elapsed - prev.endTime < 0.5) {
#       c0 = penCol(min(prev.endTime, elapsed));
#       for (cell of drawLine(c0, prev.row, p, n.row)) mark(cell.row, cell.col, now + LINE_HOLD);
#     }
#     lastNote = { row: n.row, endTime: n.endTime, dur: n.endTime - now };
#   }

#   // GROW sounding notes at the pen
#   ranked = [...activeNotes].sort((a, b) => b.velocity - a.velocity);
#   for (n of ranked) markThick(n.row, p, n.endTime, n.thick);

#   // END OF SONG: rest, then swoosh, then next song
#   if (nextNote >= notes_data.length && activeNotes.length === 0) {
#     if (songEndedAt === null) songEndedAt = elapsed;
#     t = elapsed - songEndedAt;
  
#     swooshStart = SONG_GAP - SWOOSH_TIME;     // quiet first, swoosh at the end of the gap
#     if (t >= swooshStart) {
#       col = floor((t - swooshStart) / SWOOSH_TIME * num_cols);
#       if (col < num_cols) {
#         for (let r = 0; r < num_rows; r++) mark(r, col, now + SWOOSH_HOLD);
#       }
#     }
  
#     if (t > SONG_GAP) startSong((songIndex + 1) % songs.length);
#   }

songs = load_playlist()
if not songs: return
start_song(0)
while True:
    tick()

# хз бля че там еще
