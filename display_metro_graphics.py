from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from adafruit_epd.epd import Adafruit_EPD

small_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16
)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24
)

# RGB Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Metro_Graphics:
    def __init__(self, display):

        self.small_font = small_font
        self.medium_font = medium_font
        self.large_font = large_font

        self.display = display

        self._metro_icon = None
        self._destination_name = None
        self._location_name = None
        self._arrival_minutes = None
        self._line = None
        self._progress = None
        self._has_arrived = None
        self._refresh_count = 0

    def display_metro(self, metro_status):

        if len(metro_status['Trains']) > 0:
          destination_name = metro_status['Trains'][0]['DestinationName']
          self._destination_name = destination_name

          location_name = metro_status['Trains'][0]['LocationName']
          self._location_name = location_name

          line = metro_status['Trains'][0]['Line']
          self._line = line

          arrival_minutes = metro_status['Trains'][0]['Min']
          if arrival_minutes.isdigit():
              has_arrived = False
              progress = self.display.width / int(arrival_minutes)
              arrival_minutes = arrival_minutes + 'min'
              self._progress = progress
          else:
              has_arrived = True

          self._has_arrived = has_arrived
          self._arrival_minutes = arrival_minutes
        else:
            self._destination_name = 'No Trains'

        self.update_time()
        self.update_display()

    def update_time(self):
        now = datetime.now()
        self._time_text = now.strftime("%I:%M %p").lstrip("0").replace(" 0", " ")

    def update_display(self):
        # Perform a full clear every 10 refreshes to remove ghosting
        self._refresh_count += 1
        if self._refresh_count % 10 == 1:
            self.display.fill(Adafruit_EPD.WHITE)
            self.display.display()

        self.display.fill(Adafruit_EPD.WHITE)
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Draw the destination
        draw.text(
            (5, 10),
            self._destination_name,
            font=self.large_font,
            fill=BLACK,
        )

        # Draw the location
        draw.text(
            (5, 40),
            self._location_name,
            font=self.medium_font,
            fill=BLACK,
        )

        # Draw the time
        draw.text(
            (5, self.display.height - 60),
            self._time_text,
            font=self.medium_font,
            fill=BLACK,
        )

        # Draw the line
        draw.text(
            (5, self.display.height - 35),
            self._line,
            font=self.large_font,
            fill=BLACK,
        )

        # Draw the arrival time
        bbox = draw.textbbox((0, 0), self._arrival_minutes, font=self.large_font)
        font_width = bbox[2] - bbox[0]
        draw.text(
            (
                self.display.width - font_width - 5,
                self.display.height - 35,
            ),
            self._arrival_minutes,
            font=self.large_font,
            fill=BLACK,
        )

        # Draw progress
        if not self._has_arrived:
            box_width = self.display.width / 10
            box_height = self.display.width / 10
            i = 0
            for i in range(10):
                x0 = box_width * i + 1
                y0 = self.display.height - (self.display.height / 4)
                x1 = (box_width * 2) * i
                y1 = (self.display.height - (self.display.height / 4)) + box_height
                # draw.rounded_rectangle([(x0, y0), (x1, y1)], 2, BLACK, BLACK, 30)
            self._progress = self._progress * 2
       
        self.display.image(image)
        self.display.display()
