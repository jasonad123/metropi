# metropi

## Overview
This project is used to display the nearest train at a specific metro stop in Washington DC. The project runs on a Raspberry Pi and the display used is the [e-ink bonnet from Adafruit](https://www.adafruit.com/product/4687).

The display shows the following information:
* Destination of the metro - example being "Shady Grove"
* The current time - example being "12:45 PM"
* Which line the train is running on - example being "RD"
* The arrival time of the nearest train - example being "5min"

## Installation

### Quick Setup (Recommended)

1. Create API access token on the [WMATA developer site](https://developer.wmata.com/)
2. Clone the repository on your Raspberry Pi:

   ```bash
   git clone https://github.com/jasonad123/metropi.git
   cd metropi
   ```

3. Create your `.env` file:

   ```bash
   cp .env.example .env
   # Edit .env and add your API key
   ```

4. Run the setup script:

   ```bash
   ./setup.sh
   ```

The script will:

* Create a virtual environment
* Install dependencies
* Configure systemd service for auto-start on boot

### Manual Installation

* Create API access token on the [WMATA developer site](https://developer.wmata.com/)
* Clone the repository: `git clone https://github.com/jasonad123/metropi.git`
* Change into the directory: `cd metropi`
* Install system dependencies: `sudo apt-get update && sudo apt-get install -y python3-dev swig liblgpio-dev fonts-dejavu fonts-liberation`
* Create a virtual environment: `python3 -m venv venv`
* Activate the virtual environment: `source venv/bin/activate`
* Install dependencies: `pip install -r requirements.txt`
* Create `.env` file: `METRO_API_KEY='YOUR_API_KEY'`
* Run manually: `python3 main.py`

### Service Management

Once installed via setup.sh:

```bash
sudo systemctl start metropi    # Start service
sudo systemctl stop metropi     # Stop service
sudo systemctl status metropi   # Check status
sudo journalctl -u metropi -f   # View logs
```

## Configuration

* To change the station being displayed modify `line 53` in [main.py](main.py#L53) with the station code you want to use.
* Station codes can be found in [the following JSON](https://developer.wmata.com/docs/services/5476364f031f590f38092507/operations/5476364f031f5909e4fe3311?) from the WMATA API.

## Testing

### Local Testing (Without Hardware)

Test the API connection and data processing without a Raspberry Pi:

```bash
# Create a virtual environment for testing
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install only the testing dependencies (not the hardware libraries)
pip install -r requirements-dev.txt

# Run the test
python3 test_local.py
```

This will verify your API key and show train data without requiring the e-ink display.

### Testing on Pi Zero 2 W

The code will work on Pi Zero 2 W, but you'll need the Adafruit e-ink bonnet connected. Without the display hardware, you can:

1. Use [test_local.py](test_local.py) to verify API connectivity
2. Test the virtual environment and dependencies installation
3. Verify the systemd service configuration

## Hardware Requirements

* Raspberry Pi (tested on Pi 4 and Pi Zero 2 W)
* [Adafruit 2.13" E-Ink Bonnet](https://www.adafruit.com/product/4687)

![metropi](./images/metropi.png)
