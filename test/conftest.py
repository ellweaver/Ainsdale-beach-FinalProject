import os
import pytest
from moto import mock_aws
import boto3
from pg8000 import dbapi
from dotenv import load_dotenv
import polars as pl
import json


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

    monkeypatch.setattr("src.extract.connect_to_db", start_empty_conn)

    monkeypatch.setattr("src.extract.close_db_connection", close_empty_conn)


@pytest.fixture(autouse=True)
def dummy_df(monkeypatch):
    def generate_dummy_df(*args, **kwargs):
        df = pl.DataFrame(
            {
                "user_id": [101, 102, 103, 104, 105],
                "is_premium": [True, False, True, False, True],
                "page_views": [25, 8, 33, 5, 41],
                "click_rate": [0.12, 0.05, 0.20, 0.03, 0.18],
            }
        )
        return df

    monkeypatch.setattr("src.extract.pl.read_database", generate_dummy_df)


@pytest.fixture(scope="function")
def test_s3():
    """creates secretsmanager client for moto"""
    with mock_aws():
        yield boto3.client("s3")


@pytest.fixture(scope="function")
def test_bucket(test_s3):
    """Creates mock_bucket for client"""

    test_s3.create_bucket(Bucket="test_bucket",CreateBucketConfiguration={'LocationConstraint': "eu-west-2",
        'Location': {
            'Type': 'AvailabilityZone',
            'Name': 'string'}
            })

@pytest.fixture(scope='function')
def test_tf_bucket(test_s3):
    """Creates mock_bucket for client"""
    test_s3.create_bucket(Bucket="test_tf_bucket",CreateBucketConfiguration={'LocationConstraint': "eu-west-2",
        'Location': {
            'Type': 'AvailabilityZone',
            'Name': 'string'}
            })

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
                "port": "5432",
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
    "sales_order_id": [1],
    "created_at": [1],
    "last_updated": [1],
    "design_id": [1],
    "staff_id": [1],
    "counterparty_id": [1],
    "units_sold":[1],
    "unit_price": [1],
    "currency_id":[1],
    "agreed_delivery_date": [1],
    "agreed_payment_date": [1],
    "agreed_delivery_location_id": [1]
    })

    ddf = pl.DataFrame(
    {
    "design_id": [1],
    "created_at": [1],
    "last_updated": [1],
    "design_name": [1],
    "file_location": [1],
    "file_name": [1]
    })

    cdf = pl.DataFrame(
       {
    "currency_id": [1],
    "currency_code": [1],
    "created_at":[1],
    "last_updated":[1]
    })

    sdf = pl.DataFrame(
       {
    "staff_id": [1],
    "first_name":[1],
    "last_name":[1],
    "department_id":[1],
    "email_address":[1],
    "created_at":[1],
    "last_updated":[1]
    })

    cpdf = pl.DataFrame(
     {
    "counterparty_id":  [1],
    "counterparty_legal_name":  [1],
    "legal_address_id": [1],
    "commercial_contact": [1],
    "delivery_contact": [1],
    "created_at": [1],
    "last_updated": [1],
    })

    adf = pl.DataFrame(
    {
    " address_id":  [1],
    "address_line_1":  [1],
    "address_line_2": [1],
    "district ": [1],
    "city": [1],
    "postal_code" : [1],
    "country": [1],
    "phone" : [1],
    "created_at" : [1],
    "last_updated" : [1]
    }
    )

    dpdf = pl.DataFrame(
    {
    "department_id" : [1],
    "department_name" : [1],
    "location" : [1],
    "manager": [1], 
    "created_at" : [1],
    "last_updated" : [1]
    })

    pdf = pl.DataFrame(
    {
    "purchase_order_id": [1], 
    "created_at" : [1],
    "last_updated": [1],
    "staff_id" : [1],
    "counterparty_id" : [1],
    "item_code" : [1],
    "item_quantity" : [1],
    "item_unit_price": [1], 
    "currency_id" : [1],
    "agreed_delivery_date" : [1],
    "agreed_payment_date": [1], 
    "agreed_delivery_location_id": [1]
    })

    ptdf= pl.DataFrame(
    {
    "payment_type_id" : [1],
    "payment_type_name" : [1],
    "created_at" : [1],
    "last_updated" : [1]
    })

    pymdf = pl.DataFrame(
    {
    "payment_id" : [1],
    "created_at": [1],
    "last_updated": [1],
    "transaction_id" : [1],
    "counterparty_id" : [1],
    "payment_amount": [1],
    "currency_id" : [1],
    "payment_type_id": [1], 
    "paid": [1], 
    "payment_date" : [1],
    "company_ac_number": [1], 
    "counterparty_ac_number" : [1]
    })

    tdf = pl.DataFrame(
    {
    "transaction_id" : [1],
    "transaction_type": [1], 
    "sales_order_id": [1], 
    "purchase_order_id": [1], 
    "created_at": [1], 
    "last_updated": [1]  
    })

    full_mirror_df = {
        "sales_order": sodf,
        "design": ddf,
        "currency": cdf,
        "staff": sdf,
        "counterparty": cpdf,
        "address": adf,
        "department": dpdf,
        "purchase": pdf,
        "payment_type": ptdf,
        "payment": pymdf,
        "transaction": tdf}

    return full_mirror_df


        

        
