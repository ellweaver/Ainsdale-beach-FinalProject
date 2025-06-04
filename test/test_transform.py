from src.transform import transform_data, make_fact_sales_order, make_dim_staff, make_dim_location, make_dim_currency,make_dim_currency, make_dim_design, make_dim_counterparty 
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
        df = extract_df_dummy["sales_order"]
        check_df= df.clone()
        make_fact_sales_order(df)
       
        assert df.equals(check_df)

# class TestMakeDimDate:
#     @pytest.mark.it('Test make dim date isnt corrupted')
#     def test_dim_date(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
#         check_df = extract_df_dummy["date"]
#         df = extract_df_dummy["date"]
#         make_fact_sales_order(df)

#         assert df.equals(check_df)

class TestMakeDimStaff:
    @pytest.mark.it('Test make dim staff isnt corrupted')
    def test_dim_staff(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        df = extract_df_dummy["staff"]
        df2=extract_df_dummy["department"]
        check_df = df.clone()
        test_df = df2.clone()
        make_dim_staff(df,df2)

        assert df.equals(check_df)
        assert df2.equals(test_df)

class TestMakeDimLocation:
    @pytest.mark.it('Test make dim location isnt corrupted')
    def test_dim_location(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        check_df = extract_df_dummy["address"]
        df = check_df.clone()
        make_dim_location(df)

        assert df.equals(check_df)

class TestMakeDimCurrency:
    @pytest.mark.it('Test make dim currency isnt corrupted')
    def test_dim_currency(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        check_df = extract_df_dummy["currency"]
        df = check_df.clone()
        make_dim_currency(df)

        assert df.equals(check_df)

class TestMakeDimDesign:
    @pytest.mark.it('Test make dim design isnt corrupted')
    def test_dim_design(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        check_df = extract_df_dummy["design"]
        df = check_df.clone()
        make_dim_design(df)

        assert df.equals(check_df)
    
    @pytest.mark.it('test make dim design returns new value')
    def test_new_dim_design(self,test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        df =extract_df_dummy["design"]
        dim_design=make_dim_design(df)
        assert df is not dim_design

    @pytest.mark.it('test make dim design has correct columns')
    def test_correct_columns(self,test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        df =extract_df_dummy["design"]
        dim_design=make_dim_design(df)
        assert dim_design.columns ==["design_id","design_name","file_location","file_name"]

class TestMakeDimCounterparty:
    @pytest.mark.it('Test make dim counterparty isnt corrupted')
    def test_dim_counterparty(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        check_df = extract_df_dummy["counterparty"]
        test_df= extract_df_dummy["address"]
        df = check_df.clone()
        df2= test_df.clone()
        make_dim_counterparty(df,df2)

        assert df.equals(check_df)
        assert df2.equals(test_df)


        