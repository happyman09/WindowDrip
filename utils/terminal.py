import os
import json

def set_terminal_theme(hex_color: str):
    """Update Windows Terminal background color in first scheme."""
    settings_path = os.path.expanduser(
        r"~\AppData\Local\Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"
    )

    if not os.path.exists(settings_path):
        print("[!] Windows Terminal settings.json not found.")
        return

    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    if "schemes" in settings and len(settings["schemes"]) > 0:
        settings["schemes"][0]["background"] = hex_color
        settings["schemes"][0]["foreground"] = "#FFFFFF"

        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4)

        print(f"[+] Terminal theme updated with {hex_color}")
    else:
        print("[!] No schemes found in Terminal settings.")
