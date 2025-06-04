import pytest
import moto
from src.load import load_data

@pytest.mark.skip
class TestLoadData:
    @pytest.mark.it("Test load data retrieves parquets from transform s3 bucket")
    def test_load_data(self, test_tf_bucket):
        pass

    
    @pytest.mark.it("Test load data handle errors")
    def test_load_data_handle_errors():
        pass

    @pytest.mark.it("Test load data outputs correct info logs")
    def test_load_data_outputs_info_logs():
        pass
    
    @pytest.mark.it("Test load data outputs correct error logs")
    def test_load_data_outputs_error_logs():
        pass