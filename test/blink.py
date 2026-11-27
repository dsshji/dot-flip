# Alfa-Zeta XY5 flip-dot driver (EL_PIX14x28 boards), over USB-RS485.
# Frame layout: 0x80, <cmd>, <address>, <column bytes...>, 0x8F
# Command table per github.com/ndsh/flipdots:
#   0x81 = 112 bytes, no auto-refresh    0x82 = 0 bytes, refresh now
#   0x83 =  28 bytes, auto-refresh       0x84 =  28 bytes, no refresh
#   0x85 =  56 bytes, auto-refresh       0x86 =  56 bytes, no refresh
#
# A 14x28 panel is TWO independent 7x28 halves on one PCB

import time

import serial

import flipdot as f

# command style as below to send to the board
s = serial.Serial('COM3', 57600, timeout=1)
for label, addr in (('BROADCAST 0x00', 0x00), ('BOARD4 addr 0x02', 0x02)):
    print('=== %s ===' % label, flush=True)
    for _ in range(3):
        s.write(f.build_frame([0x00] * 28, addr)); s.flush(); time.sleep(0.8)
        s.write(f.build_frame([0x7f] * 28, addr)); s.flush(); time.sleep(0.8)
    s.write(f.build_frame([0x00] * 28, addr)); s.flush(); time.sleep(0.5)
s.close()
print('done')
