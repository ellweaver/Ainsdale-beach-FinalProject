from src.extract import extract_data
from unittest.mock import Mock, patch
import sys
from moto import mock_aws
import pytest 

class TestExtractData:
    @pytest.mark.it('test extract data uploads succesfully to s3')
    def test_extract_data_uploads_succesfully_to_s3(self,test_client):
        pass
    
    @pytest.mark.it('test extract data handles client_errors_succesfully')
    def test_extract_data_handles_errors(self):
        pass

    @pytest.mark.it('test extract data creates correct info logs')
    def test_extract_data_creates_correct_info_logs(self):
        pass

    @pytest.mark.it('test extract data creates correct warning logs')
    def test_extract_data_creates_correct_info_logs(self):
        pass