#!/bin/bash

LOG_FILE=~/.anki_debug.log
echo "Starting script..." > "$LOG_FILE"
if ! pgrep -x anki > /dev/null; then
    DISPLAY=:0 i3-msg 'exec anki'
    sleep 2
    i3-msg '[class="Anki"] move to workspace 10'
fi

if [ "$#" -ge 3 ]; then
    deck="$1"
    front="$2"
    back="$3"
elif [ "$#" -eq 1 ]; then
    deck="$1"
    read -p "Front: " front
    read -p "Back: " back
else
    deck="Testing"
    read -p "Front: " front
    read -p "Back: " back
fi

NOTE_TYPE="Basic"

payload=$(jq -n \
  --arg deck "$deck" \
  --arg note "$NOTE_TYPE" \
  --arg front "$front" \
  --arg back "$back" \
  '{
    "action": "addNote",
    "version": 6,
    "params": {
      "note": {
        "deckName": $deck,
        "modelName": $note,
        "fields": {
          "Front": $front,
          "Back": $back
        },
        "tags": []
      }
    }
  }')

response=$(curl -s -X POST -d "$payload" http://localhost:8765)

if echo "$response" | grep -q '"error":null'; then
    echo "Card added successfully!"
else
    echo "Failed: $response"
fi
