# # digital prorotype same interface

# # ink, mar, markThick, drawLine, penCol

# import * as midiJs from "https://esm.sh/@tonejs/midi";
# let synth;
# let notes_data = [];

# let startMillis;
# let nextNote = 0;

# let activeVoices = 0;
# const MAX_VOICES = 24;
# const DISC_BUDGET = 120;

# let minMidi = 300;
# let maxMidi = 0;

# let minVel = 300;
# let maxVel = 0;

# let minTime = 300;
# let maxTime = 0;

# const MIN_DISCS = 6;
# const MAX_DISCS = 28;

# const MIN_ROWS = 1;
# const MAX_ROWS = 5;

# const LINE_MIN_DUR = 0.1; 
# const BOARD_FPS = 15;
# const BARS_PER_LAP = 3;

# let lastNote = null;
# const PAUSE_MAX = 1.0;

# const SWOOSH_TIME = 1.5;
# const SWOOSH_HOLD = 0.15;

# // ========== LOAD SONGS ================
# const PLAYLIST = ["Rivers In The Desert (Persona 5).mid", "It's Going Down Now (Persona 3 Reload).mid", 'Last Surprise (Persona 5).mid','Beneath The Mask (Persona 5) (1).mid', 'A Way Of Life (Persona 3 Portable).mid', 'Color Your Night (Persona 3 Reload).mid', 'Full Moon Full Life (Persona 3 Reload).mid', 'Heaven (Persona 4) (1).mid', "Persona 3 Reload - When the Moon's Reaching Out Stars.mid", "Pull The Trigger (Persona Q2_ New Cinema Labyrinth).mid", "Take Over (Persona 5 Royal).mid", "Wake Up, Get Up, Get Out There (Persona 5).mid"];
# const SONG_GAP = 4;
# let songs = [], songIndex = 0, songEndedAt = null;

# async function loadSong(file) {
#   const midi = await midiJs.Midi.fromUrl('music/' + file);
#   const notes = [];
#   midi.tracks.forEach((t) => {
#     t.notes.forEach(n => notes.push(new Note(floor(n.midi), n.name, n.time, n.duration, n.velocity)));
#   });
#   if (!notes.length) throw new Error('no notes');
#   const bpm = midi.header.tempos.length ? midi.header.tempos[0].bpm : 120;
#   const num = notes.map(n => n.number), vel = notes.map(n => n.velocity), dur = notes.map(n => n.duration);
#   return { notes, bpm, minMidi: min(num), maxMidi: max(num), minVel: min(vel), maxVel: max(vel),
#          minTime: min(dur), maxTime: max(dur) };
# }

# function startSong(i) {
#   songIndex = i;
#   const s = songs[i];
#   const lapSeconds = BARS_PER_LAP * 4 * 60 / s.bpm;
#   PEN_SPEED = min(num_cols / lapSeconds, BOARD_FPS);
#   ({ minMidi, maxMidi, minVel, maxVel, minTime, maxTime } = s);
#   notes_data = s.notes;
#   nextNote = 0; activeNotes = []; songEndedAt = null;
#   startMillis = millis() - notes_data[0].start * 1000;
#   ink = new Array(num_rows * num_cols).fill(0);
#   lastNote = null;
# }

# // ============ PEN =================

# let PEN_SPEED ;    // columns per second
# let ink = [];
# // ==================================

# let num_rows = 28;
# let num_cols = 28;

# let activeNotes = [];   // { row, endTime }

# let flipCount = 0;


# // ============== DOT =======================
# let dots = [];
# let gap = 3;
# let diameter = 15;

# class Dot {
#   constructor(col, row) {
#     this.col = col;
#     this.row = row;
#     this.diameter = diameter;
#     this.x = (this.diameter+gap)/2 + this.col* (this.diameter+gap);
#     this.y =  (this.diameter+gap)/2 + this.row* (this.diameter+gap);
#     this.lit = false;
#   }

#   draw_dot() {
#     fill(this.lit ? 'red' : 'black');
#     circle(this.x, this.y, this.diameter);
#   }
# }

# // ==========================================

# async function setup() {
#   console.log('hello');
#   createCanvas((diameter+gap)*num_cols, (diameter+gap)*num_rows);
  
#   for (const file of PLAYLIST) {
#     try {
#       songs.push(await loadSong(file));
#       console.log('loaded', file);
#     } catch (e) {
#       console.warn('skipped', file, e.message);
#     }
#   }
#   console.log(`${songs.length}/${PLAYLIST.length} songs ready`);
  
#   frameRate(BOARD_FPS);
#   synth = new p5.PolySynth(p5.MonoSynth, 64);
  
#   ink = new Array(num_rows * num_cols).fill(0);

#   // ====== DOTS GENERATION ========
#   for (let row = 0; row < num_rows; row += 1) {
#     for (let col = 0; col < num_cols; col += 1) {
#       dots.push(new Dot(col, row));
#     }
#   }
# }

# class Note {
#   constructor(number, name, start, duration, velocity) {
#     this.number = number;
#     this.name = name;
#     this.start = start;
#     this.duration = duration;
#     this.velocity = velocity;
#   }

#   play_note() {
#     if (activeVoices < MAX_VOICES) {
#       synth.play(this.name, 0.3, 0, this.duration);
#       activeVoices++;
#       setTimeout(() => activeVoices--, this.duration * 1000);
#     }
#   }
# }


# // ==================== PEN WRITE ===============================

# const penCol = t => floor(t * PEN_SPEED) % num_cols;
# const idx = (r, c) => r * num_cols + ((c % num_cols) + num_cols) % num_cols;

# let used = 0;   // discs turned on this frame

# let now = 0;
# const STRIKE_HOLD = 0.12;
# const LINE_HOLD   = 0.2;

# function mark(r, c, until) {
#   const i = idx(r, c);
#   if (ink[i] > now) { ink[i] = max(ink[i], until); return; }
#   if (used >= DISC_BUDGET) return;
#   ink[i] = until;
#   used++;
# }

# function markThick(row, col, until, thick) {
#   const top = row - (thick - 1);
#   for (let k = 0; k < thick; k++) {
#     const r = top + k;
#     if (r >= 0 && r < num_rows) mark(r, col, until);
#   }
# }

# function drawLine(c0, r0, c1, r1) {
#   if (c1 < c0) c1 += num_cols;
#   const addC = c1 < c0 ? -1 : 1;
#   const addR = r1 < r0 ? -1 : 1;
#   const dc = Math.abs(c1 - c0);
#   const dr = Math.abs(r1 - r0);
#   let c = c0, r = r0;
#   const recorded = [{ col: c, row: r }];

#   if (dr >= dc) {
#     let p = 2 * dc - dr;
#     for (let k = 0; k < dr; k++) {
#       r += addR;
#       if (p >= 0) { c += addC; p += 2 * dc - 2 * dr; }
#       else        { p += 2 * dc; }
#       recorded.push({ col: c, row: r });
#     }
#   } else {
#     let p = 2 * dr - dc;
#     for (let k = 0; k < dc; k++) {
#       c += addC;
#       if (p >= 0) { r += addR; p += 2 * dr - 2 * dc; }
#       else        { p += 2 * dr; }
#       recorded.push({ col: c, row: r });
#     }
#   }
#   return recorded;
# }

# // ==============================================================

