#!/usr/bin/env bash
#export DISPLAY=:0
#export XAUTHORITY=/home/nathan/.Xauthority
# Systemd runs headless with no display. Exporting DISPLAY and XAUTHORITY
# passes them down to all child processes including Python and the browser.
#brave-browser &
#sleep 3
cd /home/nathan/.config/scripts
source .venv/bin/activate
python3 remind_landlord.py
