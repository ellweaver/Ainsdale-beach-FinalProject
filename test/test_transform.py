from src.transform import transform_data
from src.extract import extract_data
import pytest 
import logging 
from moto import mock_aws
from freezegun import freeze_time

class TestTransformData:
    @freeze_time("29-05-2025")
    @pytest.mark.it('Transform data returns correct response')
    def test_transform_response(self,test_s3):
        key = 'data/2025/5/29/2025-05-29_00:00:00/'
        response = transform_data(test_s3, key)
        assert response == {'status': 'Success', 'code': 200, 'key': key}

    @pytest.mark.it('Transform data uploads correctly to S3')
    def test_transform_upload(self,test_s3,test_bucket,test_tf_bucket):
        key = 'data/2025/5/29/2025-05-29_00:00:00/'
        extract_data(s3_client=test_s3, bucket="test_bucket")
        transform_data(test_s3,key,sourcebucket="test_bucket",destinationbucket="test_tf_bucket")
        listing = test_s3.list_objects_v2(Bucket="test_tf_bucket")
        assert listing["Contents"][0]["Key"] =="data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_sales_order.parquet"

    