import pytest
from moto import mock_aws
from utils import upload_file, download_file, currency_code_converter, get_db_secret
import io
import json
from botocore.exceptions import ClientError
import boto3

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

class TestGetDBSecrets:
    @pytest.mark.it("test get db secrets returns correct secret")
    def test_get_db_secrets_returns_secrets(self, upload_secret):
        output = get_db_secret(client=upload_secret)

        assert output == {
            "user": "test_user",
            "password": "test_password",
            "host": "test_host",
            "database": "test_db",
            "port": "0",
        }

    @pytest.mark.it("test get db secrets_ returns error when secret does not exist")
    def test_get_db_secrets_for_error(self, test_secret_manager):

        with pytest.raises(ClientError) as exc:
            get_db_secret(client=test_secret_manager)
        err = exc.value.response["Error"]
        assert err == {
            "Message": "Secrets Manager can't find the specified secret.",
            "Code": "ResourceNotFoundException",
        }

