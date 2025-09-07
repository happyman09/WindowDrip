import json
import os

def update_terminal_colors(hex_color):
    """
    Update Windows Terminal settings.json with the given hex color
    for background + foreground.
    """
    settings_path = os.path.expandvars(
        r"%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
    )

    if not os.path.exists(settings_path):
        print("[!] Windows Terminal settings.json not found.")
        return

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        # Apply color to all profiles
        for profile in settings.get("profiles", {}).get("list", []):
            profile["background"] = hex_color
            profile["foreground"] = "#FFFFFF" if is_dark(hex_color) else "#000000"

        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

        print(f"[+] Windows Terminal settings.json updated with {hex_color}")

    except Exception as e:
        print(f"[!] Failed to update terminal colors: {e}")

def is_dark(hex_color):
    """Check if a color is dark based on luminance."""
    hex_color = hex_color.lstrip("#")
    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    luminance = 0.299*r + 0.587*g + 0.114*b
    return luminance < 128
