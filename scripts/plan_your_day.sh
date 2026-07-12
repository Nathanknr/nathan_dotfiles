#!/usr/bin/bash
# md is probably better and more lightweight but oh boy do i love a  pretty pdf
timew stop
task add "plan your day" | grep -oE '[0-9]+' | xargs task start 
cd /home/nathan/Resources/Notes/pdf
rm plan.tex
touch plan.tex
cat > plan.tex <<EOF
\documentclass[11pt]{scrartcl}
\usepackage[sexy]{evan}
\graphicspath{{~/Dropbox/figures/}}

\author{Nathan Kamgang}
\title{Plan for the Day}
\date{\today}

\begin{document}
\maketitle


\end{document}
EOF

nvim plan.tex
