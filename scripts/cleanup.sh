#!/bin/bash
# Cleanup Script - Remove temporary files and cache

set -euo pipefail

TEMP_DIR="/tmp/enterprise"
CACHE_DIR="/var/cache/enterprise"
LOG_DIR="/var/log"

echo "Cleaning up temporary files..."

# Remove temporary files
if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
    echo "Removed temporary directory: $TEMP_DIR"
fi

# Clean cache
if [ -d "$CACHE_DIR" ]; then
    find "$CACHE_DIR" -type f -mtime +30 -delete
    echo "Cleaned old cache files"
fi

# Rotate logs
if [ -d "$LOG_DIR" ]; then
    find "$LOG_DIR" -name "enterprise*.log" -mtime +90 -delete
    echo "Rotated old log files"
fi

echo "Cleanup completed"
exit 0
