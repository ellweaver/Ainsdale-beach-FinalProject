from src.transform import transform_data, make_fact_sales_order
from src.extract import extract_data
import pytest 
import logging 
from moto import mock_aws
from freezegun import freeze_time

class TestTransformData:
    @freeze_time("29-05-2025")
    @pytest.mark.it('Transform data returns correct response')
    def test_transform_response(self, test_s3, test_bucket, test_tf_bucket):
        key = 'data/2025/5/29/2025-05-29_00:00:00/'
        batch_id = '2025-05-29_00:00:00'
        extract_data(s3_client=test_s3, bucket="test_bucket")
        response = transform_data(test_s3, key, batch_id, sourcebucket="test_bucket", destinationbucket="test_tf_bucket")
        assert response == {'status': 'Success', 'code': 200, 'key': key, 'batch_id': batch_id}

    @pytest.mark.skip
    @pytest.mark.it('Transform data uploads correctly to S3')
    def test_transform_upload(self, test_s3, test_bucket, test_tf_bucket):
        key = 'data/2025/5/29/2025-05-29_00:00:00/'
        batch_id = '2025-05-29_00:00:00'
        extract_data(s3_client=test_s3, bucket="test_bucket")
        transform_data(test_s3, key, batch_id, sourcebucket="test_bucket", destinationbucket="test_tf_bucket")
        listing = test_s3.list_objects_v2(Bucket="test_tf_bucket")
        assert listing["Contents"][0]["Key"] == "data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_sales_order.parquet"

class TestMakeFactSalesOrder:
    @pytest.mark.it('Test make facts sales order data isnt corrupted')
    def test_facts_sales_order(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        check_df = extract_df_dummy["sales_order"]
        df = extract_df_dummy["sales_order"]
        make_fact_sales_order(df)

        assert df.equals(check_df)

    # @pytest.mark.it('Test make facts sales order data isnt corrupted')
    # def test_facts_sales_order(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
    #     check_df = extract_df_dummy["sales_order"]
    #     df = extract_df_dummy["sales_order"]
    #     make_fact_sales_order(df)

    #     assert df.equals(check_df)

        