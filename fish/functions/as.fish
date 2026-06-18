# ~/.config/fish/functions/p.fish

function as 
	cd /home/nathan/.config/scripts/
 	source .venv/bin/activate.fish
	python3 atomoxetine.py status
end
