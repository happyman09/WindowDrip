import sys, os, ctypes
from utils.colors import get_dominant_color
from utils.terminal import update_terminal_colors_full, terminal_color_preview

def set_wallpaper(image_path):
    """Set the Windows desktop wallpaper."""
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)
    print(f"[+] Wallpaper set: {image_path}")

def main(image_path):
    if not os.path.isfile(image_path):
        print(f"[!] File not found: {image_path}")
        return

    # 1️ Set wallpaper
    set_wallpaper(image_path)

    # 2️ Extract dominant color (optional, for accent info)
    dominant_color = get_dominant_color(image_path)
    print(f"[+] Dominant color extracted: {dominant_color}")

    # 3️ Apply Drip Hard ANSI terminal colors
    update_terminal_colors_full(image_path)

    # 4️ Animated terminal color preview
    terminal_color_preview()

    # 5️ Final info
    print("[i] Accent color handled by Windows. Make sure Auto accent mode is ON in Settings → Personalization → Colors.")
    print("[✓] Done. Your desktop drips now.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python windowdrip.py <image_path>")
    else:
        main(sys.argv[1])
