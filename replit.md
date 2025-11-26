# Replit to Raspberry Pi Sync

## Overview
This project contains a sync script that automatically pulls updates from a GitHub repository to a Raspberry Pi every 10 seconds.

## Files
- `sync_to_pi.sh` - Bash script to run on the Raspberry Pi
- `main.py` - Displays setup instructions

## How It Works
1. Connect this Replit project to GitHub
2. Copy `sync_to_pi.sh` to your Raspberry Pi
3. Run the script with your GitHub repo URL
4. The Pi will check for updates every 10 seconds and auto-pull when changes are detected

## Usage on Raspberry Pi
```bash
./sync_to_pi.sh https://github.com/YOUR_USERNAME/YOUR_REPO /home/pi/my-project
```

## Recent Changes
- Nov 26, 2025: Created sync script with 10-second update interval
