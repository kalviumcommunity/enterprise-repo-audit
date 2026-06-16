#!/bin/bash
# Database Backup Script

set -e

BACKUP_DIR="/var/backups/enterprise"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

echo "Starting database backup..."
mkdir -p "$BACKUP_DIR"

# Create database dump
pg_dump -h localhost -U admin enterprise_db > "/tmp/db_$TIMESTAMP.sql"

# Create archive
tar -czf "$BACKUP_FILE" /tmp/db_$TIMESTAMP.sql

# Cleanup
rm -f "/tmp/db_$TIMESTAMP.sql"

echo "Backup completed: $BACKUP_FILE"
echo "Backup size: $(du -h "$BACKUP_FILE" | cut -f1)"

# Keep only last 7 backups
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +7 -delete

exit 0
