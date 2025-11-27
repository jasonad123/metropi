#!/bin/bash
set -e

echo "Metro Pi Setup Script"
echo "====================="

# Check if running on Raspberry Pi
if [ ! -f /proc/device-tree/model ] || ! grep -q "Raspberry Pi" /proc/device-tree/model; then
    echo "Warning: This doesn't appear to be a Raspberry Pi"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-dev swig liblgpio-dev

# Check for .env file
if [ ! -f .env ]; then
    echo "Error: .env file not found"
    echo "Please create a .env file with your METRO_API_KEY"
    echo "Example: METRO_API_KEY='your_key_here'"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate and install dependencies
echo "Installing dependencies..."
source venv/bin/activate

# Check if uv is available for faster installs
if command -v uv &> /dev/null; then
    echo "Using uv for faster installation..."
    uv pip install -r requirements.txt
else
    echo "Using pip (install uv with 'curl -LsSf https://astral.sh/uv/install.sh | sh' for faster installs)"
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Install systemd service
echo "Installing systemd service..."
INSTALL_DIR=$(pwd)
sed "s|/home/pi/metropi|$INSTALL_DIR|g" metropi.service > /tmp/metropi.service
sudo cp /tmp/metropi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable metropi.service

echo ""
echo "Setup complete!"
echo ""
echo "Commands:"
echo "  Start service:   sudo systemctl start metropi"
echo "  Stop service:    sudo systemctl stop metropi"
echo "  View logs:       sudo journalctl -u metropi -f"
echo "  Check status:    sudo systemctl status metropi"
echo ""
echo "The service will auto-start on boot."
read -p "Start the service now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo systemctl start metropi
    echo "Service started. Check status with: sudo systemctl status metropi"
fi
