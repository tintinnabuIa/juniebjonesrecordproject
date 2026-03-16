#!/bin/env bash

get_script_dir()
{
    local SOURCE_PATH="${BASH_SOURCE[0]}"
    local SYMLINK_DIR
    local SCRIPT_DIR
    # Resolve symlinks recursively
    while [ -L "$SOURCE_PATH" ]; do
        # Get symlink directory
        SYMLINK_DIR="$( cd -P "$( dirname "$SOURCE_PATH" )" >/dev/null 2>&1 && pwd )"
        # Resolve symlink target (relative or absolute)
        SOURCE_PATH="$(readlink "$SOURCE_PATH")"
        # Check if candidate path is relative or absolute
        if [[ $SOURCE_PATH != /* ]]; then
            # Candidate path is relative, resolve to full path
            SOURCE_PATH=$SYMLINK_DIR/$SOURCE_PATH
        fi
    done
    # Get final script directory path from fully resolved source path
    SCRIPT_DIR="$(cd -P "$( dirname "$SOURCE_PATH" )" >/dev/null 2>&1 && pwd)"
    echo "$SCRIPT_DIR"
}

script_dir=$(get_script_dir)

echo "Initializing venv..."
python3 -m venv "$script_dir/.venv"
source .venv/bin/activate

echo "Installing npm shopify..."
npm install -g @shopify/cli@latest

echo "Installing pip requirements.txt..."
pip install -r "$script_dir/requirements.txt"

echo "Getting latest dumps..."
./"$script_dir/discogs-xml2db/get_latest_dumps.sh"

echo "Moving to postgresql..."
./"$script_dir/discogs-xml2db/dumps-to-csv-to-psql.sh"

echo "Changing permissions of all files to be yours 700-style..."
sudo chown -R "$(whoami)" "$script_dir"
sudo chmod -R 700 "$script_dir"

echo "Done! You'll probably want to do some \$(shopify auth login) and \$(shopify app init) stuff to initialize this as an app."
