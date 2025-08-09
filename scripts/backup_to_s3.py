import os
import boto3
import datetime
import subprocess

BUCKET_NAME = os.environ.get("BACKUP_S3_BUCKET")
REGION = os.environ.get("BACKUP_S3_REGION", "us-east-1")
DB_NAME = os.environ.get("BACKUP_DB_NAME", "whirly")
DB_USER = os.environ.get("BACKUP_DB_USER", "whirly")
DB_HOST = os.environ.get("BACKUP_DB_HOST", "localhost")
FILES_DIR = os.environ.get("BACKUP_FILES_DIR", "/path/to/document/storage")

def backup_database():
    ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    db_backup = f"/tmp/{DB_NAME}_backup_{ts}.sql"
    subprocess.run([
        "pg_dump",
        "-U", DB_USER,
        "-h", DB_HOST,
        DB_NAME,
        "-f", db_backup
    ], check=True)
    return db_backup

def backup_files():
    ts = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    files_backup = f"/tmp/whirly_files_{ts}.tar.gz"
    subprocess.run([
        "tar",
        "czf",
        files_backup,
        FILES_DIR
    ], check=True)
    return files_backup

def upload_to_s3(local_path, s3_key):
    s3 = boto3.client("s3", region_name=REGION)
    s3.upload_file(local_path, BUCKET_NAME, s3_key)
    return f"s3://{BUCKET_NAME}/{s3_key}"

def main():
    db_file = backup_database()
    files_archive = backup_files()
    db_s3_key = f"backups/db/{os.path.basename(db_file)}"
    files_s3_key = f"backups/files/{os.path.basename(files_archive)}"
    upload_to_s3(db_file, db_s3_key)
    upload_to_s3(files_archive, files_s3_key)
    os.remove(db_file)
    os.remove(files_archive)
    print("Backup complete and uploaded to S3.")

if __name__ == "__main__":
    main()