import pygetwindow as gw
from PIL import ImageGrab


def capture_chrome_window(file_path):
    chrome_windows = gw.getWindowsWithTitle("Google Chrome")

    if not chrome_windows:
        raise RuntimeError("Chrome window not found")

    window = chrome_windows[0]

    left = int(window.left)
    top = int(window.top)
    right = int(window.right)
    bottom = int(window.bottom)

    screenshot = ImageGrab.grab(
        bbox=(left, top, right, bottom)
    )

    screenshot.save(file_path)