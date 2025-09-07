import json, os
from colorthief import ColorThief
from utils.colors import rgb_to_hex
import colorsys

# ANSI slots
ANSI_SLOTS = ["black","red","green","yellow","blue","purple","cyan","white"]
BRIGHT_SLOTS = ["brightBlack","brightRed","brightGreen","brightYellow","brightBlue","brightPurple","brightCyan","brightWhite"]

def assign_color_to_slot(rgb):
    """Map RGB to closest ANSI slot by hue."""
    r,g,b = rgb
    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    # hue in 0-1
    if v < 0.2: return "black"
    if s < 0.2 and v > 0.8: return "white"
    if 0 <= h < 1/6: return "red"
    if 1/6 <= h < 1/3: return "yellow"
    if 1/3 <= h < 0.5: return "green"
    if 0.5 <= h < 2/3: return "cyan"
    if 2/3 <= h < 5/6: return "blue"
    return "purple"

def update_terminal_colors_full(image_path):
    thief = ColorThief(image_path)
    palette = thief.get_palette(color_count=12, quality=8)

    # Pad if too small
    while len(palette) < 12:
        palette.append((255,255,255))

    # Background = darkest, Foreground = lightest
    sorted_by_brightness = sorted(palette, key=lambda x: sum(x))
    bg = rgb_to_hex(sorted_by_brightness[0])
    fg = rgb_to_hex(sorted_by_brightness[-1])

    scheme = {
        "name":"WindowDrip",
        "background": bg,
        "foreground": fg
    }

    # assign ANSI slots
    slot_colors = {}
    for c in palette:
        slot = assign_color_to_slot(c)
        if slot not in slot_colors:
            slot_colors[slot] = rgb_to_hex(c)

    # fill ANSI slots and bright slots
    for i, slot in enumerate(ANSI_SLOTS):
        scheme[slot] = slot_colors.get(slot, "#808080")  # fallback gray
        scheme[BRIGHT_SLOTS[i]] = slot_colors.get(slot, "#c0c0c0")  # brighter fallback

    # Path to Windows Terminal settings.json
    settings_path = os.path.expandvars(
        r"%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
    )

    try:
        with open(settings_path,"r",encoding="utf-8") as f:
            settings = json.load(f)

        if "schemes" not in settings:
            settings["schemes"] = []

        # remove old WindowDrip scheme
        settings["schemes"] = [s for s in settings["schemes"] if s.get("name") != "WindowDrip"]
        settings["schemes"].append(scheme)

        # apply scheme to all profiles
        for p in settings.get("profiles",{}).get("list",[]):
            p["colorScheme"]="WindowDrip"

        with open(settings_path,"w",encoding="utf-8") as f:
            json.dump(settings,f,indent=4)

        print(f"[+] Terminal colors Drip Hard applied from {image_path}")

    except Exception as e:
        print(f"[!] Failed to update terminal colors: {e}")
