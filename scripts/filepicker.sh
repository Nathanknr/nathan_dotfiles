#!/usr/bin/env bash
# Credit to https://github.com/anufrievroman and their script that this was based upon
# https://github.com/anufrievroman/Neomutt-File-Picker

file_manager_cmd="yazi --chooser-file /dev/stdout" # Use filepath of stdout to print the chosen file

# No unbound variables!!!
set -u

# Logging setup
log_message() {
    if command -v logger >/dev/null 2>&1; then
        logger -t "neomutt-file-selector" "$1"
    fi
}

# Logic starts here
log_message "Starting file selection process using: $file_manager_cmd"

# Capture its standard output into the 'selected_files' variable.
selected_files=$(eval "$file_manager_cmd") # Redirect stderr for true error handling
exit_status=$?

if [ $exit_status -eq 0 ]; then
    # Check if any files were selected!
    if [ -n "$selected_files" ]; then
        log_message "Files selected, processing for NeoMutt"
        # Use echo to pipe the selected file paths (one per line) to awk
        # Double quotes around "$selected_files" are important to preserve newlines
        mutt_commands=$(echo "$selected_files" | awk 'BEGIN {printf "%s", "push "} {printf "<attach-file>\"%s\"<enter>", $0}')

        echo "$mutt_commands"
        log_message "File selection completed successfully. Commands sent to NeoMutt."
        exit 0
    else
        log_message "No files were selected or selection was cancelled."
        exit 0
    fi
else
    log_message "File selection cancelled or failed (Exit status: $exit_status)."
    exit 1 # Signal an error to NeoMutt
fi
