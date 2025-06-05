from transform import (
    transform_data,
    make_fact_sales_order,
    make_dim_staff,
    make_dim_location,
    make_dim_currency,
    make_dim_design,
    make_dim_counterparty,
    make_dim_date,
)
from extract import extract_data
import pytest
import logging
from moto import mock_aws
from freezegun import freeze_time
from datetime import date, time


class TestTransformData:
    @freeze_time("29-05-2025")
    @pytest.mark.it("Transform data returns correct response")
    def test_transform_response(self, test_s3, test_bucket, test_tf_bucket):
        key = "data/2025/5/29/2025-05-29_00:00:00/"
        batch_id = "2025-05-29_00:00:00"
        extract_data(s3_client=test_s3, bucket="test_bucket")

        response = transform_data(
            test_s3,
            key,
            batch_id,
            sourcebucket="test_bucket",
            destinationbucket="test_tf_bucket",
        )
        assert response == {
            "status": "Success",
            "code": 200,
            "key": key,
            "batch_id": batch_id,
        }

    @pytest.mark.it("Transform data uploads correctly to S3")
    def test_transform_upload(self, test_s3, test_bucket, test_tf_bucket):
        key = "data/2025/5/29/2025-05-29_00:00:00/"
        batch_id = "2025-05-29_00:00:00"
        extract_data(s3_client=test_s3, bucket="test_bucket")
        transform_data(
            test_s3,
            key,
            batch_id,
            sourcebucket="test_bucket",
            destinationbucket="test_tf_bucket",
        )
        listing = test_s3.list_objects_v2(Bucket="test_tf_bucket")
        assert (
            listing["Contents"][0]["Key"]
            == "data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_sales_order.parquet"
        )


class TestMakeFactSalesOrder:
    @pytest.mark.it("Test make facts sales doesnt manipulate inputs")
    def test_facts_sales_order(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["sales_order"]
        check_df = df.clone()
        make_fact_sales_order(df)

        assert df.equals(check_df)

    @pytest.mark.it("test make_fact_sales_order returns new value")
    def test_new_fact_sales(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["sales_order"]
        fact_sales_order = make_fact_sales_order(df)
        assert df is not fact_sales_order

    @pytest.mark.it("Test make_fact_sales_order returns correct values")
    def test_fact_sales(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        df = extract_df_dummy["sales_order"]
        fact_sales_order = make_fact_sales_order(df)
        row_data = fact_sales_order.row(1)

        assert fact_sales_order.columns == [
            "sales_record_id",
            "sales_order_id",
            "created_date",
            "created_time",
            "last_updated_date",
            "last_updated_time",
            "sales_staff_id",
            "counterparty_id",
            "units_sold",
            "unit_price",
            "currency_id",
            "design_id",
            "agreed_payment_date",
            "agreed_delivery_date",
            "agreed_delivery_location_id",
        ]
        assert row_data == (
            2,
            2,
            date(2024, 2, 2),
            time(0, 0, 0, 0),
            date(2024, 2, 2),
            time(0, 0, 0, 0),
            2,
            2,
            2,
            2,
            2,
            2,
            date(2024, 2, 2),
            date(2024, 2, 2),
            2,
        )


class TestMakeDimDate:
    @pytest.mark.it("Test make_dim_date returns correct values")
    def test_dim_date(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):

        dim_date = make_dim_date()
        row_data = dim_date.row(1)

        assert dim_date.columns == [
            "date_id",
            "year",
            "month",
            "day",
            "day_of_week",
            "day_name",
            "month_name",
            "quarter",
        ]
        assert (date(1960, 1, 2), 1960, 1, 2, 6, "Saturday", "January", 1) == row_data

class TestMakeDimStaff:
    @pytest.mark.it("Test make dim staff doesnt manipulate inputs")
    def test_dim_staff(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        df = extract_df_dummy["staff"]
        df2 = extract_df_dummy["department"]
        check_df = df.clone()
        test_df = df2.clone()
        make_dim_staff(df, df2)

        assert df.equals(check_df)
        assert df2.equals(test_df)

    @pytest.mark.it("test make dim staff returns new value")
    def test_new_dim_staff(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["staff"]
        df2 = extract_df_dummy["department"]
        dim_staff = make_dim_staff(df, df2)
        assert df is not dim_staff
        assert df2 is not dim_staff

    @pytest.mark.it("test make dim staff has correct columns and data")
    def test_correct_columns_and_data(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["staff"]
        df2 = extract_df_dummy["department"]
        dim_staff = make_dim_staff(df, df2)
        row_data = dim_staff.row(1)
        assert dim_staff.columns == [
            "staff_id",
            "first_name",
            "last_name",
            "department_name",
            "location",
            "email_address",
        ]
        assert (2, 2, 2, 2, 2, 2) == row_data


class TestMakeDimLocation:
    @pytest.mark.it("Test make dim location doesnt manipulate inputs")
    def test_dim_location(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        check_df = extract_df_dummy["address"]
        df = check_df.clone()
        make_dim_location(df)

        assert df.equals(check_df)

    @pytest.mark.it("test make dim location returns new value")
    def test_new_dim_location(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["address"]
        dim_location = make_dim_location(df)
        assert df is not dim_location

    @pytest.mark.it("test make dim location has correct columns")
    def test_correct_columns(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["address"]
        dim_location = make_dim_location(df)
        assert dim_location.columns == [
            "location_id",
            "address_line_1",
            "address_line_2",
            "district",
            "city",
            "postal_code",
            "country",
            "phone",
        ]


class TestMakeDimCurrency:
    @pytest.mark.it("Test make dim currency doesnt manipulate inputs")
    def test_dim_currency(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        check_df = extract_df_dummy["currency"]
        df = check_df.clone()
        make_dim_currency(df)
        assert df.equals(check_df)

    @pytest.mark.it("test make dim currency returns new value")
    def test_new_dim_currency(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["currency"]
        dim_currency = make_dim_currency(df)
        assert df is not dim_currency

    @pytest.mark.it("test make dim currency has correct columns")
    def test_correct_columns(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["currency"]
        dim_currency = make_dim_currency(df)
        assert dim_currency.columns == ["currency_id", "currency_code", "currency_name"]

    @pytest.mark.it("test make dim currency has correct data within currency_name")
    def test_correct_data(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        df = extract_df_dummy["currency"]
        dim_currency = make_dim_currency(df)
        data = dim_currency.get_column("currency_name")
        assert "Pound Sterling" in data
        assert "Euro" in data
        assert "Yen" in data
        assert "Yuan Renminbi" in data


class TestMakeDimDesign:
    @pytest.mark.it("Test make dim design doesnt manipulate inputs")
    def test_dim_design(self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy):
        check_df = extract_df_dummy["design"]
        df = check_df.clone()
        make_dim_design(df)
        assert df.equals(check_df)

    @pytest.mark.it("test make dim design returns new value")
    def test_new_dim_design(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["design"]
        dim_design = make_dim_design(df)
        assert df is not dim_design

    @pytest.mark.it("test make dim design has correct columns")
    def test_correct_columns(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["design"]
        dim_design = make_dim_design(df)
        assert dim_design.columns == [
            "design_id",
            "design_name",
            "file_location",
            "file_name",
        ]


class TestMakeDimCounterparty:
    @pytest.mark.it("Test make dim counterparty doesnt manipulate inputs")
    def test_dim_counterparty(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        check_df = extract_df_dummy["counterparty"]
        test_df = extract_df_dummy["address"]
        df = check_df.clone()
        df2 = test_df.clone()
        make_dim_counterparty(df, df2)

        assert df.equals(check_df)
        assert df2.equals(test_df)

    @pytest.mark.it("test make dim counterparty returns new value")
    def test_new_dim_counterparty(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["counterparty"]
        df2 = extract_df_dummy["address"]
        dim_counterparty = make_dim_counterparty(df, df2)
        assert df is not dim_counterparty
        assert df2 is not dim_counterparty

    @pytest.mark.it("test make dim counterparty returns correct content")
    def test_dim_counterparty_content(
        self, test_s3, test_bucket, test_tf_bucket, extract_df_dummy
    ):
        df = extract_df_dummy["counterparty"]
        df2 = extract_df_dummy["address"]
        dim_counterparty = make_dim_counterparty(df, df2)
        row_data = dim_counterparty.row(1)
        assert dim_counterparty.columns == [
            "counterparty_id",
            "counterparty_legal_name",
            "counterparty_legal_address_line_1",
            "counterparty_legal_address_line_2",
            "counterparty_legal_district",
            "counterparty_legal_city",
            "counterparty_legal_postal_code",
            "counterparty_legal_country",
            "counterparty_legal_phone_number",
        ]
        assert row_data == (2, 2, 2, 2, 2, 2, 2, 2, 2)
