import json, os
from colorthief import ColorThief
from utils.colors import rgb_to_hex
import colorsys
import sys, time

ANSI_SLOTS = ["black","red","green","yellow","blue","purple","cyan","white"]
BRIGHT_SLOTS = ["brightBlack","brightRed","brightGreen","brightYellow",
                "brightBlue","brightPurple","brightCyan","brightWhite"]

def assign_color_to_slot(rgb):
    r,g,b = rgb
    h,s,v = colorsys.rgb_to_hsv(r/255,g/255,b/255)
    if v < 0.2: return "black"
    if s < 0.2 and v > 0.8: return "white"
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
    """Apply wallpaper-driven ANSI colors to Windows Terminal."""
    thief = ColorThief(image_path)
    palette = thief.get_palette(color_count=16, quality=8)
    while len(palette) < 16:
        palette.append((255,255,255))
    sorted_by_brightness = sorted(palette, key=lambda x: sum(x))

    bg = "#000000"  # force black
    fg_color = sorted_by_brightness[-1]
    fg = rgb_to_hex(brighten_color(fg_color, factor=1.4))
    scheme = {"name":"WindowDrip","background":bg,"foreground":fg}

    slot_colors = {}
    for c in palette:
        slot = assign_color_to_slot(c)
        if slot not in slot_colors:
            slot_colors[slot] = c

    for i, slot in enumerate(ANSI_SLOTS):
        rgb = slot_colors.get(slot,(128,128,128))
        scheme[slot] = rgb_to_hex(rgb)
        scheme[BRIGHT_SLOTS[i]] = rgb_to_hex(brighten_color(rgb))

    settings_path = os.path.expandvars(
        r"%LOCALAPPDATA%\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
    )

    try:
        with open(settings_path,"r",encoding="utf-8") as f:
            settings = json.load(f)

        if "schemes" not in settings:
            settings["schemes"] = []

        settings["schemes"] = [s for s in settings["schemes"] if s.get("name")!="WindowDrip"]
        settings["schemes"].append(scheme)

        black_ok = True
        for p in settings.get("profiles",{}).get("list",[]):
            p["colorScheme"]="WindowDrip"
            p["useAcrylic"]=False
            p["backgroundImage"]=""
            if p.get("background","#000000").lower() != "#000000":
                black_ok = False

        with open(settings_path,"w",encoding="utf-8") as f:
            json.dump(settings,f,indent=4)

        print(f"[+] Terminal colors Drip Hard applied from {image_path}")
        print("[i] ANSI Slot mapping:")
        for slot in ANSI_SLOTS + BRIGHT_SLOTS:
            print(f"   {slot}: {scheme[slot]}")

        if not black_ok:
            print("\n[!] Warning: Some profiles may not show true black background.")
            print("[i] Close and reopen Windows Terminal for full effect, and ensure transparency/background image is off.")

    except Exception as e:
        print(f"[!] Failed to update terminal colors: {e}")

def terminal_color_preview():
    """Animated 16-color preview of ANSI slots in Terminal."""
    ANSI_SLOTS_ALL = [
        "\033[0;30m", "\033[0;31m", "\033[0;32m", "\033[0;33m",
        "\033[0;34m", "\033[0;35m", "\033[0;36m", "\033[0;37m",
        "\033[1;30m", "\033[1;31m", "\033[1;32m", "\033[1;33m",
        "\033[1;34m", "\033[1;35m", "\033[1;36m", "\033[1;37m",
    ]
    print("\n[i] WindowDrip Terminal Color Preview:\n")
    try:
        for _ in range(3):  # loop 3 times
            for code in ANSI_SLOTS_ALL:
                sys.stdout.write(code + "█")
                sys.stdout.flush()
                time.sleep(0.05)
            sys.stdout.write("\033[0m\n")  # reset + newline
            time.sleep(0.2)
        print("\033[0m[i] Preview done. Colors applied!\n")
    except KeyboardInterrupt:
        print("\033[0m[i] Preview interrupted. Colors still applied.\n")
