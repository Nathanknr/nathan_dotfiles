#!/usr/bin/bash

pluck del allow everything
pluck delay 28000
#pluck + when 0-9 block everything
pluck + when 0-9 block port:443
pluck + import:9623d022-89f3-4914-a436-5a834261f172


action:allow	host:github.com
action:allow	port:443
action:allow	program:.local/share/applications/
action:allow	program:/home/nathan/.cargo/bin/cargo
action:allow	program:/usr/bin
action:allow	program:/usr/bin/git
action:allow	program:/usr/bin/lutris	host:google.com	mediaType:application/
action:allow	program:/usr/bin/python3.13
action:allow	program:/usr/bin/steam
action:allow	program:cargo
action:allow	program:python3.13
action:allow	program:todoist
action:block	everything:true	when:0-7,2130-24
action:block	host:bsky.app
action:block	host:facebook.com
action:block	host:flickystream.ru
action:block	host:instagram.com
action:block	host:reddit.com
action:block	host:tiktok.com
action:block	host:x.com
action:block	host:youtube.com
action:block	program:/ net.ankiweb.Anki/ org.sqlitebrowser.sqlitebrowser/ re.sonny.Eloquent/
action:block	program:/home/nathan/.local/bin/zen
action:block	program:/home/nathan/.local/share/flatpak/
action:block	program:/home/nathan/.local/share/flatpak/app/org.torproject.torbrowser-launcher
action:block	program:/home/nathan/.local/share/flatpak/exports/bin
action:block	program:/home/nathan/.nix-profile/bin
action:block	program:/home/nathan/.nix-profile/bin/tor-browser
action:block	program:/home/nathan/.var/app/org.torproject.torbrowser-launcher
action:block	program:/home/nathan/local/share/flatpak
action:block	program:/nix/store/
action:block	program:/nix/var/nix/profiles/default/bin/nix
action:block	program:/nix/var/nix/profiles/default/bin/nix-env
action:block	program:/usr/bin/chromium
action:block	program:/usr/bin/python3.13
action:block	program:/usr/bin/qutebrowser
action:block	program:/var/lib/flatpak/app/org.torproject.torbrowser-launcher/
action:block	program:chrome
action:block	program:chromium
action:block	program:firefox
action:block	program:nix
action:block	program:qbittorrent
action:block	program:qutebrowser
action:block	program:tor
action:block	program:tor-browser
action:block	program:~/.local/share/flatpak/app/org.torproject.torbrowser-launcher/
feature:nofirefox
feature:okedge
feature:safe
feature:safeplease
feature:system

cd /run/media/nathan/Ventoy
rm *.iso
