#!/bin/bash

set -e

# Dump remote database to local file
ssh -C linode mysqldump -ucarlog_django -pcarlog_django --ignore-table=carlog_django.django_session carlog_django > carlog_dump.sql

# Drop all local tables
./dropAllTables.sh carlog_django

# Import the dump file
mysql -ucarlog_django -pcarlog_django carlog_django < carlog_dump.sql

# Clean up
rm carlog_dump.sql

echo "Database sync complete!"
