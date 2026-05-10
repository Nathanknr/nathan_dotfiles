zoxide init fish | source 
function tt
	taskwarrior-tui --report list
end 

set -gx EDITOR nvim
set -gx VISUAL nvim
# Lazy conda — only loads when you actually type `conda`
function conda
    functions --erase conda
    if test -f "$HOME/anaconda3/etc/fish/conf.d/conda.fish"
        source "$HOME/anaconda3/etc/fish/conf.d/conda.fish"
    else
        eval "$HOME/anaconda3/bin/conda" shell.fish hook $argv | source
    end
    conda $argv
end


set -g fish_key_bindings fish_vi_key_bindings
alias fr='bash ~/.config/scripts/anki_add.sh'
