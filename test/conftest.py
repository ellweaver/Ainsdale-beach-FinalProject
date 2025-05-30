import os
import pytest
from moto import mock_aws
import boto3
from pg8000 import dbapi


@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"

@pytest.fixture(scope="session")
def database_connect(monkeypatch):
    def local_db():
        return dbapi.connect(
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
            host =os.environ["DB_HOST"],
            port=os.environ["DB_PORT"]

        )
    monkeypatch.setatrr("connect_to_db", local_db)

@pytest.fixture(scope="function")
def test_s3():
    """creates secretsmanager client for moto"""
    with mock_aws():
         yield boto3.client("s3")

@pytest.fixture(scope='function')
def test_bucket(test_s3):
    """Creates mock_bucket for client"""
    test_s3.create_bucket(Bucket="test_bucket",CreateBucketConfiguration={'LocationConstraint': "eu-west-2",
        'Location': {
            'Type': 'AvailabilityZone',
            'Name': 'string'}
            })