import os
import pytest
from moto import mock_aws
import boto3
import polars as pl
import json
from datetime import datetime, date


@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(autouse=True)
def database_connect(monkeypatch):
    def start_empty_conn(*args, **kwargs):
        return None

    def close_empty_conn(*args, **kwargs):
        return None

    monkeypatch.setattr("extract.connect_to_db", start_empty_conn)
    monkeypatch.setattr("load.connect_to_db", start_empty_conn)
    monkeypatch.setattr("load.close_db_connection", close_empty_conn)
    monkeypatch.setattr("extract.close_db_connection", close_empty_conn)


# @pytest.fixture(autouse=True)
# def dummy_df(monkeypatch):
#     def generate_dummy_df(*args, **kwargs):
#         df = pl.DataFrame(
#             {
#                 "user_id": [101, 102, 103, 104, 105],
#                 "is_premium": [True, False, True, False, True],
#                 "page_views": [25, 8, 33, 5, 41],
#                 "click_rate": [0.12, 0.05, 0.20, 0.03, 0.18],
#             }
#         )
#         return df

#     monkeypatch.setattr("src.extract.pl.read_database", generate_dummy_df)


@pytest.fixture(scope="function")
def test_s3():
    """creates secretsmanager client for moto"""
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture(scope="function")
def test_bucket(test_s3):
    """Creates mock_bucket for client"""

    test_s3.create_bucket(
        Bucket="test_bucket",
        CreateBucketConfiguration={
            "LocationConstraint": "eu-west-2",
            "Location": {"Type": "AvailabilityZone", "Name": "string"},
        },
    )

@pytest.fixture(scope="function")
def test_tf_bucket(test_s3):
    """Creates mock_bucket for client"""
    test_s3.create_bucket(
        Bucket="test_tf_bucket",
        CreateBucketConfiguration={
            "LocationConstraint": "eu-west-2",
            "Location": {"Type": "AvailabilityZone", "Name": "string"},
        },
    )

    return test_s3
    


@pytest.fixture(scope="function")
def test_secret_manager():
    """creates secretsmanager client for moto"""
    with mock_aws():
        yield boto3.client("secretsmanager", region_name="eu-west-2")


@pytest.fixture(scope="function")
def upload_secret(test_secret_manager):
    """upload secretsmanager client for moto"""
    test_secret_manager.create_secret(
        Name="toteys_db_credentials",
        SecretString=json.dumps(
            {
                "user": "test_user",
                "password": "test_password",
                "host": "test_host",
                "database": "test_db",
                "port": "0",
            }
        ),
    )
    test_secret_manager.create_secret(
        Name="toteys_db_warehouse_credentials",
        SecretString=json.dumps(
            {
                "user": "test_user",
                "password": "test_password",
                "host": "test_host",
                "database": "test_db",
                "port": "0",
            }
        ),
    )

@pytest.fixture(autouse=True)
def extract_df_dummy(*args, **kwargs):
    """
    Generates a dummy df that mirrors the structure of extract df

    returns dict of df's, with table names as keys
    """

    sodf = pl.DataFrame(
        {
            "sales_order_id": [1, 2, 3, 4],
            "created_at": [
                datetime(2024, 1, 1, 0, 0, 0),
                datetime(2024, 2, 2, 0, 0, 0),
                datetime(2024, 3, 3, 0, 0, 0),
                datetime(2024, 4, 4, 0, 0, 0),
            ],
            "last_updated": [
                datetime(2024, 1, 1, 0, 0, 0),
                datetime(2024, 2, 2, 0, 0, 0),
                datetime(2024, 3, 3, 0, 0, 0),
                datetime(2024, 4, 4, 0, 0, 0),
            ],
            "design_id": [1, 2, 3, 4],
            "staff_id": [1, 2, 3, 4],
            "counterparty_id": [1, 2, 3, 4],
            "units_sold": [1, 2, 3, 4],
            "unit_price": [1, 2, 3, 4],
            "currency_id": [1, 2, 3, 4],
            "agreed_delivery_date": [
                date(2024, 1, 1),
                date(2024, 2, 2),
                date(2024, 3, 3),
                date(2024, 4, 4),
            ],
            "agreed_payment_date": [
                date(2024, 1, 1),
                date(2024, 2, 2),
                date(2024, 3, 3),
                date(2024, 4, 4),
            ],
            "agreed_delivery_location_id": [1, 2, 3, 4],
        }
    )

    ddf = pl.DataFrame(
        {
            "design_id": [1],
            "created_at": [1],
            "last_updated": [1],
            "design_name": [1],
            "file_location": [1],
            "file_name": [1],
        }
    )

    cdf = pl.DataFrame(
        {
            "currency_id": [1, 2, 3, 4],
            "currency_code": ["GBP", "JPY", "CNY", "EUR"],
            "created_at": [1, 2, 3, 4],
            "last_updated": [1, 2, 3, 4],
        }
    )

    sdf = pl.DataFrame(
        {
            "staff_id": [1, 2, 3, 4],
            "first_name": [1, 2, 3, 4],
            "last_name": [1, 2, 3, 4],
            "department_id": [1, 2, 3, 4],
            "email_address": [1, 2, 3, 4],
            "created_at": [1, 2, 3, 4],
            "last_updated": [1, 2, 3, 4],
        }
    )

    cpdf = pl.DataFrame(
        {
            "counterparty_id": [1, 2, 3, 4],
            "counterparty_legal_name": [1, 2, 3, 4],
            "legal_address_id": [1, 2, 3, 4],
            "commercial_contact": [1, 2, 3, 4],
            "delivery_contact": [1, 2, 3, 4],
            "created_at": [1, 2, 3, 4],
            "last_updated": [1, 2, 3, 4],
        }
    )

    adf = pl.DataFrame(
        {
            "address_id": [1, 2, 3, 4],
            "address_line_1": [1, 2, 3, 4],
            "address_line_2": [1, 2, 3, 4],
            "district": [1, 2, 3, 4],
            "city": [1, 2, 3, 4],
            "postal_code": [1, 2, 3, 4],
            "country": [1, 2, 3, 4],
            "phone": [1, 2, 3, 4],
            "created_at": [1, 2, 3, 4],
            "last_updated": [1, 2, 3, 4],
        }
    )

    dpdf = pl.DataFrame(
        {
            "department_id": [1, 2, 3, 4],
            "department_name": [1, 2, 3, 4],
            "location": [1, 2, 3, 4],
            "manager": [1, 2, 3, 4],
            "created_at": [1, 2, 3, 4],
            "last_updated": [1, 2, 3, 4],
        }
    )

    pdf = pl.DataFrame(
        {
            "purchase_order_id": [1],
            "created_at": [1],
            "last_updated": [1],
            "staff_id": [1],
            "counterparty_id": [1],
            "item_code": [1],
            "item_quantity": [1],
            "item_unit_price": [1],
            "currency_id": [1],
            "agreed_delivery_date": [1],
            "agreed_payment_date": [1],
            "agreed_delivery_location_id": [1],
        }
    )

    ptdf = pl.DataFrame(
        {
            "payment_type_id": [1],
            "payment_type_name": [1],
            "created_at": [1],
            "last_updated": [1],
        }
    )

    pymdf = pl.DataFrame(
        {
            "payment_id": [1],
            "created_at": [1],
            "last_updated": [1],
            "transaction_id": [1],
            "counterparty_id": [1],
            "payment_amount": [1],
            "currency_id": [1],
            "payment_type_id": [1],
            "paid": [1],
            "payment_date": [1],
            "company_ac_number": [1],
            "counterparty_ac_number": [1]
        }
    )

    tdf = pl.DataFrame(
        {
            "transaction_id": [1],
            "transaction_type": [1],
            "sales_order_id": [1],
            "purchase_order_id": [1],
            "created_at": [1],
            "last_updated": [1]
        }
    )

    full_mirror_df = {
        "sales_order": sodf,
        "design": ddf,
        "currency": cdf,
        "staff": sdf,
        "counterparty": cpdf,
        "address": adf,
        "department": dpdf,
        "purchase_order": pdf,
        "payment_type": ptdf,
        "payment": pymdf,
        "transaction": tdf,
    }

    return full_mirror_df


@pytest.fixture(autouse=True)
def dummy_df(monkeypatch, extract_df_dummy):
    df_list = [
        extract_df_dummy["counterparty"],
        extract_df_dummy["currency"],
        extract_df_dummy["department"],
        extract_df_dummy["design"],
        extract_df_dummy["staff"],
        extract_df_dummy["sales_order"],
        extract_df_dummy["address"],
        extract_df_dummy["payment"],
        extract_df_dummy["purchase_order"],
        extract_df_dummy["payment_type"],
        extract_df_dummy["transaction"],
    ]

    dfs = iter(df_list)

    monkeypatch.setattr("src.extract.pl.read_database", lambda *_: next(dfs))
