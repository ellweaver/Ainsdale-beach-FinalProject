import pytest
from moto import mock_aws
from utils.utils import upload_file, download_file


class TestUploadFile:
    
    @pytest.mark.it('upload file returns success on a Success')
    def test_upload_success(self, test_s3, test_bucket):
        file_name="Test_file.txt"
        bucket="test_bucket"
        key = file_name

        response = upload_file(test_s3, file_name, bucket,key)
        assert isinstance(response, dict)
        assert response["code"] == 200
        assert response["status"] =="Success"


    @pytest.mark.it('Upload file returns failure on a Failure')
    def test_upload_failure(self,test_s3,test_bucket):
        file_name="test_file.txt"
        bucket="notarealbucket"
        key=file_name
        response = upload_file(test_s3,file_name,bucket,key)
        assert isinstance(response, dict)
        assert response["status"] == "Failed"
        assert response["code"]=="NoSuchBucket"


