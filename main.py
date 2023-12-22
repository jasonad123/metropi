import requests
import os
import digitalio
import busio
import board
import time
from adafruit_epd.ssd1680 import Adafruit_SSD1680
from dotenv import load_dotenv
from display_metro_graphics import Metro_Graphics

## Load the env variable 
load_dotenv()

spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
ecs = digitalio.DigitalInOut(board.CE0)
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
station_code = ['B35']
station_code_index = 0

api_key = os.getenv('METRO_API_KEY')
api_url = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{}'.format(station_code[station_code_index])

request_headers = {'api_key': api_key}

display = Adafruit_SSD1680(   # newer eInk bonnet
    122, 250, spi, cs_pin=ecs, dc_pin=dc, sramcs_pin=None, rst_pin=rst, busy_pin=busy,
)

display.rotation = 1
gfx = Metro_Graphics(display)
refresh_display = None

while True:
    if (not refresh_display) or (time.monotonic() - refresh_display) > 60:
        request = requests.get(api_url, request_headers).json()
        gfx.display_metro(request)
        refresh_display = time.monotonic()
    
    if up_button.value != down_button.value:
        if not up_button.value and station_code_index < len(station_code) - 1:
            station_code_index += 1
            time.sleep(DEBOUNCE_DELAY)
        else:
            station_code_index = 0
        api_url = 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{}'.format(station_code[station_code_index])
        request_headers = {'api_key': api_key}
        request = requests.get(api_url, request_headers).json()
        gfx.display_metro(request)

    gfx.update_time()
