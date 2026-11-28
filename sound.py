# plays the notes out loud
#   Windows (laptop): Windows' built-in MIDI synth, no extra installs.
#   Linux (the Pi):   FluidSynth + a General MIDI soundfont
#                     (sudo apt install fluidsynth fluid-soundfont-gm,
#                      pip install pyfluidsynth)
#
import ctypes
import os
import sys

VOLUME_BOOST = 2.5
MIN_VELOCITY = 40
DRUM_CHANNEL = 9

# --- Pi / FluidSynth  ---
FS_GAIN = 0.4
ALSA_DEVICE = None
SOUNDFONTS = [
    "/usr/share/sounds/sf2/FluidR3_GM.sf2",
    "/usr/share/sounds/sf2/default-GM.sf2",
]

_backend = None
_handle = None
_winmm = None
_fs = None
_sfid = None
_channels = {}
_free = [c for c in range(16) if c != DRUM_CHANNEL]


# ================= opening =================
def open_output(device_id=0):
    if sys.platform == "win32":
        _open_windows(device_id)
    else:
        _open_fluidsynth()
    if _backend is None:
        print("sound: no synth available, running silent")
    else:
        print("sound:", _backend)


def _open_windows(device_id):
    global _backend, _handle, _winmm
    _winmm = ctypes.windll.winmm
    h = ctypes.c_void_p()
    if _winmm.midiOutOpen(ctypes.byref(h), device_id, 0, 0, 0) != 0:
        return
    _handle = h
    _backend = "win"
    _winmm.midiOutSetVolume(_handle, 0xFFFFFFFF)
    for ch in range(16):
        _cc(ch, 7, 127)    # channel volume max
        _cc(ch, 11, 127)   # expression max


def _open_fluidsynth():
    global _backend, _fs, _sfid
    try:
        import fluidsynth
    except Exception as e:
        print("sound: FluidSynth not available -", e)
        return
    sf = next((p for p in SOUNDFONTS if os.path.exists(p)), None)
    if sf is None:
        print("sound: no soundfont found - sudo apt install fluid-soundfont-gm")
        return
    _fs = fluidsynth.Synth(gain=FS_GAIN)
    if ALSA_DEVICE:
        _fs.setting("audio.alsa.device", ALSA_DEVICE)
    _fs.start(driver="alsa")
    _sfid = _fs.sfload(sf)
    _backend = "fs"
    _fs.program_select(DRUM_CHANNEL, _sfid, 128, 0)
    for ch in range(16):
        _cc(ch, 7, 127)
        _cc(ch, 11, 127)


# ============ the few MIDI actions, one per backend ============
def _cc(ch, control, value):
    if _backend == "win":
        _send(0xB0 | ch, control, value)
    elif _backend == "fs":
        _fs.cc(ch, control, value)


def _program(ch, program):
    if _backend == "win":
        _send(0xC0 | ch, program, 0)
    elif _backend == "fs":
        _fs.program_select(ch, _sfid, 0, program)


def _noteon(ch, pitch, vel):
    if _backend == "win":
        _send(0x90 | ch, pitch, vel)
    elif _backend == "fs":
        _fs.noteon(ch, pitch, vel)


def _noteoff(ch, pitch):
    if _backend == "win":
        _send(0x80 | ch, pitch, 0)
    elif _backend == "fs":
        _fs.noteoff(ch, pitch)


def _send(status, data1, data2):
    _winmm.midiOutShortMsg(_handle, status | (data1 << 8) | (data2 << 16))


# ================= used by main.py =================
def _channel_for(program, is_drum):
    if is_drum:
        return DRUM_CHANNEL
    if program not in _channels:
        # reuse the oldest channel if a song has more than 15 instruments
        ch = _free[len(_channels) % len(_free)]
        _channels[program] = ch
        _program(ch, program)   # program change = pick instrument
    return _channels[program]


def note_on(pitch, velocity, program=0, is_drum=False):
    """velocity is 0..1 (as stored in songs.Note). Returns the channel used."""
    ch = _channel_for(program, is_drum)
    v = int(velocity * 127 * VOLUME_BOOST)
    _noteon(ch, pitch, max(MIN_VELOCITY, min(127, v)))
    return ch


def note_off(pitch, channel=0):
    _noteoff(channel, pitch)


def all_off():
    for ch in range(16):
        _cc(ch, 123, 0)   # "all notes off"
    _channels.clear()     # next song assigns instruments fresh


def close():
    global _backend, _handle, _fs
    if _backend is None:
        return
    all_off()
    if _backend == "win":
        _winmm.midiOutReset(_handle)
        _winmm.midiOutClose(_handle)
        _handle = None
    elif _backend == "fs":
        _fs.delete()
        _fs = None
    _backend = None
