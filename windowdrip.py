import sys
import os
import ctypes
from utils.colors import get_dominant_color, rgb_to_hex
from utils.terminal import update_terminal_colors

SPI_SETDESKWALLPAPER = 20

def set_wallpaper(image_path):
    abs_path = os.path.abspath(image_path)
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, abs_path, 3)
    print(f"[+] Wallpaper set: {abs_path}")

def main(image_path):
    print("[*] Applying WindowDrip (Auto-accent mode)...")

    # 1. Set wallpaper
    set_wallpaper(image_path)

    # 2. Extract dominant color for terminal
    color = get_dominant_color(image_path)
    hex_color = rgb_to_hex(color)
    print(f"[+] Dominant color extracted: {hex_color}")

    # 3. Update Windows Terminal colors
    update_terminal_colors(hex_color)
    print(f"[+] Terminal theme updated with {hex_color}")

    # 4. Accent handled by Windows (Auto mode)
    print("[i] Accent color handled by Windows. Make sure Auto accent mode is ON in Settings → Personalization → Colors.")

    print("[✓] Done. Your desktop drips now.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python windowdrip.py <path_to_wallpaper>")
    else:
        main(sys.argv[1])
