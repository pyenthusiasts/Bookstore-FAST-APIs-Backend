#!/bin/bash
# Database backup script for PostgreSQL

set -e

# Configuration
BACKUP_DIR="${BACKUP_DIR:-/backups}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-bookstore}"
DB_USER="${DB_USER:-bookstore}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/bookstore_${TIMESTAMP}.sql.gz"

echo "Starting database backup..."
echo "Database: $DB_NAME"
echo "Host: $DB_HOST:$DB_PORT"
echo "Backup file: $BACKUP_FILE"

# Perform backup
PGPASSWORD="$DB_PASSWORD" pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --format=plain \
    --no-owner \
    --no-privileges \
    | gzip > "$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "Backup completed successfully!"
    echo "Backup size: $(du -h $BACKUP_FILE | cut -f1)"

    # Remove old backups
    echo "Removing backups older than $RETENTION_DAYS days..."
    find "$BACKUP_DIR" -name "bookstore_*.sql.gz" -mtime +$RETENTION_DAYS -delete

    echo "Backup cleanup completed."
else
    echo "Backup failed!"
    exit 1
fi
