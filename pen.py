# ink, mar, markThick, drawLine, penCol

import math

STRIKE_HOLD = 0.12
LINE_HOLD = 0.2


class Pen:
    def __init__(self, num_rows=28, num_cols=28, budget=120):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.budget = budget
        self.speed = 6
        self.reset()

    def reset(self):
        self.ink = [0.0] * (self.num_rows * self.num_cols)
        self.now = 0.0
        self.used = 0

    def begin_frame(self, now):
        self.now = now
        self.used = 0

    # ---------- addressing ----------
    def col(self, t):
        return math.floor(t * self.speed) % self.num_cols

    def idx(self, r, c):
        return r * self.num_cols + c % self.num_cols

    def is_on(self, r, c):
        return self.ink[self.idx(r, c)] > self.now

    # ---------- drawing ----------
    def mark(self, r, c, until):
        i = self.idx(r, c)
        if self.ink[i] > self.now:
            self.ink[i] = max(self.ink[i], until)
            return
        if self.used >= self.budget:
            return
        self.ink[i] = until
        self.used += 1

    def mark_thick(self, row, col, until, thick):
        top = row - (thick - 1)
        for r in range(top, top + thick):
            if 0 <= r < self.num_rows:
                self.mark(r, col, until)

    def line(self, c0, r0, c1, r1):
        if c1 < c0:
            c1 += self.num_cols
        add_c = -1 if c1 < c0 else 1
        add_r = -1 if r1 < r0 else 1
        dc = abs(c1 - c0)
        dr = abs(r1 - r0)
        c, r = c0, r0
        cells = [(r, c)]

        if dr >= dc:
            p = 2 * dc - dr
            for _ in range(dr):
                r += add_r
                if p >= 0:
                    c += add_c
                    p += 2 * dc - 2 * dr
                else:
                    p += 2 * dc
                cells.append((r, c))
        else:
            p = 2 * dr - dc
            for _ in range(dc):
                c += add_c
                if p >= 0:
                    r += add_r
                    p += 2 * dr - 2 * dc
                else:
                    p += 2 * dr
                cells.append((r, c))
        return cells