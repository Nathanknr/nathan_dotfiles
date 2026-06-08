#!/usr/bin/env bash
# I will power off my pc every five minutes to remind myself that I shouldn't have the pc turned on at this after 11pm
# hope it stops me from pushing commit to your dotfiles at 1am
#
notify-send "Going down baby " "Shutting off in 10 seconds. You should be asleep nigger" -u critical
sleep 10

systemctl power off
