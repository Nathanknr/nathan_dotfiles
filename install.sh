#!/bin/bash
# Adapated from Evan Chen

set -euo pipefail

do_link() {
  src="$1"
  target="$2"
  BOLD_CYN="\033[1;36m"
  BOLD_GRN="\033[1;32m"
  BOLD_RED="\033[1;31m"
  RESET="\033[0m"
  if [ -L "$target" ] && [ ! -e "$target" ]; then
    echo -e "${BOLD_CYN}UPDATED:${RESET} Fixed broken symlink: $target"
    rm "$target"
    ln -s "$src" "$target"
  elif [ ! -e "$target" ]; then
    echo -e "${BOLD_GRN}CREATED:${RESET} New symlink created:  $target"
    ln -s "$src" "$target"
  elif [ -d "$target" ] && [ ! -L "$target" ] && [ -d "$src" ]; then
    echo -e "${BOLD_RED}WARNING:${RESET} Real directory found: $target"
  fi
}

link_dot_path() {
  mkdir -p "$(dirname "$HOME/.$1")"
  do_link "$HOME/dotfiles/home/$1" "$HOME/.$1"
}

link_hidden_path() {
  mkdir -p "$(dirname "$HOME/.$1")"
  do_link "$HOME/dotfiles/dotconfig/$1" "$HOME/.$1"
}

cd "$HOME" || exit 1

link_dot_path gitconfig 
link_dot_path bashrc
#link_dot_path chktexrc
#link_dot_path eslintrc.yaml
link_dot_path gitconfig
#link_dot_path gvimrc
#link_dot_path latexmkrc
#link_dot_path mbsyncrc
#link_dot_path shellcheckrc
link_dot_path taskrc
#link_dot_path xinitrc
#link_dot_path xprofile

link_dot_path abook
link_dot_path claude/settings.json
link_dot_path jupyter/jupyter_notebook_config.py
link_dot_path vit

#link_hidden_path config/bat
#link_hidden_path config/biome
#link_hidden_path config/borse
#link_hidden_path config/dijo
#link_hidden_path config/dunst
#link_hidden_path config/feh
link_hidden_path config/flameshot
link_hidden_path config/fish
link_hidden_path config/git
link_hidden_path config/i3
#link_hidden_path config/miqin
link_hidden_path config/neomutt
#link_hidden_path config/ncdu
link_hidden_path config/nvim
link_hidden_path config/qutebrowser
link_hidden_path config/redshift
link_hidden_path config/rofi
#link_hidden_path config/ruff
#link_hidden_path config/rumdl
#link_hidden_path config/von
link_hidden_path config/zathura

link_hidden_path config/systemd/user/landlord.service
link_hidden_path config/systemd/user/landlord.timer
link_hidden_path config/systemd/user/mbsync.service
link_hidden_path config/systemd/user/mbsync.timer
link_hidden_path config/systemd/user/back_up.service
link_hidden_path config/systemd/user/back_up.timer
link_hidden_path config/systemd/user/sleep.service
link_hidden_path config/systemd/user/sleep.timer
link_hidden_path config/systemd/user/taskchampion-sync-server.timer
link_hidden_path config/systemd/user/taskchampion-sync-server.service

link_hidden_path texmf
link_dot_path task/hooks
link_hidden_path local/share/gh/extensions
link_hidden_path local/share/typst

# Set default browser to qutebrowser
if [ "$USER" = "nathan" ]; then
  xdg-settings set default-web-browser org.qutebrowser.qutebrowser.desktop
  xdg-settings set default-url-scheme-handler https org.qutebrowser.qutebrowser.desktop
fi
