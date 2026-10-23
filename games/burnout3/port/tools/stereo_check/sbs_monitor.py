"""Watches the Burnout 3 window's side-by-side picture (PrintWindow, so other windows on top do not
matter) about 10 times a second and logs, per capture:

    dL, dR    how much each half changed since the last capture (mean abs, 0-255)
    dx, dy    the right half's shift against the left (phase correlation, quarter size px)
    peak      the correlation's strength (1 = the halves the same picture, shifted)
    resid     what is left between the halves after that shift (mean abs)

A capture where one half moves while the other stays, or the halves are apart vertically, or they
stop looking alike, saves the last 30 captures to <out>\\event_<n>\\. A file "dump" in <out> saves
them on demand.

    python sbs_monitor.py <out folder> [minutes]
"""
import csv
import ctypes
import ctypes.wintypes as wt
import sys
import time
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
try:
    user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))   # per monitor v2
except Exception:
    user32.SetProcessDPIAware()


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wt.DWORD), ("biWidth", wt.LONG), ("biHeight", wt.LONG), ("biPlanes", wt.WORD),
                ("biBitCount", wt.WORD), ("biCompression", wt.DWORD), ("biSizeImage", wt.DWORD),
                ("biXPelsPerMeter", wt.LONG), ("biYPelsPerMeter", wt.LONG), ("biClrUsed", wt.DWORD),
                ("biClrImportant", wt.DWORD)]


def find_window():
    return user32.FindWindowW(None, "Burnout 3: Takedown")


def grab(hwnd):
    r = wt.RECT()
    if not user32.GetClientRect(hwnd, ctypes.byref(r)) or r.right <= 0 or r.bottom <= 0:
        return None
    w, h = r.right, r.bottom
    wdc = user32.GetDC(hwnd)
    mdc = gdi32.CreateCompatibleDC(wdc)
    bmp = gdi32.CreateCompatibleBitmap(wdc, w, h)
    old = gdi32.SelectObject(mdc, bmp)
    ok = user32.PrintWindow(hwnd, mdc, 3)                      # client only, full content
    bi = BITMAPINFOHEADER(ctypes.sizeof(BITMAPINFOHEADER), w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mdc, bmp, 0, h, buf, ctypes.byref(bi), 0)
    gdi32.SelectObject(mdc, old)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mdc)
    user32.ReleaseDC(hwnd, wdc)
    if not ok:
        return None
    a = np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4)
    return a[::4, ::4, 2::-1].copy()                          # quarter size, BGRA -> RGB


def shift(a, b):
    wy = np.hanning(a.shape[0])[:, None]
    wx = np.hanning(a.shape[1])[None, :]
    fa = np.fft.rfft2((a - a.mean()) * wy * wx)
    fb = np.fft.rfft2((b - b.mean()) * wy * wx)
    r = fb * np.conj(fa)
    r /= np.abs(r) + 1e-9
    c = np.fft.irfft2(r, s=a.shape)
    y, x = np.unravel_index(np.argmax(c), c.shape)
    if y > c.shape[0] // 2: y -= c.shape[0]
    if x > c.shape[1] // 2: x -= c.shape[1]
    return int(x), int(y), float(c.max())


def main():
    out = Path(sys.argv[1])
    minutes = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0
    save_all = len(sys.argv) > 3 and sys.argv[3] == "all"     # every capture into <out>/all/
    out.mkdir(parents=True, exist_ok=True)
    if save_all:
        (out / "all").mkdir(exist_ok=True)
    ring = deque(maxlen=30)
    prev = None
    events = 0
    last_event = 0.0
    t_end = time.time() + 60 * minutes
    with open(out / "log.csv", "w", newline="") as f:
        log = csv.writer(f)
        # qpc_ms: the performance counter in ms, as the port's "[stereo] picture" lines (steady_clock, modulo 1e5 s)
        log.writerow(["time", "qpc_ms", "dL", "dR", "dx", "dy", "peak", "resid", "flag"])
        while time.time() < t_end:
            t0 = time.time()
            qpc_ms = (time.perf_counter() * 1e6 % 1e8) / 1000.0
            hwnd = find_window()
            img = grab(hwnd) if hwnd else None
            if img is None:
                time.sleep(1.0)
                continue
            g = img.astype(np.float32).mean(axis=2)
            w = g.shape[1] // 2
            L, R = g[:, :w], g[:, w:2 * w]
            dx, dy, peak = shift(L, R)
            Rs = np.roll(R, (-dy, -dx), axis=(0, 1))
            resid = float(np.abs(L[8:-8, 40:-40] - Rs[8:-8, 40:-40]).mean())
            dL = dR = 0.0
            if prev is not None and prev[0].shape == L.shape:
                dL = float(np.abs(L - prev[0]).mean())
                dR = float(np.abs(R - prev[1]).mean())
            prev = (L, R)
            flags = []
            if abs(dy) >= 2: flags.append("vertical")
            if (dR > 3.0 and dL < 0.5) or (dL > 3.0 and dR < 0.5): flags.append("one-half")
            if peak < 0.08 and resid > 12.0: flags.append("unalike")
            if resid < 1.0 and peak > 0.9: flags.append("flat")
            stamp = time.strftime("%H:%M:%S", time.localtime(t0)) + f".{int((t0 % 1) * 10)}"
            ring.append((stamp, img))
            if save_all and (dL > 2.0 and dR > 2.0):           # moving: a race
                Image.fromarray(img).save(out / "all" / f"{stamp.replace(':', '')}.png")
            log.writerow([stamp, f"{qpc_ms:.1f}", f"{dL:.2f}", f"{dR:.2f}", dx, dy, f"{peak:.2f}", f"{resid:.2f}",
                          "+".join(flags)])
            f.flush()
            dump = out / "dump"
            if (flags and t0 - last_event > 5.0) or dump.exists():
                events += 1
                last_event = t0
                d = out / f"event_{events:02d}_{stamp.replace(':', '')}"
                d.mkdir(exist_ok=True)
                for s, im in ring:
                    Image.fromarray(im).save(d / f"{s.replace(':', '')}.png")
                if dump.exists():
                    dump.unlink()
                print(f"{stamp} saved {d.name} ({'+'.join(flags) or 'on demand'})", flush=True)
            time.sleep(max(0.0, 0.1 - (time.time() - t0)))
    print("done", flush=True)


if __name__ == "__main__":
    main()
