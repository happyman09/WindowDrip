import os
from utils.wallpaper import set_wallpaper
from utils.colors import get_dominant_color
from utils.terminal import update_terminal_colors_full, terminal_color_preview


def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(*rgb)

def drip_wallpaper(wallpaper_path, force_black_bg=True):
    print("[*] Applying WindowDrip (Auto-accent mode)...")

    # Set wallpaper
    set_wallpaper(wallpaper_path)
    print(f"[+] Wallpaper set: {wallpaper_path}")

    # Extract dominant color
    dominant_rgb = get_dominant_color(wallpaper_path)
    print(f"[+] Dominant color extracted: {dominant_rgb}")
    dominant_hex = rgb_to_hex(dominant_rgb)

    # Build color map (simple Drip Hard palette)
    color_map = {
        "black": "#130f11",
        "red": "#d98a52",
        "green": "#808080",
        "yellow": "#a7ac98",
        "blue": "#94939c",
        "purple": "#3a080b",
        "cyan": "#5d5e63",
        "white": "#e0dddd",
        "brightBlack": "#181316",
        "brightRed": "#ffb36a",
        "brightGreen": "#a6a6a6",
        "brightYellow": "#d9dfc5",
        "brightBlue": "#c0bfca",
        "brightPurple": "#4b0a0e",
        "brightCyan": "#787a80",
        "brightWhite": "#ffffff",
    }

    # Apply to terminal
    update_terminal_colors_full(color_map, force_black_bg=force_black_bg)
    print(f"[+] Terminal colors Drip Hard applied from {wallpaper_path}")

    # Show ANSI slot mapping
    print("[i] ANSI Slot mapping:")
    for k, v in color_map.items():
        print(f"   {k}: {v}")

    # Warning for background
    if force_black_bg:
        print("\n[!] Warning: Some profiles may not show true black background.")
        print("[i] Close and reopen Windows Terminal for full effect, and ensure transparency/background image is off.\n")

    # Preview block
    terminal_color_preview(dominant_hex)

    # Sync accent color
    print("[i] Accent color handled by Windows. Make sure Auto accent mode is ON in Settings → Personalization → Colors.")
    print("[✓] Done. Your desktop drips now.")

if __name__ == "__main__":
    # Default test run (replace with your own wallpaper path)
    wallpaper_path = os.path.expanduser(r"C:\Users\mahox\Downloads\car-wallpaper.jpg")
    drip_wallpaper(wallpaper_path, force_black_bg=True)
