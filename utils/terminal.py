import json, os
from colorthief import ColorThief
from utils.colors import rgb_to_hex
import colorsys

ANSI_SLOTS = ["black","red","green","yellow","blue","purple","cyan","white"]
BRIGHT_SLOTS = ["brightBlack","brightRed","brightGreen","brightYellow","brightBlue","brightPurple","brightCyan","brightWhite"]

def assign_color_to_slot(rgb):
    r,g,b = rgb
    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    # background/foreground handled separately
    if v < 0.2: return "black"
    if s < 0.2 and v > 0.8: return "white"
    # hue buckets
    if 0 <= h < 1/6: return "red"
    if 1/6 <= h < 1/3: return "yellow"
    if 1/3 <= h < 0.5: return "green"
    if 0.5 <= h < 2/3: return "cyan"
    if 2/3 <= h < 5/6: return "blue"
    return "purple"

def brighten_color(rgb, factor=1.3):
    r,g,b = rgb
    r = min(int(r*factor),255)
    g = min(int(g*factor),255)
    b = min(int(b*factor),255)
    return (r,g,b)

def update_terminal_colors_full(image_path):
    thief = ColorThief(image_path)
    palette = thief.get_palette(color_count=16, quality=8)

    # pad if too small
    while len(palette) < 16:
        palette.append((255,255,255))

    # Background = darkest, Foreground = lightest
    sorted_by_brightness = sorted(palette, key=lambda x: sum(x))
    bg = rgb_to_hex(sorted_by_brightness[0])
    fg = rgb_to_hex(sorted_by_brightness[-1])

    scheme = {"name":"WindowDrip","background":bg,"foreground":fg}

    slot_colors = {}
    # assign normal slots
    for c in palette:
        slot = assign_color_to_slot(c)
        if slot not in slot_colors:
            slot_colors[slot] = c

    # assign ANSI slots
    for i, slot in enumerate(ANSI_SLOTS):
        rgb = slot_colors.get(slot,(128,128,128))
        scheme[slot] = rgb_to_hex(rgb)
        # bright slot = brighter version
        scheme[BRIGHT_SLOTS[i]] = rgb_to_hex(brighten_color(rgb))

    # path to settings.json
    settings_path = os.path.expandvars(
        r"%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
    )

    try:
        with open(settings_path,"r",encoding="utf-8") as f:
            settings = json.load(f)

        if "schemes" not in settings:
            settings["schemes"] = []

        # remove old WindowDrip scheme
        settings["schemes"] = [s for s in settings["schemes"] if s.get("name")!="WindowDrip"]
        settings["schemes"].append(scheme)

        # apply scheme to all profiles
        for p in settings.get("profiles",{}).get("list",[]):
            p["colorScheme"]="WindowDrip"

        with open(settings_path,"w",encoding="utf-8") as f:
            json.dump(settings,f,indent=4)

        # log mapping
        print(f"[+] Terminal colors Drip Hard applied from {image_path}")
        print("[i] ANSI Slot mapping:")
        for slot in ANSI_SLOTS + BRIGHT_SLOTS:
            print(f"   {slot}: {scheme[slot]}")

    except Exception as e:
        print(f"[!] Failed to update terminal colors: {e}")
