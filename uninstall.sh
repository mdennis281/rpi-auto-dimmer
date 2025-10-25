#!/bin/bash

# Raspberry Pi Auto-Dimmer Service Uninstallation Script
# This script removes the rpi-auto-dimmer service and all related files

set -e  # Exit on any error

PROJECT_NAME="rpi-auto-dimmer"
SERVICE_NAME="rpi-auto-dimmer"
INSTALL_DIR="/opt/$PROJECT_NAME"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
UDEV_RULE="/etc/udev/rules.d/99-backlight.rules"
USER=$(whoami)  # Current user for reference

echo "Uninstalling $PROJECT_NAME..."

# Stop and disable the service
echo "Stopping and disabling service..."
if sudo systemctl is-active --quiet "$SERVICE_NAME"; then
    sudo systemctl stop "$SERVICE_NAME"
    echo "   Service stopped"
fi

if sudo systemctl is-enabled --quiet "$SERVICE_NAME" 2>/dev/null; then
    sudo systemctl disable "$SERVICE_NAME"
    echo "   Service disabled"
fi

# Remove the service file
echo "Removing systemd service file..."
if [ -f "$SERVICE_FILE" ]; then
    sudo rm "$SERVICE_FILE"
    echo "   Service file removed: $SERVICE_FILE"
else
    echo "   Service file not found (already removed)"
fi

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload
sudo systemctl reset-failed

# Remove the installation directory
echo "Removing installation directory..."
if [ -d "$INSTALL_DIR" ]; then
    sudo rm -rf "$INSTALL_DIR"
    echo "   Installation directory removed: $INSTALL_DIR"
else
    echo "   Installation directory not found (already removed)"
fi

# Remove udev rule
echo "Removing udev rule..."
if [ -f "$UDEV_RULE" ]; then
    sudo rm "$UDEV_RULE"
    echo "   Udev rule removed: $UDEV_RULE"
    
    # Reload udev rules
    sudo udevadm control --reload-rules
    sudo udevadm trigger
else
    echo "   Udev rule not found (already removed)"
fi

# Note about user groups (we don't remove them as they might be used by other services)
echo "Note: User $USER remains in gpio and video groups"
echo "   These groups may be used by other services"

echo ""
echo "Uninstallation complete!"
echo ""
echo "The following were removed:"
echo "  * Systemd service: $SERVICE_NAME"
echo "  * Installation directory: $INSTALL_DIR"
echo "  * Service file: $SERVICE_FILE"
echo "  * Udev rule: $UDEV_RULE"
echo ""
echo "The following were left intact:"
echo "  * System packages (python3, pip, venv, git, xprintidle)"
echo "  * User group memberships (gpio, video) for user $USER"
echo ""
echo "All traces of $PROJECT_NAME have been removed from your system."