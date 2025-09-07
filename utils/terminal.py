import json, os
from colorthief import ColorThief
from utils.colors import rgb_to_hex

def update_terminal_colors_full(image_path):
    # pull 8 colors from wallpaper
    thief = ColorThief(image_path)
    palette = thief.get_palette(color_count=8, quality=8)

    # pad if palette too small
    while len(palette) < 8:
        palette.append((255,255,255))

    bg = rgb_to_hex(palette[0])
    fg = rgb_to_hex(palette[-1])

    scheme = {
        "name": "WindowDrip",
        "background": bg,
        "foreground": fg,
        "black": rgb_to_hex(palette[0]),
        "red": rgb_to_hex(palette[1]),
        "green": rgb_to_hex(palette[2]),
        "yellow": rgb_to_hex(palette[3]),
        "blue": rgb_to_hex(palette[4]),
        "purple": rgb_to_hex(palette[5]),
        "cyan": rgb_to_hex(palette[6]),
        "white": rgb_to_hex(palette[7]),
        "brightBlack": rgb_to_hex(palette[1]),
        "brightRed": rgb_to_hex(palette[2]),
        "brightGreen": rgb_to_hex(palette[3]),
        "brightYellow": rgb_to_hex(palette[4]),
        "brightBlue": rgb_to_hex(palette[5]),
        "brightPurple": rgb_to_hex(palette[6]),
        "brightCyan": rgb_to_hex(palette[7]),
        "brightWhite": fg
    }

    settings_path = os.path.expandvars(
        r"%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
    )

    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)

        if "schemes" not in settings:
            settings["schemes"] = []

        # nuke old scheme if exists
        settings["schemes"] = [s for s in settings["schemes"] if s.get("name") != "WindowDrip"]
        settings["schemes"].append(scheme)

        # apply to all profiles
        for p in settings.get("profiles", {}).get("list", []):
            p["colorScheme"] = "WindowDrip"

        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

        print(f"[+] Terminal colors riced from {image_path}")

    except Exception as e:
        print(f"[!] couldn’t update terminal colors: {e}")
