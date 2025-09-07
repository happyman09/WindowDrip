from colorthief import ColorThief

def get_dominant_color(image_path: str) -> str:
    """Extract dominant color from wallpaper as HEX string."""
    color_thief = ColorThief(image_path)
    dominant = color_thief.get_color(quality=1)
    return "#{:02x}{:02x}{:02x}".format(*dominant)
