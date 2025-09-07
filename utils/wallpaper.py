import ctypes
import os

def set_wallpaper(path: str):
    """Set Windows desktop wallpaper."""
    abs_path = os.path.abspath(path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
    print(f"[+] Wallpaper set: {abs_path}")
