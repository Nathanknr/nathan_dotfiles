function sendpdf
    kdeconnect-cli \
        --device 9162DD724B104D6397E00D29F6E64155 \
        --share (find . -maxdepth 2 -name '*.pdf' | fzf)
end
