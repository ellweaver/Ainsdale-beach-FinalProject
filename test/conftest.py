import os
import pytest
from moto import mock_aws
import boto3
from pg8000 import dbapi
from dotenv import load_dotenv

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
    def local_db():
        load_dotenv()
        return dbapi.connect(
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            database=os.environ["DB_NAME"],
            host =os.environ["DB_HOST"],
            port=os.environ["DB_PORT"],
            timeout=60
    )

    monkeypatch.setattr("src.extract.connect_to_db", local_db)

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
