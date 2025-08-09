import os
import pytest
from scripts.backup_to_s3 import upload_to_s3

def test_upload_to_s3(monkeypatch):
    class FakeS3:
        def upload_file(self, local_path, bucket, key):
            assert os.path.exists(local_path)
            assert bucket
            assert key

    monkeypatch.setattr("boto3.client", lambda *a, **kw: FakeS3())
    result = upload_to_s3(__file__, "test/key")
    assert result.startswith("s3://")