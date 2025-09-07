from colorthief import ColorThief

def get_dominant_color(image_path):
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=1)
    return dominant_color  # (R, G, B)

def rgb_to_hex(rgb):
    """Convert (R, G, B) → #RRGGBB"""
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])
