import sys
import time
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Waveshare library path
LIB_DIR = Path.home() / "e-Paper/RaspberryPi_JetsonNano/python/lib"
sys.path.append(str(LIB_DIR))

from waveshare_epd import epd2in13_V4


def display_hive_data(temp_f, humidity, weight_lb):
    epd = epd2in13_V4.EPD()

    try:
        epd.init()
        epd.Clear(0xFF)

        # Landscape mode: 250 x 122
        image = Image.new("1", (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        font_big = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18
        )
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15
        )
        font_small = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12
        )

        now = time.strftime("%I:%M %p")

        draw.text((8, 4), "Hive Monitor", font=font_big, fill=0)
        draw.line((8, 28, 242, 28), fill=0)

        draw.text((8, 36), f"Temp:     {temp_f:.1f} F", font=font, fill=0)
        draw.text((8, 58), f"Humidity: {humidity:.1f} %", font=font, fill=0)
        draw.text((8, 80), f"Weight:   {weight_lb:.2f} lb", font=font, fill=0)

        draw.text((8, 106), f"Updated: {now}", font=font_small, fill=0)

        epd.display(epd.getbuffer(image))
        epd.sleep()

    except KeyboardInterrupt:
        epd.sleep()
        raise


if __name__ == "__main__":
    # Replace these with your actual sensor readings
    temperature_f = 74.2
    humidity_percent = 58.0
    weight_pounds = 121.35

    display_hive_data(temperature_f, humidity_percent, weight_pounds)
