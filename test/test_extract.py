from src.extract import extract_data
from unittest.mock import Mock, patch
from unittest import TestCase
import sys
import pytest
import logging


class TestExtractData:

    @pytest.mark.skip
    @pytest.mark.it("uploads succesfully to s3")
    def test_extract_data_uploads_succesfully_to_s3(self, test_client):
        response = extract_data(test_client)
        assert response == {"status": "Success", "code": 200}

    @pytest.mark.skip
    @pytest.mark.it("handles client_errors_succesfully")
    def test_extract_data_handles_errors(self, test_client):
        response = extract_data(test_client)
        assert response["result"] == "FAILURE"
        assert response["message"] == "upload failed"

    @pytest.mark.skip
    @pytest.mark.it("s3 key naming follows datetime_folder/datetime_tablename")
    def test_extract_data_s3_key_naming_follows_datetime_folder_datetime_tablename(
        self, test_client
    ):
        response = extract_data(test_client)
        # asserts


class TestExtractDataLogging:

    @pytest.mark.it("creates correct logger_used")
    def test_extract_data_uses_correct_logger(self, test_s3, caplog):
        with caplog.at_level(logging.INFO):
            extract_data(test_s3)
            # print(caplog)
            # print("^^^^", caplog.text)
        assert "File successfully uploaded to ingestion bucket" in caplog.text

    # change below tests to use caplog
    @pytest.mark.skip
    @pytest.mark.it("creates correct info logs")
    def test_extract_data_creates_info_log(self, test_client):
        with self.assertLogs() as captured:
            extract_data(test_client)
        self.assertEqual(captured.records[0].levelname, "INFO")

    @pytest.mark.skip
    @pytest.mark.it("outputs correct info message")
    def test_extract_data_outputs_correct_info_message(self, test_client):
        with self.assertLogs() as captured:
            extract_data(test_client)
        self.assertIn("is this message there>", captured.output[0])

    @pytest.mark.skip
    @pytest.mark.it("outputs correct number of info message")
    def test_extract_data_outputs_correct_number_of_info_message(self, test_client):
        with self.assertLogs() as captured:
            extract_data(test_client)
        self.assertEqual(len(captured.records[0]), 1)

    @pytest.mark.skip
    @pytest.mark.it("test extract data creates correct warning logs")
    def test_extract_data_creates_correct_info_logs(self):
        pass
