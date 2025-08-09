import os
from src.storage.s3_storage import S3Storage

def test_backup_restore_e2e():
    s3 = S3Storage(os.environ['TEST_S3_BUCKET'])
    local_path = "/tmp/e2e_test.txt"
    restored_path = "/tmp/e2e_restored.txt"
    content = b"End-to-end test content"
    with open(local_path, "wb") as f:
        f.write(content)
    s3_key = "e2e/testfile.txt"
    s3.upload_file(local_path, s3_key)
    s3.download_file(s3_key, restored_path)
    with open(restored_path, "rb") as f:
        assert f.read() == content
    os.remove(local_path)
    os.remove(restored_path)