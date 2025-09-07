import subprocess

def set_accent_color(hex_color: str):
    """Set Windows accent color via registry."""
    rgb = [int(hex_color[i:i+2], 16) for i in (1, 3, 5)]
    bgr = rgb[::-1]
    dword = bgr[0] | (bgr[1] << 8) | (bgr[2] << 16)

    subprocess.run([
        "powershell", "-Command",
        f"Set-ItemProperty -Path HKCU:\\Software\\Microsoft\\Windows\\DWM -Name ColorizationColor -Value {dword}; "
        "RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters"
    ], shell=True)

    print(f"[+] Accent color set: {hex_color} ({dword})")
