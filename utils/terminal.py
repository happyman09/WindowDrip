import json
import os

TERMINAL_SETTINGS_PATH = os.path.expanduser(
    r"%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
)

def update_terminal_colors_full(color_map: dict, force_black_bg: bool = True):
    """
    Update Windows Terminal color scheme with generated colors.
    :param color_map: dict containing ANSI slot → hex mappings
    :param force_black_bg: always keep background pure black if True
    """
    try:
        settings_path = os.path.expandvars(TERMINAL_SETTINGS_PATH)
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        scheme = {
            "name": "WindowDrip",
            "black": color_map.get("black", "#000000"),
            "red": color_map.get("red", "#FF0000"),
            "green": color_map.get("green", "#00FF00"),
            "yellow": color_map.get("yellow", "#FFFF00"),
            "blue": color_map.get("blue", "#0000FF"),
            "purple": color_map.get("purple", "#FF00FF"),
            "cyan": color_map.get("cyan", "#00FFFF"),
            "white": color_map.get("white", "#FFFFFF"),
            "brightBlack": color_map.get("brightBlack", "#808080"),
            "brightRed": color_map.get("brightRed", "#FF5555"),
            "brightGreen": color_map.get("brightGreen", "#55FF55"),
            "brightYellow": color_map.get("brightYellow", "#FFFF55"),
            "brightBlue": color_map.get("brightBlue", "#5555FF"),
            "brightPurple": color_map.get("brightPurple", "#FF55FF"),
            "brightCyan": color_map.get("brightCyan", "#55FFFF"),
            "brightWhite": color_map.get("brightWhite", "#FFFFFF"),
        }

        if force_black_bg:
            scheme["background"] = "#000000"
        else:
            scheme["background"] = color_map.get("black", "#000000")

        scheme["foreground"] = color_map.get("white", "#FFFFFF")

        if "schemes" not in settings:
            settings["schemes"] = []

        # Replace existing WindowDrip scheme if present
        settings["schemes"] = [s for s in settings["schemes"] if s.get("name") != "WindowDrip"]
        settings["schemes"].append(scheme)

        # Apply to all profiles
        for profile in settings.get("profiles", {}).get("list", []):
            profile["colorScheme"] = "WindowDrip"

        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

        print("[+] Terminal colors updated (WindowDrip scheme applied).")

    except Exception as e:
        print(f"[!] Failed to update terminal colors: {e}")


def terminal_color_preview(hex_color: str):
    """
    Prints a preview bar in the terminal using the given hex color.
    Example: terminal_color_preview("#ff9900")
    """
    try:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)

        print("\n[i] WindowDrip Terminal Color Preview:\n")
        for _ in range(3):
            print(f"\033[48;2;{r};{g};{b}m" + " " * 24 + "\033[0m")
        print(f"\n[i] Preview done for {hex_color}.\n")

    except Exception as e:
        print(f"[!] Failed to preview color {hex_color}: {e}")
