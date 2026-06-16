#!/bin/bash
# Database Migration Script

set -euo pipefail

MIGRATION_DIR="./migrations"
LOG_FILE="/var/log/enterprise-migrations.log"

echo "Starting database migrations..." | tee -a "$LOG_FILE"

if [ ! -d "$MIGRATION_DIR" ]; then
    echo "Migration directory not found: $MIGRATION_DIR" | tee -a "$LOG_FILE"
    exit 1
fi

# Run migrations in order
for migration in $(find "$MIGRATION_DIR" -name "*.sql" | sort); do
    echo "Running migration: $migration" | tee -a "$LOG_FILE"
    psql -h localhost -U admin -d enterprise_db -f "$migration" || {
        echo "Migration failed: $migration" | tee -a "$LOG_FILE"
        exit 1
    }
done

echo "All migrations completed successfully" | tee -a "$LOG_FILE"
exit 0
