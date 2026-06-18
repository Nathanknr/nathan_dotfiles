
# Send audio and video to my Ipad 
function sendvid
	set FILE (find . -maxdepth 2 \( -name '*.mp3' -o -name '*.flac' -o -name '*.wav' -o -name '*.ogg' -o -name '*.m4a' -o -name '*.aac' -o -name '*.opus' -o -name '*.mp4' -o -name '*.mkv' -o -name '*.avi' -o -name '*.webm' -o -name '*.mov' -o -name '*.part' \) | fzf)

	if test -z "$FILE"
		return 1
	end

	kdeconnect-cli --device 9162DD724B104D6397E00D29F6E64155 --share "$FILE"

end 
