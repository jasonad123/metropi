from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD

# PIDS-style fonts (Liberation Sans is closer to Helvetica Neue than DejaVu)
try:
    header_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 14)
    train_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", 16)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 12)
    mins_font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", 10)
except OSError:
    # Fallback to DejaVu if Liberation Sans not available
    header_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    train_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
    small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
    mins_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 10)

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
        self._refresh_count += 1
        if self._refresh_count % 60 == 1:
            self.display.fill(Adafruit_EPD.WHITE)
            self.display.display()

        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Get current time
        now = datetime.now()
        time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

        # Header: Station name and time
        y_pos = 2
        station_text = (self._station_name or "")
        draw.text((5, y_pos), station_text, font=header_font, fill=BLACK)

        # Time on right side of header
        bbox = draw.textbbox((0, 0), time_text, font=header_font)
        time_width = bbox[2] - bbox[0]
        draw.text((self.display.width - time_width - 5, y_pos), time_text, font=header_font, fill=BLACK)

        # Separator line between header and departures
        draw.line([(0, 17), (self.display.width, 17)], fill=BLACK, width=1)

        # Column headers (newer PIDS style: Ln | Destination | Car | Arrival)
        y_pos = 20
        draw.text((5, y_pos), "Ln", font=small_font, fill=BLACK)
        draw.text((40, y_pos), "Destination", font=small_font, fill=BLACK)
        draw.text((175, y_pos), "Car", font=small_font, fill=BLACK)
        draw.text((205, y_pos), "Arrival", font=small_font, fill=BLACK)

        # Train rows
        y_pos = 38
        row_height = 20

        for train in self._trains[:4]:
            line = train.get('Line', '--')
            car = train.get('Car', '-')
            destination = train.get('DestinationName', 'Unknown')
            min_val = train.get('Min', '-')

            # Truncate destination if too long (135px available from x=40 to x=175)
            # At 16pt bold, roughly 13 chars max
            if len(destination) > 13:
                destination = destination[:12] + "."

            # Draw train info (Ln, Destination, Car order)
            draw.text((5, y_pos), line, font=train_font, fill=BLACK)
            draw.text((40, y_pos), destination, font=train_font, fill=BLACK)
            draw.text((175, y_pos), str(car), font=train_font, fill=BLACK)

            # Format arrival time (large number + small "min" suffix)
            if min_val not in ['ARR', 'BRD', '-']:
                # Draw number in large font
                draw.text((205, y_pos), min_val, font=train_font, fill=BLACK)
                # Calculate width of number and draw "min" in smaller font
                bbox = draw.textbbox((0, 0), min_val, font=train_font)
                num_width = bbox[2] - bbox[0]
                # Offset "min" slightly down to align baseline better
                draw.text((205 + num_width + 2, y_pos + 4), "min", font=mins_font, fill=BLACK)
            else:
                # ARR/BRD use regular font
                draw.text((205, y_pos), min_val, font=train_font, fill=BLACK)

            y_pos += row_height

        self.display.image(image)
        self.display.display()

class Metro_Graphics_Shift:
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
        self._refresh_count += 1
        if self._refresh_count % 60 == 1:
            self.display.fill(Adafruit_EPD.WHITE)
            self.display.display()

        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Get current time
        now = datetime.now()
        time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

        # Header: Station name and time
        y_pos = 8
        station_text = (self._station_name or "")
        draw.text((5, y_pos), station_text, font=header_font, fill=BLACK)

        # Time on right side of header
        bbox = draw.textbbox((0, 0), time_text, font=header_font)
        time_width = bbox[2] - bbox[0]
        draw.text((self.display.width - time_width - 5, y_pos), time_text, font=header_font, fill=BLACK)

        # Separator line between header and departures
        draw.line([(0, 23), (self.display.width, 23)], fill=BLACK, width=1)

        # Column headers (newer PIDS style: Ln | Destination | Car | Arrival)
        y_pos = 26
        draw.text((5, y_pos), "Ln", font=small_font, fill=BLACK)
        draw.text((40, y_pos), "Destination", font=small_font, fill=BLACK)
        draw.text((175, y_pos), "Car", font=small_font, fill=BLACK)
        draw.text((205, y_pos), "Arrival", font=small_font, fill=BLACK)

        # Train rows
        y_pos = 44
        row_height = 20

        for train in self._trains[:4]:
            line = train.get('Line', '--')
            car = train.get('Car', '-')
            destination = train.get('DestinationName', 'Unknown')
            min_val = train.get('Min', '-')

            # Truncate destination if too long (135px available from x=40 to x=175)
            # At 16pt bold, roughly 13 chars max
            if len(destination) > 13:
                destination = destination[:12] + "."

            # Draw train info (Ln, Destination, Car order)
            draw.text((5, y_pos), line, font=train_font, fill=BLACK)
            draw.text((40, y_pos), destination, font=train_font, fill=BLACK)
            draw.text((175, y_pos), str(car), font=train_font, fill=BLACK)

            # Format arrival time (large number + small "min" suffix)
            if min_val not in ['ARR', 'BRD', '-']:
                # Draw number in large font
                draw.text((205, y_pos), min_val, font=train_font, fill=BLACK)
                # Calculate width of number and draw "min" in smaller font
                bbox = draw.textbbox((0, 0), min_val, font=train_font)
                num_width = bbox[2] - bbox[0]
                # Offset "min" slightly down to align baseline better
                draw.text((205 + num_width + 2, y_pos + 4), "min", font=mins_font, fill=BLACK)
            else:
                # ARR/BRD use regular font
                draw.text((205, y_pos), min_val, font=train_font, fill=BLACK)

            y_pos += row_height

        self.display.image(image)
        self.display.display()

