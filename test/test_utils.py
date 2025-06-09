import pytest
from moto import mock_aws
from src.utils import upload_file, download_file, currency_code_converter
import io


class TestUploadFile:
    @pytest.mark.it("upload file returns success on a Success")
    def test_upload_success(self, test_s3, test_bucket):
        file_name = "Test_file.txt"
        bucket = "test_bucket"
        key = file_name

        response = upload_file(test_s3, file_name, bucket, key)
        assert isinstance(response, dict)
        assert response["code"] == 200
        assert response["status"] == "Success"

    @pytest.mark.it("Upload file returns failure on a Failure")
    def test_upload_failure(self, test_s3, test_bucket):
        file_name = "test_file.txt"
        bucket = "notarealbucket"
        key = file_name
        response = upload_file(test_s3, file_name, bucket, key)
        assert isinstance(response, dict)
        assert response["status"] == "Failed"
        assert response["code"] == "NoSuchBucket"


class TestDownloadFile:
    @pytest.mark.it("Download file returns Success on a Successful download")
    def test_download_success(self, test_s3, test_bucket):
        file_name = "Test_file.txt"
        bucket = "test_bucket"
        key = file_name
        upload_file(test_s3, file_name, bucket, key)
        response = download_file(test_s3, bucket, key)
        assert isinstance(response, dict)
        assert response["code"] == 200
        assert response["status"] == "Success"
        fileobj = io.BytesIO(response["body"].read())
        assert b"Test_file.txt" == fileobj.read()

    @pytest.mark.it("Download file returns Failure on failed download")
    def test_snake_case_name(self, test_s3, test_bucket):
        file_name = "test_file.txt"
        bucket = "test_bucket"
        key = file_name
        response = download_file(test_s3, bucket, key)
        assert isinstance(response, dict)
        assert response["status"] == "Failed"
        assert response["code"] == "NoSuchKey"

    class TestCurrencyCodeConverter:
        @pytest.mark.it("test currency converter converts usd correctly")
        def test_currency_converter_converts_usd(self):
            assert currency_code_converter("usd") == "US Dollar"

        @pytest.mark.it(
            "test currency converter returns correct response to unavailable currency"
        )
        def test_currency_converter_returns_correct_response(self):
            assert currency_code_converter("waffles") == "currency not available"
