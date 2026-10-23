"""Every half second for N seconds: the Burnout 3 window's rectangle, client size, style and (PrintWindow) its
picture at half size into <out>/probe_NN.png; a line each into <out>/probe.txt.

    python window_probe.py <out> [seconds]
"""
import ctypes
import ctypes.wintypes as wt
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

user32 = ctypes.windll.user32
gdi32 = ctypes.windll.gdi32
try:
    user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
except Exception:
    user32.SetProcessDPIAware()
user32.GetWindowLongW.restype = ctypes.c_long


class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [("biSize", wt.DWORD), ("biWidth", wt.LONG), ("biHeight", wt.LONG), ("biPlanes", wt.WORD),
                ("biBitCount", wt.WORD), ("biCompression", wt.DWORD), ("biSizeImage", wt.DWORD),
                ("biXPelsPerMeter", wt.LONG), ("biYPelsPerMeter", wt.LONG), ("biClrUsed", wt.DWORD),
                ("biClrImportant", wt.DWORD)]


def grab(hwnd, w, h):
    wdc = user32.GetDC(hwnd)
    mdc = gdi32.CreateCompatibleDC(wdc)
    bmp = gdi32.CreateCompatibleBitmap(wdc, w, h)
    old = gdi32.SelectObject(mdc, bmp)
    ok = user32.PrintWindow(hwnd, mdc, 3)
    bi = BITMAPINFOHEADER(ctypes.sizeof(BITMAPINFOHEADER), w, -h, 1, 32, 0, 0, 0, 0, 0, 0)
    buf = ctypes.create_string_buffer(w * h * 4)
    gdi32.GetDIBits(mdc, bmp, 0, h, buf, ctypes.byref(bi), 0)
    gdi32.SelectObject(mdc, old)
    gdi32.DeleteObject(bmp)
    gdi32.DeleteDC(mdc)
    user32.ReleaseDC(hwnd, wdc)
    return np.frombuffer(buf, dtype=np.uint8).reshape(h, w, 4)[:, :, 2::-1] if ok else None


out = Path(sys.argv[1])
seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
every = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
out.mkdir(parents=True, exist_ok=True)
lines = []
end = time.time() + seconds
n = 0
while time.time() < end:
    hwnd = user32.FindWindowW(None, "Burnout 3: Takedown")
    if hwnd:
        r = wt.RECT()
        user32.GetWindowRect(hwnd, ctypes.byref(r))
        c = wt.RECT()
        user32.GetClientRect(hwnd, ctypes.byref(c))
        style = user32.GetWindowLongW(hwnd, -16) & 0xFFFFFFFF
        caption = bool(style & 0x00C00000)
        img = grab(hwnd, c.right, c.bottom) if c.right > 0 and c.bottom > 0 else None
        if img is not None:
            Image.fromarray(img).resize((c.right // 2, c.bottom // 2)).save(out / ("probe_%02d.png" % n))
        lines.append("%s probe_%02d window (%d,%d)-(%d,%d) client %dx%d style 0x%08X caption %s"
                     % (time.strftime("%H:%M:%S"), n, r.left, r.top, r.right, r.bottom, c.right, c.bottom, style,
                        caption))
        n += 1
    elif n:
        break                                   # the window gone: the run is over
    time.sleep(every)
(out / "probe.txt").write_text("\n".join(lines) + "\n")
print("\n".join(lines[-3:]))
