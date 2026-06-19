#!/usr/bin/bash

pluck del allow everything
pluck delay 28000
#pluck + when 0-9 block everything
pluck + when 0-9 block port:443
pluck + import:9623d022-89f3-4914-a436-5a834261f172


pluck + allow	host:github.com
pluck + allow	port:443
pluck + allow	program:.local/share/applications/
pluck + allow	program:/home/nathan/.cargo/bin/cargo
pluck + allow	program:/usr/bin
pluck + allow	program:/usr/bin/git
pluck + allow	program:/usr/bin/lutris	host:google.com	mediaType:application/
pluck + allow	program:/usr/bin/python3.13
pluck + allow	program:/usr/bin/steam
pluck + allow	program:cargo
pluck + allow	program:python3.13
pluck + allow	program:todoist
pluck + block	everything:true	when:0-7,2130-24
pluck + block	host:bsky.app
pluck + block	host:facebook.com
pluck + block	host:flickystream.ru
pluck + block	host:instagram.com
pluck + block	host:reddit.com
pluck + block	host:tiktok.com
pluck + block	host:x.com
pluck + block	host:youtube.com
pluck + block	program:/ net.ankiweb.Anki/ org.sqlitebrowser.sqlitebrowser/ re.sonny.Eloquent/
pluck + block	program:/home/nathan/.local/bin/zen
pluck + block	program:/home/nathan/.local/share/flatpak/
pluck + block	program:/home/nathan/.local/share/flatpak/app/org.torproject.torbrowser-launcher
pluck + block	program:/home/nathan/.local/share/flatpak/exports/bin
pluck + block	program:/home/nathan/.nix-profile/bin
pluck + block	program:/home/nathan/.nix-profile/bin/tor-browser
pluck + block	program:/home/nathan/.var/app/org.torproject.torbrowser-launcher
pluck + block	program:/home/nathan/local/share/flatpak
pluck + block	program:/nix/store/
pluck + block	program:/nix/var/nix/profiles/default/bin/nix
pluck + block	program:/nix/var/nix/profiles/default/bin/nix-env
pluck + block	program:/usr/bin/chromium
pluck + block	program:/usr/bin/python3.13
pluck + block	program:/usr/bin/qutebrowser
pluck + block	program:/var/lib/flatpak/app/org.torproject.torbrowser-launcher/
pluck + block	program:chrome
pluck + block	program:chromium
pluck + block	program:firefox
pluck + block	program:nix
pluck + block	program:qbittorrent
pluck + block	program:qutebrowser
pluck + block	program:tor
pluck + block	program:tor-browser
pluck + block	program:~/.local/share/flatpak/app/org.torproject.torbrowser-launcher/
pluck + nofirefox
pluck + okedge
pluck + safe
pluck + block program:/usr/bin/python3.14
pluck + block program:python3.14 
pluck + safeplease
pluck + system
pluck + system                # enable the system feature (aka level 2)

cd /run/media/nathan/Ventoy
rm *.iso
