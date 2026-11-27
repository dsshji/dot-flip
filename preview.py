# digital prorotype same interface

import os
import sys

if os.name == "nt":
    os.system("")

_first_frame = True


def show(pen):
    global _first_frame
    lines = []
    for r in range(pen.num_rows):
        lines.append(" ".join("●" if pen.is_on(r, c) else "·"
                              for c in range(pen.num_cols)))
    sys.stdout.write(("\033[2J" if _first_frame else "") + "\033[H")
    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()
    _first_frame = False