# bit grid -> serial frames for the 4 panels
#
# panels controlling which rows (top to bottom)
# B1 0-6
# B2 7-13
# B3 14-20
# B4 21-27

# DS1 switches [4, 3, 1, 2] (top to bottom)
import sys

import serial

# laptop (Windows) & Pi (Linux)
PORT = "COM3" if sys.platform == "win32" else "/dev/ttyUSB0"
BAUD = 57600
CMD = 0x83
BOARD_ADR = [0x04, 0x03, 0x01, 0x02]
PANEL_ROWS = 7
PANEL_COLS = 28

ser = serial.Serial(PORT, BAUD)


# what to send in the command for each column
def column_byte(pen, top_row, col):
    b = 0
    for bit in range(PANEL_ROWS):
        if pen.is_on(top_row + bit, col):
            b |= 1 << bit
    return b

def show(pen):
    for i, address in enumerate(BOARD_ADR):
        top_row = i * PANEL_ROWS
        data = [column_byte(pen, top_row, c) for c in range(PANEL_COLS)]
        frame = bytes([0x80, CMD, address] + data + [0x8F])  # header, CMD, which board, data per col, closing
        ser.write(frame)

def close():
    ser.close()