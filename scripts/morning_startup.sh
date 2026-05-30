#!/bin/bash

hour=$(date +%H)

if [ "$hour" -ge 6 ] && [ "$hour" -lt 9 ]; then
    # block distractions
    ~/.config/scripts/no_distraction.sh
    # launch anki
    anki &
fi
