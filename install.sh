#!/bin/bash

# Raspberry Pi Auto-Dimmer Remote Installation Script
# This script downloads and installs the rpi-auto-dimmer as a systemd service

set -e  # Exit on any error

PROJECT_NAME="rpi-auto-dimmer"
SERVICE_NAME="rpi-auto-dimmer"
INSTALL_DIR="/opt/$PROJECT_NAME"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
USER=$(whoami)  # Use the current user running the script

# Default branch
BRANCH="main"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -b|--branch) BRANCH="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

GITHUB_RAW_URL="https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/$BRANCH"

echo "Installing $PROJECT_NAME from GitHub (branch: $BRANCH)..."

# Update system packages
echo "Updating system packages..."
sudo apt update
sudo apt upgrade -y

# Install required system packages
echo "Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv git curl

# Create installation directory
echo "Creating installation directory..."
sudo mkdir -p "$INSTALL_DIR"
sudo chown $USER:$USER "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download project files
echo "Downloading project files..."
mkdir -p src

# Download root files
for file in main.py requirements.txt config.sh LICENSE README.md; do
    echo "  Downloading $file..."
    curl -sL "$GITHUB_RAW_URL/$file" -o "$file" || {
        echo "Warning: Could not download $file"
    }
done

# Download src files
for file in decorator.py helpers.py idle_monitor.py screen_control.py; do
    echo "  Downloading src/$file..."
    curl -sL "$GITHUB_RAW_URL/src/$file" -o "src/$file" || {
        echo "Warning: Could not download src/$file"
    }
done

# Make config script executable
chmod +x config.sh

# Create and activate virtual environment
echo "Creating Python virtual environment..."
python3 -m venv --system-site-packages venv
source venv/bin/activate

# Upgrade pip and install requirements
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create default configuration
echo "Setting up default configuration..."
cat > config.ini << EOF
[display]
# Screen brightness percentage when system is idle (0-100)
idle_brightness = 5

# Screen brightness percentage when system is active (0-100)
active_brightness = 100

# Number of seconds to wait before dimming the screen
dim_delay_seconds = 30

[behavior]
# How often to check idle status (seconds)
check_interval = 0.25
EOF

echo "Default configuration created:"
echo "  ✓ Idle brightness:    5%"
echo "  ✓ Active brightness:  100%"
echo "  ✓ Dimming delay:      30 seconds"
echo ""
echo "To customize settings later, run: /opt/$PROJECT_NAME/config.sh"

# Set up permissions for backlight access
echo "Setting up permissions for user $USER to access backlight controls and input devices..."
sudo usermod -a -G gpio $USER
sudo usermod -a -G video $USER
sudo usermod -a -G input $USER

# Create udev rule for backlight access
echo "Creating udev rule for backlight access..."
sudo tee /etc/udev/rules.d/99-backlight.rules > /dev/null << EOF
SUBSYSTEM=="backlight", ACTION=="add", RUN+="/bin/chgrp video %S%p/brightness", RUN+="/bin/chmod g+w %S%p/brightness"
SUBSYSTEM=="backlight", ACTION=="add", RUN+="/bin/chgrp video %S%p/bl_power", RUN+="/bin/chmod g+w %S%p/bl_power"
EOF

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "Service will run as user $USER with hardware access permissions..."

# Create systemd service file
echo "Creating systemd service..."
sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=Raspberry Pi Auto Screen Dimmer
After=graphical-session.target
Wants=graphical-session.target

[Service]
Type=simple
User=$USER
Group=$USER
WorkingDirectory=$INSTALL_DIR
Environment=PATH=$INSTALL_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/$USER/.Xauthority
ExecStartPre=/bin/sleep 10
ExecStart=$INSTALL_DIR/venv/bin/python main.py
Restart=on-failure
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
EOF

# Set proper permissions on the service file
sudo chmod 644 "$SERVICE_FILE"

# Reload systemd and enable the service
echo "Enabling and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable "$SERVICE_NAME"
sudo systemctl start "$SERVICE_NAME"

# Check service status
echo "Service status:"
sudo systemctl status "$SERVICE_NAME" --no-pager

echo ""
echo "Installation complete!"
echo ""
echo "To customize settings, run: sudo /opt/$PROJECT_NAME/config.sh"
echo ""
echo "Service commands:"
echo "  Start:   sudo systemctl start $SERVICE_NAME"
echo "  Stop:    sudo systemctl stop $SERVICE_NAME"
echo "  Restart: sudo systemctl restart $SERVICE_NAME"
echo "  Status:  sudo systemctl status $SERVICE_NAME"
echo "  Logs:    sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "The service is now running and will start automatically on boot."
echo "Check logs with: sudo journalctl -u $SERVICE_NAME -f"