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


@pytest.fixture(scope="function")
def get_real_secret(monkeypatch):
    response=get_secret()
    monkeypatch.setattr(get_secret,response)

class TestExtractData:
    @freeze_time("29-05-2025")
    @pytest.mark.it('extract data correctly Uploads data to S3')
    def test_upload(self,test_s3,get_real_secret):
        response = extract_data(test_s3)
        assert response == {"status": "Success", "code": 200,"key":"data/current_time"}
        listing = test_s3.list_objects_v2(Bucket="test_bucket")
        assert len(listing["Contents"]) == 11
    
   
    @pytest.mark.it("uploads to s3")
    def test_extract_data_uploads_succesfully_to_s3(self, test_s3, mock_time):
        pass
        # key = "test_file.json"
        # data = [{"a": 1}, {"b": 2}]
        # resp = write_to_s3(s3, data, "test_bucket", key)
        # assert listing["Contents"][0]["Key"] == "test_file.json"
        # assert resp
        # use MockAWS - in new test bucket count file uploads - compare before and after

    @pytest.mark.skip
    @pytest.mark.it("checks uploaded files not empty")
    def test_extract_data_uploads_succesfully_to_s3(self, test_client):
        response = extract_data(test_client) 
        # check size not 0

    @pytest.mark.skip
    @pytest.mark.it("s3 key naming follows datetime_folder/datetime_tablename.parquet")
    def test_extract_data_s3_key_naming_follows_datetime_folder_datetime_tablename(
        self, test_client
    ):
        response = extract_data(test_client)
        # asserts

    @pytest.mark.skip
    @pytest.mark.it("handles client errors")
    def test_extract_data_handles_errors(self, test_client):
        response = extract_data(test_client)
        assert response["result"] == "FAILURE"
        assert response["message"] == "upload failed"
        # pass sad data in to invoke exception code 



class TestExtractDataLogging:
    
    @pytest.mark.skip
    @pytest.mark.it("creates correct logger_used")
    def test_extract_data_uses_correct_logger(self, test_s3, caplog):
        with caplog.at_level(logging.INFO):
            extract_data(test_s3)
            print(caplog)
            print("^^^^", caplog.text)
        assert "extract" in caplog.text

    # change below tests to use caplog
    @pytest.mark.skip
    @pytest.mark.it("creates correct info logs")
    def test_extract_data_creates_info_log(self, test_client, caplog):
        with self.assertLogs() as captured:
            extract_data(test_client)
        self.assertEqual(captured.records[0].levelname, "INFO")

    @pytest.mark.skip
    @pytest.mark.it("outputs correct info message")
    def test_extract_data_outputs_correct_info_message(self, test_client, caplog):
        with self.assertLogs() as captured:
            extract_data(test_client)
        self.assertIn("is this message there>", captured.output[0])

    @pytest.mark.skip
    @pytest.mark.it("outputs correct number of info messages")
    def test_extract_data_outputs_correct_number_of_info_message(self, test_client, caplog):
        with self.assertLogs() as captured:
            extract_data(test_client)
        self.assertEqual(len(captured.records[0]), 1)

    @pytest.mark.skip
    @pytest.mark.it("test extract data creates correct warning logs")
    def test_extract_data_creates_correct_info_logs(self, caplog):
        pass
