import requests
import os
import digitalio
import busio
import board
import time
import logging
import signal
import sys
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from dotenv import load_dotenv
from display_metro_graphics import Metro_Graphics

## Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

## Load the env variable
load_dotenv()

## Signal handler for graceful shutdown
def signal_handler(_sig, _frame):
    logger.info("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

## Validate API key exists
api_key = os.getenv('METRO_API_KEY')
if not api_key:
    raise ValueError("METRO_API_KEY not found in environment variables. Please check your .env file.")

logger.info("Starting Metro Pi Display Service")

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs = digitalio.DigitalInOut(board.CE0)
dc = digitalio.DigitalInOut(board.D22)
rst = digitalio.DigitalInOut(board.D27)
busy = digitalio.DigitalInOut(board.D17)
up_button = digitalio.DigitalInOut(board.D5)
up_button.switch_to_input()
down_button = digitalio.DigitalInOut(board.D6)
down_button.switch_to_input()

DEBOUNCE_DELAY = 0.3

## Station code can be set to 'All' to get all the stations or
## a specific station code such as B03
station_code = ['A03']
station_code_index = 0
api_url = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{}'.format(station_code[station_code_index])

request_headers = {'api_key': api_key}

display = Adafruit_SSD1680(   # newer eInk bonnet
    122, 250, spi, cs_pin=cs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)

display.rotation = 1
gfx = Metro_Graphics(display)
refresh_display = None

while True:
    if (not refresh_display) or (time.monotonic() - refresh_display) > 60:
        try:
            response = requests.get(api_url, headers=request_headers, timeout=10)
            response.raise_for_status()
            request = response.json()
            gfx.display_metro(request)
            refresh_display = time.monotonic()
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            time.sleep(5)
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing API response: {e}")
            time.sleep(5)

    if up_button.value != down_button.value:
        if not up_button.value and station_code_index < len(station_code) - 1:
            station_code_index += 1
        elif not down_button.value and station_code_index > 0:
            station_code_index -= 1
        time.sleep(DEBOUNCE_DELAY)

        api_url = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{}'.format(station_code[station_code_index])
        try:
            response = requests.get(api_url, headers=request_headers, timeout=10)
            response.raise_for_status()
            request = response.json()
            gfx.display_metro(request)
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
        except (KeyError, ValueError) as e:
            logger.error(f"Error parsing API response: {e}")

    gfx.update_time()
