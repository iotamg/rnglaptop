#!/bin/bash

REPO_URL="${1:-}"
TARGET_DIR="${2:-./replit-project}"

if [ -z "$REPO_URL" ]; then
    echo "Usage: ./sync_to_pi.sh <github-repo-url> [target-directory]"
    echo "Example: ./sync_to_pi.sh https://github.com/username/my-replit-project /home/pi/my-project"
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Cloning repository for the first time..."
    git clone "$REPO_URL" "$TARGET_DIR"
    cd "$TARGET_DIR"
else
    cd "$TARGET_DIR"
fi

echo "Starting sync loop - checking for updates every 10 seconds"
echo "Press Ctrl+C to stop"
echo "----------------------------------------"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    
    git fetch origin 2>/dev/null
    
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse @{u} 2>/dev/null)
    
    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "[$TIMESTAMP] New changes detected! Pulling updates..."
        git pull origin main 2>/dev/null || git pull origin master 2>/dev/null
        echo "[$TIMESTAMP] Updated successfully!"
    else
        echo "[$TIMESTAMP] No changes"
    fi
    
    sleep 10
done
