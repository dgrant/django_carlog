#!/bin/bash

set -e

# Database credentials (defaults for local dev)
DB_USER="${DB_USER:-carlog_django}"
DB_PASSWORD="${DB_PASSWORD:-carlog_django}"
DB_NAME="${DB_NAME:-carlog_django}"

# Check for required script
if [ ! -x ./dropAllTables.sh ]; then
    echo "Error: ./dropAllTables.sh not found or not executable" >&2
    exit 1
fi

# Dump remote database to local file
ssh -C linode mysqldump -u"$DB_USER" -p"$DB_PASSWORD" --ignore-table="$DB_NAME".django_session "$DB_NAME" > carlog_dump.sql

# Drop all local tables
./dropAllTables.sh "$DB_NAME"

# Import the dump file
mysql -u"$DB_USER" -p"$DB_PASSWORD" "$DB_NAME" < carlog_dump.sql

# Clean up
rm carlog_dump.sql

echo "Database sync complete!"
