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
    left_weight_lb,
    right_temp_f,
    right_humidity,
    right_weight_lb,
    external_temp_f,
    external_humidity,
    timestamp=None,
):
    import sys
    from pathlib import Path
    from datetime import datetime
    from PIL import Image, ImageDraw, ImageFont

    # Use absolute path so systemd/root/venv does not break it
    sys.path.insert(0, "/home/bee/e-Paper/RaspberryPi_JetsonNano/python/lib")

    from waveshare_epd import epd2in13_V4

    def fmt(value, decimals=1):
        try:
            return f"{float(value):.{decimals}f}"
        except (TypeError, ValueError):
            return "nan"

    epd = epd2in13_V4.EPD()

    epd.init()

    width = epd.height
    height = epd.width

    image = Image.new("1", (width, height), 255)
    draw = ImageDraw.Draw(image)

    font_title = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14
    )
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12
    )
    font_small = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10
    )

    mid_x = width // 2
    bottom_y = 94

    if timestamp is None:
        timestamp_text = datetime.now().strftime("%m/%d/%y %I:%M %p")
    else:
        timestamp_text = str(timestamp)

    # Lines
    draw.line((mid_x, 0, mid_x, bottom_y), fill=0, width=1)
    draw.line((0, 22, width, 22), fill=0, width=1)
    draw.line((0, bottom_y, width, bottom_y), fill=0, width=1)

    # Headers
    draw.text((35, 3), "LEFT", font=font_title, fill=0)
    draw.text((158, 3), "RIGHT", font=font_title, fill=0)

    # Left values
    draw.text((6, 30), f"T: {fmt(left_temp_f)} F", font=font, fill=0)
    draw.text((6, 50), f"H: {fmt(left_humidity)} %", font=font, fill=0)
    draw.text((6, 70), f"W: {fmt(left_weight_lb, 2)} lb", font=font, fill=0)

    # Right values
    draw.text((mid_x + 6, 30), f"T: {fmt(right_temp_f)} F", font=font, fill=0)
    draw.text((mid_x + 6, 50), f"H: {fmt(right_humidity)} %", font=font, fill=0)
    draw.text((mid_x + 6, 70), f"W: {fmt(right_weight_lb, 2)} lb", font=font, fill=0)

    # External row
    draw.text(
        (6, 98),
        f"Ext: {fmt(external_temp_f)} F   {fmt(external_humidity)} %",
        font=font_small,
        fill=0,
    )

    draw.text(
        (6, 110),
        f"Updated: {timestamp_text}",
        font=font_small,
        fill=0,
    )

    epd.display(epd.getbuffer(image))
    epd.sleep()
