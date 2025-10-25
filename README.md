# 🌅 Raspberry Pi Auto-Dimmer

> **Automatically dims your official Raspberry Pi touchscreen after periods of inactivity - saving power and extending screen life.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Compatible-red.svg)](https://www.raspberrypi.org/)

## ✨ Features

- 🔆 **Smart brightness control** - Automatically dims screen when idle, restores on activity
- ⚡ **Power efficient** - Reduces power consumption and heat generation
- 🛠️ **Easy configuration** - Simple interactive setup with sensible defaults
- 🚀 **One-line installation** - Get up and running in seconds
- 🔄 **Seamless updates** - Update to latest version with a single command
- 🎯 **Official Pi displays** - Designed for Raspberry Pi 7" touchscreen and compatible displays
- 🔧 **Systemd service** - Runs automatically on boot, managed like any system service

## 🎬 Demo

*Demo video coming soon!*

---

## 🚀 Quick Start

### One-Line Installation

```bash
curl -sSL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/install-remote.sh | bash
```

That's it! The service will be installed and started automatically.

### One-Line Update

```bash
curl -sSL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/update.sh | bash
```

### One-Line Uninstall

```bash
curl -sSL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/uninstall.sh | bash
```

---

## 📋 What Gets Installed

The installer automatically handles:

- **System packages**: `python3`, `python3-pip`, `python3-venv`, `xprintidle`
- **Python dependencies**: [`rpi_backlight`](https://pypi.org/project/rpi-backlight/) for display control
- **Service setup**: Creates and enables systemd service for automatic startup
- **Permissions**: Configures user access to GPIO and backlight controls
- **Configuration**: Sets up sensible defaults (customizable later)

## ⚙️ Configuration

### Default Settings
- **Idle brightness**: 5% (nearly off but visible)
- **Active brightness**: 100% (full brightness)
- **Dim delay**: 30 seconds of inactivity

### Customize Settings
```bash
sudo /opt/rpi-auto-dimmer/config.sh
```

The interactive configuration script will guide you through customizing:
- Brightness levels for idle and active states
- Delay before dimming kicks in
- Update frequency for activity checking

---

## 🛠️ Manual Installation

If you prefer to install manually or want to understand what the installer does:

<details>
<summary>Click to expand manual installation steps</summary>

1. **Install system dependencies**:
   ```bash
   sudo apt update && sudo apt install -y python3 python3-pip python3-venv xprintidle curl
   ```

2. **Download the project**:
   ```bash
   sudo mkdir -p /opt/rpi-auto-dimmer
   sudo chown $USER:$USER /opt/rpi-auto-dimmer
   cd /opt/rpi-auto-dimmer
   
   # Download all files
   curl -sL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/main.py -o main.py
   curl -sL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/requirements.txt -o requirements.txt
   curl -sL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/config.sh -o config.sh
   mkdir -p src
   curl -sL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/src/idle_monitor.py -o src/idle_monitor.py
   curl -sL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/src/screen_control.py -o src/screen_control.py
   curl -sL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/src/helpers.py -o src/helpers.py
   curl -sL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/src/decorator.py -o src/decorator.py
   ```

3. **Set up Python environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure the service**:
   ```bash
   chmod +x config.sh
   ./config.sh
   ```

5. **Set up systemd service**: (See install script for full service configuration)

</details>

---

## 🎮 Service Management

### Basic Commands
```bash
# Check status
sudo systemctl status rpi-auto-dimmer

# Start service
sudo systemctl start rpi-auto-dimmer

# Stop service
sudo systemctl stop rpi-auto-dimmer

# Restart service
sudo systemctl restart rpi-auto-dimmer

# View logs
sudo journalctl -u rpi-auto-dimmer -f
```

### Service Details
- **Service name**: `rpi-auto-dimmer`
- **Installation path**: `/opt/rpi-auto-dimmer/`
- **Configuration file**: `/opt/rpi-auto-dimmer/config.ini`
- **Runs as**: Current user with hardware access permissions
- **Auto-start**: Enabled on boot

---

## 🔧 Dependencies

### System Dependencies
- **[xprintidle](https://packages.debian.org/stable/xprintidle)** - Detects user idle time in X11
  ```bash
  sudo apt install xprintidle
  ```

### Python Dependencies
- **[rpi_backlight](https://github.com/linusg/rpi-backlight)** - Controls Raspberry Pi display backlight
  ```bash
  pip install rpi_backlight
  ```

### Hardware Requirements
- Raspberry Pi (any model with display output)
- Official Raspberry Pi 7" Touchscreen Display (or compatible)
- Raspberry Pi OS with desktop environment

---

## 🐛 Troubleshooting

### Common Issues

**Service won't start?**
```bash
# Check service status
sudo systemctl status rpi-auto-dimmer

# Check logs for errors
sudo journalctl -u rpi-auto-dimmer -n 50
```

**Permission errors?**
```bash
# Ensure user is in correct groups
groups $USER  # Should include 'gpio' and 'video'

# If not, run the installer again
curl -sSL https://raw.githubusercontent.com/mdennis281/rpi-auto-dimmer/refs/heads/main/install-remote.sh | bash
```

**Screen not dimming?**
- Check if `xprintidle` is working: `xprintidle` (should return a number)
- Verify display is supported: Check `/sys/class/backlight/` for available controls
- Review configuration: `/opt/rpi-auto-dimmer/config.ini`

**Still having issues?**
[Open an issue](https://github.com/mdennis281/rpi-auto-dimmer/issues) with:
- Service logs: `sudo journalctl -u rpi-auto-dimmer -n 100`
- System info: `uname -a` and `cat /proc/device-tree/model`

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Thanks to the [rpi_backlight](https://github.com/linusg/rpi-backlight) project for making display control simple
- Built for the awesome Raspberry Pi community 🥧

---

<div align="center">

**[⭐ Star this repo](https://github.com/mdennis281/rpi-auto-dimmer)** if it helped you save power and extend your Pi display's life!

Made with ❤️ for Raspberry Pi enthusiasts

</div>