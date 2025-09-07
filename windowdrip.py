import sys
from utils.wallpaper import set_wallpaper
from utils.colors import get_dominant_color
from utils.accent import set_accent_color
from utils.terminal import set_terminal_theme

def main(image_path: str):
    print("[*] Applying WindowDrip...")

    set_wallpaper(image_path)
    color = get_dominant_color(image_path)
    print(f"[+] Dominant color extracted: {color}")

    set_accent_color(color)
    set_terminal_theme(color)

    print("[✓] Done. Your desktop drips now.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python windowdrip.py <wallpaper.jpg>")
    else:
        main(sys.argv[1])
