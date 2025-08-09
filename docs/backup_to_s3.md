# Automated Backups to S3

## Overview

`scripts/backup_to_s3.py` provides automated database and file storage backups, uploading archives to S3.

## Usage

Set environment variables for bucket, DB credentials, and file directory, then run:

```bash
python scripts/backup_to_s3.py
```

## Environment Variables

- `BACKUP_S3_BUCKET`
- `BACKUP_S3_REGION`
- `BACKUP_DB_NAME`
- `BACKUP_DB_USER`
- `BACKUP_DB_HOST`
- `BACKUP_FILES_DIR`

## Testing

See `tests/unit/test_backup_to_s3.py` for upload logic unit test.

## Notes

- Ensure AWS credentials/IAM role are present.
- Clean up local temp files after backup.
- Enable S3 versioning for backup safety.