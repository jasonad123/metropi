from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD

# PIDS-style fonts
header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
train_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Metro_Graphics:
    def __init__(self, display):
        self.display = display
        self._station_name = None
        self._trains = []
        self._refresh_count = 0

    def display_metro(self, metro_status):
        # Store station name and train list
        if len(metro_status['Trains']) > 0:
            self._station_name = metro_status['Trains'][0]['LocationName']
            self._trains = metro_status['Trains'][:4]  # Show up to 4 trains
        else:
            self._station_name = "No Service"
            self._trains = []

        self.update_display()

    def update_time(self):
        pass  # Called from main loop but not needed in PIDS display

    def update_display(self):
        # Perform a full clear every 10 refreshes to remove ghosting
        self._refresh_count += 1
        if self._refresh_count % 10 == 1:
            self.display.fill(Adafruit_EPD.WHITE)
            self.display.display()

        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Get current time
        now = datetime.now()
        time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

        # Header: Station name and time
        y_pos = 5
        station_text = (self._station_name or "").upper()
        draw.text((5, y_pos), station_text, font=header_font, fill=BLACK)

        # Time on right side of header
        bbox = draw.textbbox((0, 0), time_text, font=header_font)
        time_width = bbox[2] - bbox[0]
        draw.text((self.display.width - time_width - 5, y_pos), time_text, font=header_font, fill=BLACK)

        # Column headers
        y_pos = 25
        draw.text((5, y_pos), "LN", font=small_font, fill=BLACK)
        draw.text((30, y_pos), "CAR", font=small_font, fill=BLACK)
        draw.text((60, y_pos), "DESTINATION", font=small_font, fill=BLACK)
        draw.text((self.display.width - 40, y_pos), "MIN", font=small_font, fill=BLACK)

        # Train rows
        y_pos = 45
        row_height = 20

        for train in self._trains[:4]:
            line = train.get('Line', '--')
            car = train.get('Car', '-')
            destination = train.get('DestinationName', 'Unknown')
            min_val = train.get('Min', '-')

            # Truncate destination if too long (approx 13 chars for 16pt font)
            if len(destination) > 13:
                destination = destination[:12] + "."

            # Draw train info
            draw.text((5, y_pos), line, font=train_font, fill=BLACK)
            draw.text((30, y_pos), str(car), font=train_font, fill=BLACK)
            draw.text((60, y_pos), destination, font=train_font, fill=BLACK)

            # Right-align minutes
            bbox = draw.textbbox((0, 0), min_val, font=train_font)
            min_width = bbox[2] - bbox[0]
            draw.text((self.display.width - min_width - 5, y_pos), min_val, font=train_font, fill=BLACK)

            y_pos += row_height

        self.display.image(image)
        self.display.display()
