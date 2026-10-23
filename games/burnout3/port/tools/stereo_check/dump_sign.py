"""In a dumped stereo run (--frames, PS2HOST_STEREO_LOG): for each right eye's picture with the left eye's before
it, the scenery band's shift of the right against the left (30-45% down; +DEPTH when the eyes are right).

    python dump_sign.py <frames dir> <run log> [from] [to]
"""
import os
import re
import sys

import numpy as np
from PIL import Image


def shift(a, b, most):
    best, best_s = -2.0, 0
    w = a.shape[1]
    for s in range(-most, most + 1):
        x, y = (a[:, : w - s], b[:, s:]) if s >= 0 else (a[:, -s:], b[:, : w + s])
        x = x - x.mean()
        y = y - y.mean()
        d = np.sqrt((x * x).sum() * (y * y).sum())
        r = float((x * y).sum() / d) if d else -1.0
        if r > best:
            best, best_s = r, s
    return best_s, best


folder, log = sys.argv[1], sys.argv[2]
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0
hi = int(sys.argv[4]) if len(sys.argv) > 4 else 1 << 30
eyes = {}
for line in open(log, encoding="utf-8", errors="replace"):
    m = re.match(r"\[stereo\] frame (\d+) dumped: eye (\d)", line)
    if m:
        eyes[int(m.group(1))] = int(m.group(2))
frames = [f for f in sorted(int(n[6:12]) for n in os.listdir(folder) if re.fullmatch(r"frame_\d{6}\.bmp", n))
          if lo <= f <= hi]
pos = neg = 0
shifts = []
left = None
for fr in frames:
    eye = eyes.get(fr, -1)
    g = np.asarray(Image.open(os.path.join(folder, "frame_%06d.bmp" % fr)).convert("L"), dtype=np.float32)
    if eye == 1:
        left = g
        continue
    if eye != 2 or left is None:
        continue
    h, w = g.shape
    ys, xs = slice(int(h * 0.30), int(h * 0.45)), slice(int(w * 0.10), int(w * 0.90))
    s, r = shift(left[ys, xs], g[ys, xs], w // 12)
    if r > 0.5 and s:
        pos += s > 0
        neg += s < 0
        shifts.append(s)
print("pairs with a clear scenery shift: right-eye-to-the-right (eyes right) %d, to the left (swapped) %d; "
      "median %+d px of %d" % (pos, neg, int(np.median(shifts)) if shifts else 0, w))
