#!/bin/bash
DATE=$(date +%Y%m%d%H%M)
PG_DB="whirly"
PG_USER="whirly"
PG_HOST="localhost"
BACKUP_DIR="/backups"
mkdir -p $BACKUP_DIR
pg_dump -U $PG_USER -h $PG_HOST $PG_DB > $BACKUP_DIR/whirly_db_$DATE.sql
tar czf $BACKUP_DIR/whirly_files_$DATE.tar.gz /path/to/document/storage