import sys
import time
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

LIB_DIR = Path.home() / "e-Paper/RaspberryPi_JetsonNano/python/lib"
sys.path.append(str(LIB_DIR))

from waveshare_epd import epd2in13_V4


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

    try:
        epd.init()
        epd.Clear(0xFF)

        # Landscape mode: 250 x 122
        width = epd.height
        height = epd.width

        image = Image.new("1", (width, height), 255)
        draw = ImageDraw.Draw(image)

        font_title = ImageFont.truetype(
            "/usr/share/fonts/truetype/ibm-plex/IBMPlexMono-Bold.ttf",  14
        )
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/ibm-plex/IBMPlexMono-Regular.ttf",  12
        )
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/ibm-plex/IBMPlexMono-Regular.ttf", 10
        )

        mid_x = width // 2
        bottom_y = 94

        # Use current date/time unless a timestamp is passed in
        if timestamp is None:
            timestamp_text = datetime.now().strftime("%m/%d/%y %I:%M %p")
        else:
            timestamp_text = timestamp

        # Vertical separator between left/right columns
        draw.line((mid_x, 0, mid_x, bottom_y), fill=0, width=1)

        # Bottom separator for external row
        draw.line((0, bottom_y, width, bottom_y), fill=0, width=1)

        # Header row
        draw.text((35, 3), "LEFT", font=font_title, fill=0)
        draw.text((158, 3), "RIGHT", font=font_title, fill=0)
        draw.line((0, 22, width, 22), fill=0, width=1)

        # Left column
        draw.text((6, 30), f"T: {left_temp_f:.1f} F", font=font, fill=0)
        draw.text((6, 50), f"H: {left_humidity:.1f} %", font=font, fill=0)
        draw.text((6, 70), f"W: {left_weight_kg:.2f} kg", font=font, fill=0)

        # Right column
        draw.text((mid_x + 6, 30), f"T: {right_temp_f:.1f} F", font=font, fill=0)
        draw.text((mid_x + 6, 50), f"H: {right_humidity:.1f} %", font=font, fill=0)
        draw.text((mid_x + 6, 70), f"W: {right_weight_kg:.2f} kg", font=font, fill=0)

        # Bottom external row
        draw.text(
            (6, 98),
            f"Ext: {external_temp_f:.1f} F   {external_humidity:.1f} %",
            font=font_small,
            fill=0,
        )

        # Date + time stamp
        draw.text(
            (6, 110),
            f"Updated: {timestamp_text}",
            font=font_small,
            fill=0,
        )

        epd.display(epd.getbuffer(image))
        epd.sleep()

    except KeyboardInterrupt:
        epd.sleep()
        raise


if __name__ == "__main__":
    display_hive_data(
        left_temp_f=74.2,
        left_humidity=58.0,
        left_weight_kg=58.35,

        right_temp_f=73.8,
        right_humidity=60.5,
        right_weight_kg=42.80,

        external_temp_f=70.1,
        external_humidity=65.2,
    )
