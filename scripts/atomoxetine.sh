#!/usr/bin/env bash
# Systemd runs headless with no display. Exporting DISPLAY and XAUTHORITY
# passes them down to all child processes including Python and the browser.
#brave-browser &
#export DISPLAY=:0
#export XAUTHORITY=/home/nathan/.Xauthority
#brave-browser &
#sleep 3
cd /home/nathan/.config/scripts
source .venv/bin/activate
python3 atomoxetine.py
