# WindowDrip – Auto Wallpaper + Terminal Color Sync for Windows
Description

WindowDrip automatically applies wallpapers and extracts dominant colors to “rice” your Windows experience. It syncs colors with Windows Terminal and can optionally prepare themes for apps (VS Code, Notepad++), though full integration isn’t guaranteed on all systems.

**It’s a proof-of-concept showcasing dynamic color extraction and terminal ricing on Windows—a feat usually reserved for Linux.**

## Features

- ✅ Auto Wallpaper Rotation

Pick wallpapers from a folder.

Automatically rotate every X minutes.

- ✅ Dominant Color Extraction

Extracts the dominant color of the wallpaper using ColorThief.

Converts it into RGB + HEX for easy use.

- ✅ Terminal Ricing (Drip Hard Mode)

Updates Windows Terminal colors to match wallpaper.

Provides ANSI color previews in the terminal.

Optional “full black background” mode (some profiles may ignore).

- ✅ App Integration (Experimental / Optional)

Prepares VS Code and Notepad++ themes based on wallpaper colors.

Gracefully skips apps if not installed.

- Why It’s Cool

Brings Linux-style “ricing” vibes to Windows.

Fully Python-based: cross-machine, easy to run.

Automatic workflow: just drop wallpapers, run the script, and enjoy.

Shows Python use: ColorThief, Windows API, JSON configs, Terminal preview.

## Installation & Usage

Clone the repo:
```
git clone https://github.com/happyman09/WindowDrip.git
cd WindowDrip
```

## Install dependencies:
```
pip install -r requirements.txt
```

## Configure config.json:
```
{
  "wallpaper_folder": "C:/Users/YourName/Pictures/Wallpapers",
  "rotation_interval_minutes": 10,
  "background_mode": "black",
  "apps": {
    "vscode": true,
    "notepadpp": false
  }
}
```

## Run auto-drip:
```
python auto_drip.py
```
## Phase Summary

Phase 1: Basic wallpaper + terminal color sync → ✅ Success
Phase 2: Auto rotation, persistent terminal drip → ✅ Success
Phase 3: App integration (VS Code, Notepad++, Spotify…) → ⚠ Experimental / Not fully supported on Windows


Auto accent mode must be ON in Settings → Personalization → Colors.

Background effects are optional; some profiles may ignore pure black background.
