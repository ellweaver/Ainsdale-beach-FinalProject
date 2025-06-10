import pytest
from load import load_data, lambda_handler
from utils import upload_file
import logging


class TestLoadData:
    @pytest.mark.it("Test load data retrieves parquets from transform s3 bucket")
    def test_load_data(self, test_tf_bucket, test_load_read_parquet):
        table_names = {
            "dim_date": "",
            "dim_staff": "",
            "dim_location": "",
            "dim_design": "",
            "dim_currency": "",
            "dim_counterparty": "",
            "fact_sales_order": "",
        }

        key = "data/2025/5/29/2025-05-29_00:00:00/"
        batch_id = "2025-05-29_00:00:00"
        source_bucket = "test_tf_bucket"
        for table in table_names:
            file = f"data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_{table}.parquet"
            upload_file(test_tf_bucket, file, source_bucket, file)
        response = load_data(
            test_tf_bucket, key, batch_id, sourcebucket=source_bucket, test=True
        )
        assert response == {
            "status": "Success",
            "code": 200,
            "key": key,
            "batch_id": batch_id,
        }
    
    @pytest.mark.it("Test load data handle errors")
    def test_load_data_handle_errors(self, test_tf_bucket):
        key = "data/2025/5/29/2025-05-29_00:00:00/"
        batch_id = "2025-05-29_00:00:00"
        source_bucket = "test_tf_bucket"
        response = load_data(
            test_tf_bucket, key, batch_id, sourcebucket=source_bucket, test=True
        )
        assert response == {"status": "Failure", "code": 404, "message": 'dim_date not found'}
   
    @pytest.mark.it("Test load data client exceptions errors")
    def test_load_data_handle_exceptions(self, test_tf_bucket):
        key = "test"
        batch_id = "test"
        source_bucket = "testdd_tf_bucket"
        response = load_data(
            test_tf_bucket, key, batch_id, sourcebucket=source_bucket, test=True
        )
        assert response == {"status": "Failure", "code": 404, "message": 'dim_date not found'}


class TestLoadDataLogging:
    @pytest.mark.it("Test load data uses correct logger")
    def test_load_data_uses_correct_logger(self, test_tf_bucket, caplog,test_load_read_parquet):

        key = "data/2025/5/29/2025-05-29_00:00:00/"
        batch_id = "2025-05-29_00:00:00"
        source_bucket = "test_tf_bucket"

        file = f"data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_fact_sales_order.parquet"
        upload_file(test_tf_bucket, file, source_bucket, file)
        with caplog.at_level(logging.INFO):
            load_data(
                test_tf_bucket, key, batch_id, sourcebucket=source_bucket, test=True
            )

        assert "load" in caplog.text

    @pytest.mark.it("Test load data outputs correct info logs")
    def test_load_data_outputs_info_logs(self, test_tf_bucket, caplog, test_load_read_parquet):
        table_names = {
            "dim_date": "",
            "dim_staff": "",
            "dim_location": "",
            "dim_design": "",
            "dim_currency": "",
            "dim_counterparty": "",
            "fact_sales_order": "",
        }

        key = "data/2025/5/29/2025-05-29_00:00:00/"
        batch_id = "2025-05-29_00:00:00"
        source_bucket = "test_tf_bucket"
        for table in table_names:
            file = f"data/2025/5/29/2025-05-29_00:00:00/2025-05-29_00:00:00_{table}.parquet"
            upload_file(test_tf_bucket, file, source_bucket, file)
        with caplog.at_level(logging.INFO):
            load_data(
                test_tf_bucket, key, batch_id, sourcebucket=source_bucket, test=True
            )
        log_list = [
            "fact_sales_order successfully uploaded to data warehouse",
            "dim_date successfully uploaded to data warehouse",
            "dim_staff successfully uploaded to data warehouse",
            "dim_location successfully uploaded to data warehouse",
            "dim_design successfully uploaded to data warehouse",
            "dim_currency successfully uploaded to data warehouse",
            "dim_counterparty successfully uploaded to data warehouse",
            "All tables successfully uploaded to data warehouse",
        ]
        for log in log_list:
            assert log in caplog.text
    
    @pytest.mark.it("Test load data outputs correct error logs")
    def test_load_data_outputs_error_logs(self, test_tf_bucket, caplog,test_load_read_parquet):
        key = "data/2025/5/29/2025-05-29_00:00:00/"
        batch_id = "2025-05-29_00:00:00"
        source_bucket = "test_tf_bucket"
        with caplog.at_level(logging.ERROR):
            load_data(
                test_tf_bucket, key, batch_id, sourcebucket=source_bucket, test=True
            )
        print(caplog.text)
        assert (
            "{'status': 'Failure', 'code': 404, 'message': 'dim_date not found'}"
            in caplog.text
        )

class TestLambdaHandler:
    @pytest.mark.it('test lambda handle invoke load data')
    def test_lambda_handler(self, test_lambdas):
        test_event = {
  "status": "Success",
  "code": 200,
  "key": "test",
  "batch_id": "test"
}
        test_context = ""
        response=lambda_handler(test_event,test_context)
        assert response == "lambdahandler is used correctly"
       