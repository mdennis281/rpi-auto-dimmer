#!/bin/bash

# Raspberry Pi Auto-Dimmer Configuration Script
# This script creates a configuration file for the auto-dimmer service

CONFIG_FILE="config.ini"

# Display header
echo "========================================================================"
echo "             RASPBERRY PI AUTO-DIMMER CONFIGURATION"
echo "========================================================================"
echo ""
echo "This script will guide you through configuring your auto-dimmer settings."
echo "Press Enter to accept default values shown in brackets [like this]."
echo ""

# Get current values or defaults
IDLE_BRIGHTNESS_DEFAULT=5
ACTIVE_BRIGHTNESS_DEFAULT=100
DIM_DELAY_SECONDS_DEFAULT=10

# If config file exists, read current values
if [ -f "$CONFIG_FILE" ]; then
    echo ">>> Existing configuration found - current values will be shown as defaults"
    echo ""
    
    # Extract current values
    CURRENT_IDLE=$(grep "idle_brightness" "$CONFIG_FILE" 2>/dev/null | cut -d'=' -f2 | tr -d ' ')
    CURRENT_ACTIVE=$(grep "active_brightness" "$CONFIG_FILE" 2>/dev/null | cut -d'=' -f2 | tr -d ' ')
    CURRENT_DELAY=$(grep "dim_delay_seconds" "$CONFIG_FILE" 2>/dev/null | cut -d'=' -f2 | tr -d ' ')
    
    # Use current values as defaults if they exist
    [ ! -z "$CURRENT_IDLE" ] && IDLE_BRIGHTNESS_DEFAULT=$CURRENT_IDLE
    [ ! -z "$CURRENT_ACTIVE" ] && ACTIVE_BRIGHTNESS_DEFAULT=$CURRENT_ACTIVE
    [ ! -z "$CURRENT_DELAY" ] && DIM_DELAY_SECONDS_DEFAULT=$CURRENT_DELAY
else
    echo ">>> Creating new configuration file with default settings"
    echo ""
fi

# Prompt for configuration values with visual separators
echo "------------------------------------------------------------------------"
echo "STEP 1: IDLE BRIGHTNESS SETTING"
echo "------------------------------------------------------------------------"
echo "When your system is idle, how bright should the screen be?"
echo "  • 0 = Screen completely off"
echo "  • 50 = Half brightness" 
echo "  • 100 = Full brightness"
echo ""
echo -n "Enter idle brightness (0-100) [$IDLE_BRIGHTNESS_DEFAULT]: "
read -r IDLE_BRIGHTNESS
IDLE_BRIGHTNESS=${IDLE_BRIGHTNESS:-$IDLE_BRIGHTNESS_DEFAULT}
echo ""

echo "------------------------------------------------------------------------"
echo "STEP 2: ACTIVE BRIGHTNESS SETTING"
echo "------------------------------------------------------------------------"
echo "When your system is active, how bright should the screen be?"
echo "  • Typically you want this at 100 for full visibility"
echo "  • Lower values save power but reduce visibility"
echo ""
echo -n "Enter active brightness (0-100) [$ACTIVE_BRIGHTNESS_DEFAULT]: "
read -r ACTIVE_BRIGHTNESS
ACTIVE_BRIGHTNESS=${ACTIVE_BRIGHTNESS:-$ACTIVE_BRIGHTNESS_DEFAULT}
echo ""

echo "------------------------------------------------------------------------"
echo "STEP 3: DIMMING DELAY SETTING"
echo "------------------------------------------------------------------------"
echo "How long should the system wait before dimming the screen?"
echo "  • Shorter delays save more power but may be annoying"
echo "  • Longer delays are less intrusive but save less power"
echo ""
echo -n "Enter delay before dimming in seconds [$DIM_DELAY_SECONDS_DEFAULT]: "
read -r DIM_DELAY_SECONDS
DIM_DELAY_SECONDS=${DIM_DELAY_SECONDS:-$DIM_DELAY_SECONDS_DEFAULT}
echo ""

# Validate inputs
if ! [[ "$IDLE_BRIGHTNESS" =~ ^[0-9]+$ ]] || [ "$IDLE_BRIGHTNESS" -lt 0 ] || [ "$IDLE_BRIGHTNESS" -gt 100 ]; then
    echo "Error: Idle brightness must be a number between 0 and 100"
    exit 1
fi

if ! [[ "$ACTIVE_BRIGHTNESS" =~ ^[0-9]+$ ]] || [ "$ACTIVE_BRIGHTNESS" -lt 0 ] || [ "$ACTIVE_BRIGHTNESS" -gt 100 ]; then
    echo "Error: Active brightness must be a number between 0 and 100"
    exit 1
fi

if ! [[ "$DIM_DELAY_SECONDS" =~ ^[0-9]+$ ]] || [ "$DIM_DELAY_SECONDS" -lt 1 ]; then
    echo "Error: Delay must be a positive number"
    exit 1
fi

# Create the configuration file
cat > "$CONFIG_FILE" << EOF
[display]
# Screen brightness percentage when system is idle (0-100)
idle_brightness = $IDLE_BRIGHTNESS

# Screen brightness percentage when system is active (0-100)
active_brightness = $ACTIVE_BRIGHTNESS

# Number of seconds to wait before dimming the screen
dim_delay_seconds = $DIM_DELAY_SECONDS

[behavior]
# How often to check idle status (seconds)
check_interval = 0.25
EOF

echo "========================================================================"
echo "                        CONFIGURATION COMPLETE!"
echo "========================================================================"
echo ""
echo "Configuration saved to: $CONFIG_FILE"
echo ""
echo "Your settings:"
echo "  ✓ Idle brightness:    ${IDLE_BRIGHTNESS}%"
echo "  ✓ Active brightness:  ${ACTIVE_BRIGHTNESS}%"
echo "  ✓ Dimming delay:      ${DIM_DELAY_SECONDS} seconds"
echo ""
echo "------------------------------------------------------------------------"
echo "To change these settings later:"
echo "  • Run this script again: ./config.sh"
echo "  • Or edit the file directly: nano $CONFIG_FILE"
echo "  • Remember to restart the service: sudo systemctl restart rpi-auto-dimmer"
echo "========================================================================"