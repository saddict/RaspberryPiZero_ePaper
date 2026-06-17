import sys
import argparse
from pathlib import Path
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont


# Waveshare library path
LIB_DIR = Path.home() / "e-Paper/RaspberryPi_JetsonNano/python/lib"
sys.path.insert(0, str(LIB_DIR))

from waveshare_epd import epd2in13_V4


def get_font(size, bold=False):
    """
    Uses IBM Plex Mono if installed.
    Falls back to DejaVu Sans Mono if IBM Plex Mono is not found.
    """

    if bold:
        candidates = [
            "/usr/share/fonts/truetype/ibm-plex/IBMPlexMono-Bold.ttf",
            "/usr/share/fonts/opentype/ibm-plex/IBMPlexMono-Bold.otf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/ibm-plex/IBMPlexMono-Regular.ttf",
            "/usr/share/fonts/opentype/ibm-plex/IBMPlexMono-Regular.otf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ]

    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass

    return ImageFont.load_default()


def fmt(value, decimals=1):
    """
    Safely formats sensor values that may be floats, strings, None, or 'nan'.
    """

    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return "nan"


def display_hive_data(
    left_temp_f,
    left_humidity,
    left_weight_kg,
    right_temp_f,
    right_humidity,
    right_weight_kg,
    external_temp_f,
    external_humidity,
    timestamp=None,
):
    epd = epd2in13_V4.EPD()
    epd.init()

    # Landscape mode: 250 x 122
    width = epd.height
    height = epd.width

    image = Image.new("1", (width, height), 255)
    draw = ImageDraw.Draw(image)

    font_title = get_font(14, bold=True)
    font = get_font(12)
    font_small = get_font(10)

    mid_x = width // 2
    bottom_y = 94

    timestamp_text = (
        datetime.now().strftime("%m/%d/%y %I:%M %p")
        if timestamp is None
        else str(timestamp)
    )

    # Main separator lines
    draw.line((mid_x, 0, mid_x, bottom_y), fill=0, width=1)
    draw.line((0, 22, width, 22), fill=0, width=1)
    draw.line((0, bottom_y, width, bottom_y), fill=0, width=1)

    # Column headers
    draw.text((35, 3), "LEFT", font=font_title, fill=0)
    draw.text((158, 3), "RIGHT", font=font_title, fill=0)

    # Left hive values
    draw.text((6, 30), f"T: {fmt(left_temp_f)} F", font=font, fill=0)
    draw.text((6, 50), f"H: {fmt(left_humidity)} %", font=font, fill=0)
    draw.text((6, 70), f"W: {fmt(left_weight_kg, 2)} kg", font=font, fill=0)

    # Right hive values
    draw.text((mid_x + 6, 30), f"T: {fmt(right_temp_f)} F", font=font, fill=0)
    draw.text((mid_x + 6, 50), f"H: {fmt(right_humidity)} %", font=font, fill=0)
    draw.text((mid_x + 6, 70), f"W: {fmt(right_weight_kg, 2)} kg", font=font, fill=0)

    # Bottom external row
    draw.text(
        (6, 98),
        f"Ext: {fmt(external_temp_f)} F   {fmt(external_humidity)} %",
        font=font_small,
        fill=0,
    )

    # Timestamp row
    draw.text(
        (6, 110),
        f"Updated: {timestamp_text}",
        font=font_small,
        fill=0,
    )

    epd.display(epd.getbuffer(image))
    epd.sleep()


def display_love_meredith():
    epd = epd2in13_V4.EPD()
    epd.init()

    # Landscape mode: 250 x 122
    width = epd.height
    height = epd.width

    image = Image.new("1", (width, height), 255)
    draw = ImageDraw.Draw(image)

    font_big = get_font(24, bold=True)
    font_mid = get_font(16, bold=True)

    draw.text((54, 18), "I Love", font=font_big, fill=0)
    draw.text((38, 52), "Meredith", font=font_big, fill=0)

    # Draw heart
    x, y = 188, 44
    draw.ellipse((x, y, x + 22, y + 22), fill=0)
    draw.ellipse((x + 18, y, x + 40, y + 22), fill=0)
    draw.polygon(
        [
            (x - 1, y + 13),
            (x + 41, y + 13),
            (x + 20, y + 43),
        ],
        fill=0,
    )

    draw.text((94, 94), "<3", font=font_mid, fill=0)

    epd.display(epd.getbuffer(image))
    epd.sleep()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--display",
        choices=["hive", "love"],
        default="hive",
        help="Choose what to show on the e-paper display.",
    )

    args = parser.parse_args()

    if args.display == "love":
        display_love_meredith()
        return

    display_hive_data(
        left_temp_f=74.2,
        left_humidity=58.0,
        left_weight_kg=55.04,
        right_temp_f=73.8,
        right_humidity=60.5,
        right_weight_kg=54.34,
        external_temp_f=70.1,
        external_humidity=65.2,
    )


if __name__ == "__main__":
    main()
