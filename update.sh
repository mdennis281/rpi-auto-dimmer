#!/bin/bash

# Raspberry Pi Auto-Dimmer Update Script
# This script updates the rpi-auto-dimmer to the latest version from GitHub

set -e  # Exit on any error

PROJECT_NAME="rpi-auto-dimmer"
SERVICE_NAME="rpi-auto-dimmer"
INSTALL_DIR="/opt/$PROJECT_NAME"
GITHUB_RAW_URL="https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main"

echo "Updating $PROJECT_NAME from GitHub..."

# Check if installation directory exists
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Error: $PROJECT_NAME is not installed. Please run the installer first:"
    echo "curl -sSL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/install-remote.sh | bash"
    exit 1
fi

# Stop the service before updating
echo "Stopping $SERVICE_NAME service..."
sudo systemctl stop "$SERVICE_NAME" || echo "Service was not running"

# Backup current config if it exists
if [ -f "$INSTALL_DIR/config.ini" ]; then
    echo "Backing up current configuration..."
    cp "$INSTALL_DIR/config.ini" "$INSTALL_DIR/config.ini.backup"
fi

# Change to installation directory
cd "$INSTALL_DIR"

# Download updated project files
echo "Downloading updated project files..."

# Download root files
for file in main.py requirements.txt config.sh LICENSE README.md; do
    echo "  Updating $file..."
    curl -sL "$GITHUB_RAW_URL/$file?$(date +%s)" -o "$file" || {
        echo "Warning: Could not download $file"
    }
done

# Download src files
for file in decorator.py helpers.py idle_monitor.py screen_control.py; do
    echo "  Updating src/$file..."
    curl -sL "$GITHUB_RAW_URL/src/$file?$(date +%s)" -o "src/$file" || {
        echo "Warning: Could not download src/$file"
    }
done

# Make config script executable
chmod +x config.sh

# Restore config if it was backed up
if [ -f "$INSTALL_DIR/config.ini.backup" ]; then
    echo "Restoring your configuration..."
    mv "$INSTALL_DIR/config.ini.backup" "$INSTALL_DIR/config.ini"
fi

# Activate virtual environment and update dependencies
echo "Updating Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Restart the service
echo "Starting $SERVICE_NAME service..."
sudo systemctl start "$SERVICE_NAME"

# Check service status
echo "Service status:"
sudo systemctl status "$SERVICE_NAME" --no-pager

echo ""
echo "Update complete!"
echo ""
echo "Service commands:"
echo "  Start:   sudo systemctl start $SERVICE_NAME"
echo "  Stop:    sudo systemctl stop $SERVICE_NAME"
echo "  Restart: sudo systemctl restart $SERVICE_NAME"
echo "  Status:  sudo systemctl status $SERVICE_NAME"
echo "  Logs:    sudo journalctl -u $SERVICE_NAME -f"
echo ""
echo "Check logs with: sudo journalctl -u $SERVICE_NAME -f"