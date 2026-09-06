#!/usr/bin/env bash
notify-send "i3: power mode" -i system-shutdown \
  -t 6000 \
  -u low \
  "<b>e</b>: exit i3
<b>s</b>: suspend
<b>p</b>: poweroff
<b>r</b>: reboot
<b>Escape</b>: cancel"
