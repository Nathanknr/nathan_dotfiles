function fish_greeting
    set hour (date +%H)

    if test $hour -ge 6 && test $hour -lt 9
        set_color --bold red
        printf "Hello %s\n" $USER
        set_color normal
        set_color --italics
        printf "It's time for your Anki review. Distractions are blocked.\n"
        set_color normal
        ~/.config/scripts/no_distraction.sh
    else
        set_color --italics
        printf "Hello %s! " $USER
        set_color normal
        printf "Type "
        set_color --bold cyan
        printf "help"
        set_color normal
        printf " to see fish's built-in commands.\n"
    end
end
