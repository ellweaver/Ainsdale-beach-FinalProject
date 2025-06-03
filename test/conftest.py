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

    test_s3.create_bucket(
        Bucket="test_bucket",
        CreateBucketConfiguration={
            "LocationConstraint": "eu-west-2",
            "Location": {"Type": "AvailabilityZone", "Name": "string"},
        },
    )


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

