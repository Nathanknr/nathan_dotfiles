#!/usr/bin/bash
# md is probably better and more lightweight but oh boy do i love a  pretty pdf
z pdf
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
