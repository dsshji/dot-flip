# plays notes on the laptop through Windows' built-in MIDI synth
# (Microsoft GS Wavetable Synth) - no extra installs needed.
# On non-Windows (e.g. the Pi) it silently does nothing.
#
# Each instrument in the MIDI file gets its own channel so it keeps its
# real sound (strings, bass, flute...). Drums always go on channel 10.
import ctypes
import sys

VOLUME_BOOST = 2.5   # multiplies note velocity - these MIDIs are very quiet
MIN_VELOCITY = 40    # quietest a note can be (0-127)
DRUM_CHANNEL = 9     # channel 10 in MIDI-speak

_handle = None
_winmm = None
_channels = {}       # program -> channel
_free = [c for c in range(16) if c != DRUM_CHANNEL]


def open_output(device_id=0):
    global _handle, _winmm
    if sys.platform != "win32":
        print("sound: not on Windows, running silent")
        return
    _winmm = ctypes.windll.winmm
    h = ctypes.c_void_p()
    if _winmm.midiOutOpen(ctypes.byref(h), device_id, 0, 0, 0) != 0:
        print("sound: couldn't open MIDI output, running silent")
        return
    _handle = h
    _winmm.midiOutSetVolume(_handle, 0xFFFFFFFF)  # synth volume to max (L+R)
    for ch in range(16):
        _send(0xB0 | ch, 7, 127)   # channel volume max
        _send(0xB0 | ch, 11, 127)  # expression max


def _send(status, data1, data2):
    if _handle is not None:
        _winmm.midiOutShortMsg(_handle, status | (data1 << 8) | (data2 << 16))


def _channel_for(program, is_drum):
    if is_drum:
        return DRUM_CHANNEL
    if program not in _channels:
        # reuse the oldest channel if a song has more than 15 instruments
        ch = _free[len(_channels) % len(_free)]
        _channels[program] = ch
        _send(0xC0 | ch, program, 0)  # program change = pick instrument
    return _channels[program]


def note_on(pitch, velocity, program=0, is_drum=False):
    """velocity is 0..1 (as stored in songs.Note). Returns the channel used."""
    ch = _channel_for(program, is_drum)
    v = int(velocity * 127 * VOLUME_BOOST)
    _send(0x90 | ch, pitch, max(MIN_VELOCITY, min(127, v)))
    return ch


def note_off(pitch, channel=0):
    _send(0x80 | channel, pitch, 0)


def all_off():
    for ch in range(16):
        _send(0xB0 | ch, 123, 0)  # "all notes off"
    _channels.clear()             # next song assigns instruments fresh


def close():
    global _handle
    if _handle is not None:
        all_off()
        _winmm.midiOutReset(_handle)
        _winmm.midiOutClose(_handle)
        _handle = None
