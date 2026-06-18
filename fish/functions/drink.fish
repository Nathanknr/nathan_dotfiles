# ~/.config/fish/functions/p.fish

function drink 
	cd /home/nathan/.config/scripts/
 	source .venv/bin/activate.fish
	python3 atomoxetine.py 
end
