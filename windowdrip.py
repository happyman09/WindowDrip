import argparse
import os
import subprocess
import sys

from utils.wallpaper import set_wallpaper
from utils.colors import get_dominant_hex
from utils.accent import set_windows_accent, hex_to_bgr_dword
from utils.terminal import find_windows_terminal_settings, backup_settings, inject_color_scheme

def run_powershell(cmd):
    # Helper fallback for operations that might need powershell
    subprocess.run(["powershell", "-NoProfile", "-Command", cmd], shell=True)

def try_refresh_ui():
    # Try using RUNDLL32 as fallback
    try:
        subprocess.run(["RUNDLL32.EXE", "user32.dll,UpdatePerUserSystemParameters"], check=True)
    except Exception:
        pass

def apply_wallpaper(image_path):
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    print("[*] Setting wallpaper...")
    set_wallpaper(image_path)

    print("[*] Extracting dominant color...")
    hex_color = get_dominant_hex(image_path)
    print(f"[+] Dominant color: {hex_color}")

    print("[*] Applying accent color...")
    try:
        set_windows_accent(hex_color)
    except Exception as e:
        print("[!] Failed to set accent via registry directly, trying Powershell fallback.")
        # As a fallback, use powershell to set ColorizationColor
        dword = hex_to_bgr_dword(hex_color)
        ps_cmd = f"Set-ItemProperty -Path HKCU:\\Software\\Microsoft\\Windows\\DWM -Name ColorizationColor -Value {dword}"
        run_powershell(ps_cmd)
        try_refresh_ui()

    print("[*] Updating Windows Terminal (if found)...")
    settings_path = find_windows_terminal_settings()
    if settings_path:
        bak = backup_settings(settings_path)
        print(f"[+] Backed up settings.json to {bak}")
        inject_color_scheme(settings_path, hex_color)
        print("[+] Injected WindowDrip scheme into Terminal settings.")
    else:
        print("[!] Windows Terminal settings.json not found. Skipping terminal update.")

    print("[✓] Done — your system should reflect the new vibe.")

def switch_profile(profile):
    base = os.path.join(os.path.dirname(__file__), "profiles", profile)
    if not os.path.isdir(base):
        print(f"Profile not found: {profile}")
        return
    # Expect wallpaper.jpg in profile directory
    wallpaper = os.path.join(base, "wallpaper.jpg")
    if not os.path.exists(wallpaper):
        print(f"Profile wallpaper not found: {wallpaper}")
        return
    apply_wallpaper(wallpaper)

def list_profiles():
    pdir = os.path.join(os.path.dirname(__file__), "profiles")
    if not os.path.isdir(pdir):
        print("No profiles directory.")
        return
    profiles = [name for name in os.listdir(pdir) if os.path.isdir(os.path.join(pdir, name))]
    print("Available profiles:")
    for p in profiles:
        print(" -", p)

def main():
    parser = argparse.ArgumentParser(prog="WindowDrip")
    sub = parser.add_subparsers(dest="cmd")

    a_apply = sub.add_parser("apply", help="Apply wallpaper image")
    a_apply.add_argument("image", help="Path to wallpaper image")

    a_switch = sub.add_parser("switch", help="Switch to a bundled profile")
    a_switch.add_argument("profile", help="Profile name (in profiles/)")

    a_list = sub.add_parser("list-profiles", help="List bundled profiles")

    args = parser.parse_args()
    if args.cmd == "apply":
        apply_wallpaper(args.image)
    elif args.cmd == "switch":
        switch_profile(args.profile)
    elif args.cmd == "list-profiles":
        list_profiles()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
