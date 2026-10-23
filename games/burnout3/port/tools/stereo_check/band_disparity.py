"""The right half's shift against the left in each side-by-side capture of a folder, in bands of the picture below
the HUD: the scenery (30-45% down: far, about +DEPTH of the half's width when the eyes are right), the car's
(55-75%: about -1%), the road under it (85-95%: about 0). A capture whose scenery shift is negative has its eyes
swapped.

    python band_disparity.py <folder>
"""
import sys
from pathlib import Path

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


files = sorted(Path(sys.argv[1]).glob("*.png"))
right = wrong = unsure = 0
for f in files:
    g = np.asarray(Image.open(f).convert("L"), dtype=np.float32)
    h, w2 = g.shape
    w = w2 // 2
    L, R = g[:, :w], g[:, w:2 * w]
    xs = slice(int(w * 0.10), int(w * 0.90))
    out = []
    for name, (a, b) in {"scenery": (0.30, 0.45), "car": (0.55, 0.75), "road": (0.85, 0.95)}.items():
        ys = slice(int(h * a), int(h * b))
        s, r = shift(L[ys, xs], R[ys, xs], max(3, w // 12))
        out.append((name, s, r))
    s, r = out[0][1], out[0][2]
    verdict = "?" if r < 0.5 or s == 0 else ("right" if s > 0 else "SWAPPED")
    right += verdict == "right"
    wrong += verdict == "SWAPPED"
    unsure += verdict == "?"
    print(f.stem, "  ".join("%s %+d (%.2f)" % o for o in out), verdict)
print("eyes right: %d, swapped: %d, unsure: %d (of %d)" % (right, wrong, unsure, len(files)))
