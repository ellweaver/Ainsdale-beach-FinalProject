from src.extract import extract_data
from unittest.mock import Mock, patch
import sys
import pytest
import logging
import os
import boto3
from moto import mock_aws
from datetime import datetime
from utils.db_utils import get_secret
from freezegun import freeze_time
from pg8000 import dbapi


class TestExtractData:
    @freeze_time("29-05-2025")
    @pytest.mark.it("extract data returns correct response")
    def test_upload(self, test_s3, dummy_df):
        response = extract_data(test_s3)
        assert response == {'status': 'Success', 'code': 200, 'key': 'data/2025/5/29/2025-05-29_00:00:00/'}

    @freeze_time("29-05-2025")
    @pytest.mark.it("uploads to s3")
    def test_extract_data_uploads_succesfully_to_s3(self, test_s3, test_bucket):
        key = 'data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_address.csv'
        extract_data(test_s3, "test_bucket")

        listing = test_s3.list_objects_v2(Bucket="test_bucket")

        assert len(listing["Contents"]) == 11
        assert listing["Contents"][0]["Key"] == 'data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_address.csv'
        
    @pytest.mark.it("checks uploaded files not empty")
    def test_extract_data_extracts(self, test_s3, test_bucket):
        extract_data(test_s3, "test_bucket")
        listing = test_s3.list_objects_v2(Bucket="test_bucket")
        for item in listing["Contents"]:
            assert item["Size"] != 0

    @pytest.mark.it("handles client errors")
    def test_extract_data_handles_errors(self, test_s3, test_bucket):
        response = extract_data(test_s3, bucket=["fake-bucket","fake-bucket"])
        assert response["status"] == "Failure"
        
       
class TestExtractDataLogging:
    @pytest.mark.it("creates correct logger_used")
    def test_extract_data_uses_correct_logger(self, test_s3, caplog):
        with caplog.at_level(logging.INFO):
            extract_data(test_s3)

        assert "extract" in caplog.text

    @pytest.mark.it("outputs correct info message")
    def test_extract_data_outputs_correct_info_message(self, test_s3, test_bucket, caplog):
        with caplog.at_level(logging.INFO):
            extract_data(test_s3)
        
        assert "File successfully uploaded to ingestion bucket" in caplog.text 

    @pytest.mark.it("test extract data creates correct warning logs")
    def test_extract_data_creates_correct_info_logs(self, test_s3, caplog):
        with caplog.at_level(logging.INFO):
            extract_data(test_s3, bucket=["fake-bucket","fake-bucket"])
        
        assert "expected string or bytes-like object, got 'list'" in caplog.text
