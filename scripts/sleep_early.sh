#!/usr/bin/env bash
# I will power off my pc every five minutes to remind myself that I shouldn't have the pc turned on at this after 11pm
# hope it stops me from pushing commit to your dotfiles at 1am
#
notify-send "Going down baby " "Shutting off in 10 seconds. No device in your bedtime window" -u critical
sleep 10

systemctl poweroff
