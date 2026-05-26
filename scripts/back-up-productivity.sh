#!/usr/bin/env bash

rsync -a /home/nathan/.config/task/.task /home/nathan/Dropbox/backups
rsync -a /home/nathan/.local/share/timewarrior /home/nathan/Dropbox/backups
