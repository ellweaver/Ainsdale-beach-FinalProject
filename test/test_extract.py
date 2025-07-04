from extract import extract_data, lambda_handler
from unittest.mock import Mock, patch
import pytest
import logging
from datetime import datetime
from freezegun import freeze_time




class TestExtractData:
    @freeze_time("29-05-2025")
    @pytest.mark.it("extract data returns correct response")
    def test_upload(self, test_s3, test_df_read_db):
        response = extract_data(test_s3)
        assert response == {
            "status": "Success",
            "code": 200,
            "key": "data/2025/5/29/2025-05-29_00:00:00/",
            "batch_id": "2025-05-29_00:00:00",
        }

    
    @freeze_time("29-05-2025")
    @pytest.mark.it("uploads to s3")
    def test_extract_data_uploads_succesfully_to_s3(self, test_s3, test_bucket,test_df_read_db):
        key = "data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_address.csv"
        extract_data(test_s3, "test_bucket")

        listing = test_s3.list_objects_v2(Bucket="test_bucket")

        assert len(listing["Contents"]) == 11
        assert (
            listing["Contents"][0]["Key"]
            == "data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_address.csv"
        )
    
    @pytest.mark.it("checks uploaded files not empty")
    def test_extract_data_extracts(self, test_s3, test_bucket, test_df_read_db):
        extract_data(test_s3, "test_bucket")
        listing = test_s3.list_objects_v2(Bucket="test_bucket")
        for item in listing["Contents"]:
            assert item["Size"] != 0
      
    @pytest.mark.it("handles client errors")
    def test_extract_data_handles_errors(self, test_s3, test_bucket, test_df_read_db):
        response = extract_data(test_s3, bucket=["fake-bucket", "fake-bucket"])
        assert response["status"] == "Failure"


class TestExtractDataLogging:
    @pytest.mark.it("creates correct logger_used")
    def test_extract_data_uses_correct_logger(self, test_s3, caplog, test_df_read_db):
        with caplog.at_level(logging.INFO):
            extract_data(test_s3)

        assert "extract" in caplog.text
  
    @pytest.mark.it("outputs correct info message")
    def test_extract_data_outputs_correct_info_message(
        self, test_s3, test_bucket, caplog
    , test_df_read_db):
        with caplog.at_level(logging.INFO):
            extract_data(test_s3)

        assert "File successfully uploaded to ingestion bucket" in caplog.text
     
    @pytest.mark.it("test extract data creates correct warning logs")
    def test_extract_data_creates_correct_info_logs(self, test_s3, caplog, test_df_read_db):
        with caplog.at_level(logging.INFO):
            extract_data(test_s3, bucket=["fake-bucket", "fake-bucket"])

        assert "expected string or bytes-like object, got 'list'" in caplog.text

class TestLambdaHandler:
    @pytest.mark.it("test lambda hander invokes extract data ")
    def test_lambda_handler_invokes_extract_data(self,test_lambdas):
        test_event = {}
        test_context = ""
        response=lambda_handler(test_event,test_context)
        assert response == "lambdahandler is used correctly"