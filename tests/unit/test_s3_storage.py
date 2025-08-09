import os
import tempfile
import pytest
from src.storage.s3_storage import S3Storage

# Set these using environment variables or test secrets
BUCKET = os.environ.get("TEST_S3_BUCKET")
REGION = os.environ.get("TEST_S3_REGION")

@pytest.fixture
def s3():
    return S3Storage(BUCKET, REGION)

def test_upload_and_download_file(s3):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"test data")
        local_path = f.name
    s3_key = "test/testfile.txt"

    # Upload
    url = s3.upload_file(local_path, s3_key)
    assert url.endswith(s3_key)
    assert s3.file_exists(s3_key)

    # Download
    download_path = local_path + ".download"
    s3.download_file(s3_key, download_path)
    with open(download_path, "rb") as f:
        data = f.read()
    assert data == b"test data"

    # Cleanup local files
    os.remove(local_path)
    os.remove(download_path)