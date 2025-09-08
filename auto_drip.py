import os
import time
from pathlib import Path
from utils.wallpaper import set_wallpaper, get_dominant_color
from utils.terminal import update_terminal_colors_full, terminal_color_preview
from utils.apps import apply_vscode_template, apply_notepadpp_template

CONFIG_PATH = Path("config.json")

def drip_wallpaper_auto(wallpaper_path, background_mode="black", apps_config=None):
    apps_config = apps_config or {}
    
    # Set wallpaper
    set_wallpaper(wallpaper_path)
    
    # Get dominant color
    dominant_rgb = get_dominant_color(wallpaper_path)
    dominant_hex = '#{:02x}{:02x}{:02x}'.format(*dominant_rgb)
    
    # Terminal colors
    app_colors = {
        "accent": dominant_hex,
        "background": "#000000" if background_mode == "black" else dominant_hex,
        "foreground": "#ffffff"
    }
    try:
        update_terminal_colors_full(app_colors)
        terminal_color_preview(dominant_hex)
        print("[+] Terminal colors updated (WindowDrip scheme applied).")
    except Exception as e:
        print(f"[!] Failed to update terminal colors: {e}")

    # VS Code
    if apps_config.get("vscode", False):
        try:
            apply_vscode_template(app_colors)
            print("[+] VS Code theme updated.")
        except Exception as e:
            print(f"[!] Failed to update VS Code: {e}")
    
    # Notepad++
    if apps_config.get("notepadpp", False):
        try:
            apply_notepadpp_template(app_colors)
            print("[+] Notepad++ theme updated.")
        except Exception as e:
            print(f"[!] Failed to update Notepad++: {e}")

def main():
    import json
    config = json.loads(CONFIG_PATH.read_text())
    wallpaper_folder = Path(config.get("wallpaper_folder", "Wallpapers"))
    interval = config.get("rotation_interval_minutes", 10)
    background_mode = config.get("background_mode", "black")
    apps_config = config.get("apps", {})

    wallpapers = list(wallpaper_folder.glob("*.*"))
    if not wallpapers:
        print("[!] No wallpapers found.")
        return

    print(f"[i] Loaded config from {CONFIG_PATH}")
    print(f"[i] Found {len(wallpapers)} wallpapers. Starting auto-drip loop...")

    idx = 0
    while True:
        wp = wallpapers[idx % len(wallpapers)]
        print(f"\n[*] Applying WindowDrip: {wp}")
        drip_wallpaper_auto(str(wp), background_mode=background_mode, apps_config=apps_config)
        idx += 1
        time.sleep(interval * 60)

if __name__ == "__main__":
    main()
