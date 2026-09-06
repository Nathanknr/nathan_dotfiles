# ~/.config/fish/functions/p.fish

function pa
    set open xdg-open
    ag -U -g '.pdf$' \
    | fast-p \
    | fzf --read0 --reverse -e -d (printf '\t') \
        --preview-window down:80% --preview '
            v=$(echo {q} | tr " " "|");
            echo -e {1}"\n"{2} | grep -E "^|$v" -i --color=always;
        ' \
    | cut -z -f 1 -d (printf '\t') | tr -d '\n' | xargs -r --null $open > /dev/null 2> /dev/null
end
