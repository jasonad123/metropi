#!/usr/bin/env python3
"""
Local testing script for metropi without hardware.
Tests API calls and data processing logic.
"""
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

api_key = os.getenv('METRO_API_KEY')
if not api_key:
    print("Error: METRO_API_KEY not found in .env file")
    exit(1)

station_code = 'A03'  # Change this to test different stations
api_url = f'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/{station_code}'
request_headers = {'api_key': api_key}

print(f"Testing Metro API for station: {station_code}")
print(f"Time: {datetime.now().strftime('%I:%M %p').lstrip('0').replace(' 0', ' ')}")
print("-" * 50)

try:
    response = requests.get(api_url, headers=request_headers, timeout=10)
    response.raise_for_status()
    data = response.json()

    if 'Trains' in data and len(data['Trains']) > 0:
        for idx, train in enumerate(data['Trains'][:3]):  # Show first 3 trains
            print(f"\nTrain {idx + 1}:")
            print(f"  Destination: {train.get('DestinationName', 'Unknown')}")
            print(f"  Location: {train.get('LocationName', 'Unknown')}")
            print(f"  Line: {train.get('Line', 'Unknown')}")
            print(f"  Minutes: {train.get('Min', 'Unknown')}")
            print(f"  Car Count: {train.get('Car', 'Unknown')}")
    else:
        print("No trains currently scheduled")

    print("\n" + "-" * 50)
    print("API test successful")

except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except (KeyError, ValueError) as e:
    print(f"Error parsing response: {e}")
